import socket
import struct
import logging
import argparse
import datetime

from jaraco.text import trim
import jaraco.logging

log = logging.getLogger(__name__)

TIME1970 = 0x83AA7E80


def query(server, force_ipv6=False):
    """
    Return current time from NTP server as a Unix timestamp

    >>> import time
    >>> res = query('us.pool.ntp.org')
    >>> type(res)
    <class 'int'>
    >>> res > time.time() - 5
    True
    """
    timeout = 3
    ntp_port = 123

    family = socket.AF_INET6 if force_ipv6 else 0
    sock_type = socket.SOCK_DGRAM

    infos = socket.getaddrinfo(server, ntp_port, family, sock_type)

    log.debug(infos)
    family, socktype, proto, canonname, sockaddr = infos[0]

    log.info(f'Requesting time from {sockaddr}')
    client = socket.socket(family=family, type=sock_type, proto=proto)
    client.settimeout(timeout)

    data = b'\x1b' + 47 * b'\x00'
    client.sendto(data, sockaddr)
    data, address = client.recvfrom(1024)
    if not data:
        return

    log.info(f'Response received from: {address}')
    t = struct.unpack('!12I', data)[10]
    return t - TIME1970


def handle_command_line():
    """
    Query the NTP server for the current time.
    """
    parser = argparse.ArgumentParser(usage=trim(handle_command_line.__doc__))
    parser.add_argument(
        '-6', '--ipv6', help="Force IPv6", action="store_true", default=False
    )
    parser.add_argument('server', help="IP Address of server to query")
    jaraco.logging.add_arguments(parser)
    args = parser.parse_args()
    jaraco.logging.setup(args)
    logging.root.handlers[0].setFormatter(logging.Formatter("%(message)s"))
    val = query(args.server, args.ipv6)
    dt = datetime.datetime.fromtimestamp(val)  # noqa
    log.info(f'\tTime={dt}')


if __name__ == '__main__':
    handle_command_line()
