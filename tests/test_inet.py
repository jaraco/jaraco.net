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
