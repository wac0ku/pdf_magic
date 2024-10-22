from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QProgressBar

class ProgressOverview(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QGridLayout(self)

        self.progress_label = QLabel("No task in progress")
        layout.addWidget(self.progress_label, 0, 0)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar, 1, 0)

        self.updateUI()

    def updateUI(self):
        # Update the UI based on the current task progress
        pass