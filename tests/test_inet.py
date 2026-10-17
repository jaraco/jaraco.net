import errno
import io
import socket
import threading

from jaraco.net import inet


def test_wait_for_testers_to_finish(monkeypatch):
    done = []
    tester = threading.Thread(target=lambda: done.append(True))
    monkeypatch.setattr(inet.ScanThread, 'all_testers', [tester])
    tester.start()
    inet.ScanThread.wait_for_testers_to_finish()
    assert done == [True]
    assert not tester.is_alive()


def test_port_listener_address_in_use(monkeypatch):
    class FakeSocket:
        def __init__(self, *args):
            pass

        def bind(self, addr):
            raise OSError(errno.EADDRINUSE, 'Address already in use')

    monkeypatch.setattr(socket, 'socket', FakeSocket)
    listener = inet.PortListener(8080)
    listener.output = io.StringIO()
    listener.run()
    assert 'Cannot listen on port 8080' in listener.output.getvalue()
