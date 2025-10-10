import time

def elapse_time(since):
    return time.time() - since

def mock_time():
    return 200

def test_elapsed():
    time.time = mock_time
    assert elapse_time(50) == 150