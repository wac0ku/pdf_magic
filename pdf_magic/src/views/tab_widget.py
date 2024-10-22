from PyQt5.QtWidgets import QTabWidget
from .file_preview import FilePreview
from .progress_overview import ProgressOverview

class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.file_preview = FilePreview()
        self.progress_overview = ProgressOverview()

        self.addTab(self.file_preview, "File Preview")
        self.addTab(self.progress_overview, "Progress Overview")