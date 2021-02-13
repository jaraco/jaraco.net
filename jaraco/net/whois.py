#! -*- coding: UTF-8 -*-

"""whois_bridge.py

HTTP scraper for nic servers who only offer whois service via web only.

Run the script from the command line and it will service port 43 as a whois
server, passing the query to the appropriate web form and parsing the results
into a textual format.
"""

import os
import re
import logging
import abc
import socket
import select
import urllib
import http.cookiejar as http_cookiejar
import socketserver

try:
    from ClientForm import ParseResponse, ItemNotFoundError
except ImportError:
    "Disabled for Python 3 compatibility"
from bs4 import BeautifulSoup
from jaraco.classes.meta import LeafClassesMeta

from .http import mechanize

log = logging.getLogger(__name__)


def init():
    """
    Initialize HTTP functionality to support cookies, which are necessary
    to use the HTTP interface.
    """
    cj = http_cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    urllib.request.install_opener(opener)


class WhoisHandler(metaclass=LeafClassesMeta):
    """
    WhoisHandler is an abstract class for defining whois interfaces for
    web-based nic servers.
    """

    @abc.abstractproperty
    def services(self):
        "Regular expression that will match domains serviced by this handler."

    @abc.abstractmethod
    def LoadHTTP(self):
        """
        Retrieve the HTTP response and a _parser class which is an HTMLParser
        capable of parsing the response and outputting the textual result.
        """

    def __init__(self, query=None):
        self._query = query

    @classmethod
    def _query_matches_services(cls, query):
        return re.search(cls.services, query, re.IGNORECASE)

    @staticmethod
    def GetHandler(query):
        """Search through the WhoisHandler subclasses and return the one
        that matches the query."""
        query = query.lower()
        handlers = WhoisHandler._leaf_classes
        matches = [c for c in handlers if c._query_matches_services(query)]
        if not len(matches) == 1:
            error = [
                'Domain for %s is not serviced by this server.',
                'Server error, ambiguous nic server resolution for %s.',
            ][bool(len(matches))]
            raise ValueError(error % query)
        return matches[0](query)

    @staticmethod
    def _IsWhoisHandler_(ob):
        return hasattr(ob, '__bases__') and WhoisHandler in ob.__bases__

    def ParseResponse(self):
        soup = BeautifulSoup(self._response)
        return soup.get_text()


class ArgentinaWhoisHandler(WhoisHandler):
    services = r'\.ar$'

    def LoadHTTP(self):
        query = self._query
        pageURL = 'http://www.nic.ar/consdom.html'
        form = ParseResponse(urllib.request.urlopen(pageURL))[0]
        form['nombre'] = query[: query.find('.')]
        try:
            domain = query[query.find('.') :]
            form['dominio'] = [domain]
        except ItemNotFoundError:
            raise ValueError('Invalid domain (%s)' % domain)
        req = form.click()
        # req.data = 'nombre=%s&dominio=.com.ar' % query
        req.add_header('referer', pageURL)
        resp = urllib.request.urlopen(req)
        self._response = resp.read()


class CoZaWhoisHandler(WhoisHandler):
    services = r'\.co\.za$'

    def LoadHTTP(self):
        query = self._query
        pageURL = 'http://whois.co.za/'
        form = ParseResponse(urllib.request.urlopen(pageURL))[0]
        form['Domain'] = query[: query.find('.')]
        req = form.click()
        resp = urllib.request.urlopen(req)
        self._response = resp.read()


class GovWhoisHandler(WhoisHandler):
    services = r'(\.fed\.us|\.gov)$'

    def LoadHTTP(self):
        query = self._query
        # Perform an whois query on the dotgov server.
        url = urllib.request.urlopen('http://dotgov.gov/whois.aspx')
        forms = ParseResponse(url)
        assert len(forms) == 1
        form = forms[0]
        if form.attrs['action'] == 'agree.aspx':
            # we've been redirected to a different form
            # need to agree to license agreement
            self.Agree(form)
            # note this could get to an infinite loop if cookies aren't working
            # or for whatever reason we're always being redirected to the
            # agree.aspx page.
            return self.LoadHTTP()
        form['who_search'] = query
        resp = urllib.request.urlopen(forms[0].click())
        self._response = resp.read()

    def Agree(self, form):
        "agree to the dotgov agreement"
        agree_req = form.click()
        u2 = urllib.request.urlopen(agree_req)
        u2.read()

    def ParseResponse(self):
        soup = BeautifulSoup(self._response)
        target = soup.select('#TD1')
        return target.get_text()


mozilla_headers = {
    'referer': 'http://www.nic.bo/buscar.php',
    'accept': 'text/xml,application/xml,application/xhtml+xml,text/html;'
    'q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5',
    'accept-encoding': 'gzip,deflate',
    'user-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8) '
    'Gecko/20051111 Firefox/1.5',
    'accept-charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
    'accept-language': 'en-us,en;q=0.5',
}


class BoliviaWhoisHandler(WhoisHandler):
    services = r'\.bo$'

    def LoadHTTP(self):
        name, domain = self._query.split('.', 1)
        domain = '.' + domain
        getter = mechanize.PageGetter()
        search_page = getter.load('http://www.nic.bo/')
        form_items = {'subdominio': [domain], 'dominio': name}
        resp = getter.process_form(search_page, form_items)

        # now that we've submitted the request, we've got a response.
        # This page returns 'available' or 'not available'
        # If it's not available, we need to know who owns it.
        if re.search('Dominio %s registrado' % self._query, resp.text):
            info_url = urllib.parse.basejoin(resp.url, 'informacion.php')
            resp = getter.load(info_url)

        self._response = resp.text

    def ParseResponse(self):
        soup = BeautifulSoup(self._response)
        return soup.strong.parent.div.text


class SourceWhoisHandler(WhoisHandler):
    """This is not a typical Whois handler, but rather a special
    handler that returns the source of this file"""

    services = r'^source$'

    def LoadHTTP(self):
        pass

    def ParseResponse(self):
        filename = os.path.splitext(__file__)[0] + '.py'
        return open(filename).read()


class DebugHandler(WhoisHandler):
    services = r'^debug (.*)$'
    authorized_addresses = ['127.0.0.1']

    def LoadHTTP(self):
        pass

    def ParseResponse(self):
        if self.client_address[0] not in self.authorized_addresses:
            return
        match = re.match(self.services, self._query)
        return 'result: %s' % eval(match.group(1))


# disable the debug handler
del DebugHandler


class Handler(socketserver.StreamRequestHandler):
    def handle(self):
        try:
            self._handle()
        except Exception:
            log.exception('unhandled exception')

    def _handle(self):
        query = self.rfile.readline().decode('utf-8').strip()
        log.info('%s requests %s', self.client_address, query)
        try:
            handler = WhoisHandler.GetHandler(query)
            handler.client_address = self.client_address
            handler.LoadHTTP()
            self.wfile.write(handler.ParseResponse())
            log.info('%s success', self.client_address)
        except urllib.error.URLError:
            msg = 'Could not contact whois HTTP service.'
            self.wfile.write(msg + '\n')
            log.exception(msg)
        except ValueError as e:
            log.info('%s response %s', self.client_address, e)
            out = '%s\n' % e
            self.wfile.write(out.encode('utf-8'))


class ConnectionClosed(Exception):
    pass


class Listener(socketserver.ThreadingTCPServer):
    def __init__(self):
        socketserver.ThreadingTCPServer.__init__(self, ('', 43), Handler)

    def serve_until_closed(self):
        try:
            while True:
                self.handle_request()
        except ConnectionClosed:
            pass

    def get_request(self):
        # use select here because select will throw an exception if the socket
        #  is closed.  Simply blocking on accept will block even if the socket
        #  object is closed.
        try:
            select.select((self.socket,), (), ())
        except socket.error as e:
            if e[1].lower() == 'bad file descriptor':
                raise ConnectionClosed
        return socketserver.ThreadingTCPServer.get_request(self)


def serve():
    init()
    Listener().serve_forever()


if __name__ == '__main__':
    serve()
