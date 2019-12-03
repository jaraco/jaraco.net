"""
whois_bridge service for Windows
"""


import os
import sys
import logging

import win32service
import win32serviceutil
import servicemanager
import jaraco.logging


log = logging.getLogger(__name__)


class Service(win32serviceutil.ServiceFramework):
    _svc_name_ = 'whois_bridge'
    _svc_display_name_ = 'Whois HTTP Bridge'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.listener.server_close()

    def SvcDoRun(self):
        self._setup_logging()

        log.info('%s service is starting.', self._svc_display_name_)
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, ''),
        )

        self.run()

        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STOPPED,
            (self._svc_name_, ''),
        )
        log.info('%s service is stopped.', self._svc_display_name_)

    def run(self):
        from jaraco.net.whois import init, Listener

        init()
        self.listener = Listener()
        self.listener.serve_until_closed()

    def _setup_logging(self):
        logfile = os.path.join(
            os.environ['WINDIR'],
            'system32',
            'LogFiles',
            self._svc_display_name_,
            'events.log',
        )
        handler = jaraco.logging.TimestampFileHandler(logfile)
        handlerFormat = '[%(asctime)s] - %(levelname)s - [%(name)s] %(message)s'
        handler.setFormatter(logging.Formatter(handlerFormat))
        logging.root.addHandler(handler)
        # Redirect stdout and stderr, else when the stdio flushes,
        # an exception will be thrown and the service will bail
        sys.stdout = jaraco.logging.LogFileWrapper('stdout')
        sys.stderr = jaraco.logging.LogFileWrapper('stderr')
        logging.root.level = logging.INFO

    @classmethod
    def handle_command_line(cls):
        win32serviceutil.HandleCommandLine(cls)
