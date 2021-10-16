import server
import pytest


class Test_Server_Process:
    def test_process_1(self):
        server.process(True)

    def test_process_2(self):
        server.process(False)


class Test_Worker_Run:
    @pytest.fixture()
    def worker(self):
        return server.Worker()

    def test_run_1(self, worker):
        worker.run()

def test_cookie 