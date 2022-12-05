import ifparser

from .base import BaseManager


def if_config():
    cfg = subprocess.check_output(['ifconfig'])
    return ifparser.Ifcfg(cfg)


class Manager(BaseManager):
    def get_host_mac_addresses(self):
        return map(operator.attrgetter('hwaddr'), self._get_ifaces())

    def get_host_ip_addresses(self):
        return map(operator.attrgetter('ip'), self._get_ifaces())

    @staticmethod
    def _get_ifaces():
        cfg = if_config()
        return map(cfg.get_interface, cfg.interfaces)
