from PyQt5.QtCore import QObject, QThreadPool
from utils.logger import logger
from utils.file_handler import FileHandler

class BaseController(QObject):
    def __init__(self, thread_pool: QThreadPool, file_handler: FileHandler):
        super().__init__()
        self.thread_pool = thread_pool
        self.file_handler = file_handler
        self.current_worker = None

    def _start_worker(self, worker):
        """Startet einen Worker im ThreadPool"""
        self.current_worker = worker
        self.thread_pool.start(worker)

    def cancel_current_task(self):
        """Bricht die aktuelle Aufgabe ab"""
        if self.current_worker:
            self.current_worker.cancel()
            self.current_worker = None
