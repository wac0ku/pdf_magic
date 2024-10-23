from PyQt5.QtCore import QObject, pyqtSignal, QRunnable

class WorkerSignals(QObject):
    """
    Definiert die Signale für den Worker
    """
    started = pyqtSignal()
    finished = pyqtSignal()
    error = pyqtSignal(str)
    progress = pyqtSignal(int)
    result = pyqtSignal(object)

class BaseWorker(QRunnable):
    """
    Basis-Worker-Klasse, die von QRunnable erbt
    """
    def __init__(self):
        super().__init__()
        self.signals = WorkerSignals()
        self.is_cancelled = False

    def run(self):
        """
        Muss von abgeleiteten Klassen implementiert werden
        """
        raise NotImplementedError("Subclasses must implement run()")

    def cancel(self):
        """
        Bricht die Ausführung ab
        """
        self.is_cancelled = True
