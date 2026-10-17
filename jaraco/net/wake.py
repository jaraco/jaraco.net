import socket
import struct


def wake_on_lan(self, addr='00:00:00:00:00:00'):
    "Wake up a computer on the network"
    bytes = (int(bs, 16) for bs in addr.split(':'))
    binary_addr = struct.pack('BBBBBB', *bytes)
    magic_packet = b'\xff' * 6 + binary_addr * 16
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.sendto(magic_packet, ('<broadcast>', 9))
    s.close()
    return f'Woke up the computer at {addr}'
