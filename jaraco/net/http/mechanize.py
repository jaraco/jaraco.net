import urllib2
import logging

import ClientForm

log = logging.getLogger(__name__)

class PageGetter(object):
	"""
	PageGetter
	A helper class for common HTTP page retrieval.
	"""

	def __init__(self, **attrs):
		"set url to the target url or set request to the urllib2.Request object"
		self.__dict__.update(attrs)

	def GetRequest(self):
		req = getattr(self, 'request', None) or urllib2.Request(getattr(self, 'url'))
		return req

	def Fetch(self):
		return self._opener.open(self.GetRequest())

	def Process(self):
		resp = self.Fetch()
		forms = ClientForm.ParseResponse(resp)
		form = self.SelectForm(forms)
		self.FillForm(form)
		return form.click()

	def SelectForm(self, forms):
		sel = getattr(self, 'form_selector', 0)
		log.info('selecting form %s', sel)
		if not isinstance(sel, int):
			# assume the selector is the name of the form
			forms = dict(map(lambda f: (f.name, f), forms))
		return forms[sel]

	def FillForm(self, form):
		for name, value in self.form_items.items():
			if callable(value):
				value = value()
			form[name] = value

	def __call__(self, next):
		# process the form and set the request for the next object
		next.request = self.Process()
		return next
