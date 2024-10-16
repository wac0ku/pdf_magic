# Author: Leon Gajtner
# Datum 15.10.2024
# Project: PDF Magic main file

from impl import PDFConverter, DropArea
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QProgressBar, QTextEdit, QFileDialog, QLabel
from PyQt5.QtGui import QColor, QPalette, QFont
from PyQt5.QtCore import Qt
import sys
import logging

class ModernButton(QPushButton):
    """
    Custom button class with modern styling.
    """
    def __init__(self, text, color):
        """
        Initialize the button with custom styling.
        
        :param text: Button text
        :param color: Base color for the button
        """
        super().__init__(text)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border: none;
                color: white;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 8px;
            }}
            QPushButton:hover {{
                background-color: {QColor(color).darker(110).name()};
            }}
            QPushButton:pressed {{
                background-color: {QColor(color).darker(120).name()};
            }}
        """)

class MainWindow(QMainWindow):
    """
    Main application window for the PDF to DOCX converter.
    """
    def __init__(self):
        """
        Initialize the main window and set up the UI.
        """
        super().__init__()
        self.setWindowTitle("PDF zu DOCX Konverter")
        self.setGeometry(100, 100, 800, 600)

        # Define color scheme
        self.colors = {
            'background': '#F0F4F8',
            'primary': '#4A90E2',
            'secondary': '#50C878',
            'text': '#333333',
            'accent': '#FF6B6B'
        }

        # Set window style
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {self.colors['background']};
            }}
            QLabel, QTextEdit {{
                color: {self.colors['text']};
            }}
        """)

        # Set up central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Add title label
        title_label = QLabel("PDF zu DOCX Konverter")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"""
            font-size: 24px;
            color: {self.colors['primary']};
            margin-bottom: 20px;
            font-weight: bold;
        """)
        layout.addWidget(title_label)

        # Set up drop area
        self.drop_area = DropArea()
        self.drop_area.setStyleSheet(f"""
            QWidget {{
                border: 2px dashed {self.colors['primary']};
                border-radius: 12px;
                background-color: {QColor(self.colors['primary']).lighter(180).name()};
                min-height: 150px;
            }}
            QWidget:hover {{
                background-color: {QColor(self.colors['primary']).lighter(170).name()};
            }}
        """)
        self.drop_area.files_dropped.connect(self.add_files)
        layout.addWidget(self.drop_area)

        # Set up buttons
        button_layout = QHBoxLayout()
        self.select_button = ModernButton("PDFs auswählen", self.colors['primary'])
        self.select_button.clicked.connect(self.select_files)
        button_layout.addWidget(self.select_button)

        self.convert_button = ModernButton("Konvertieren", self.colors['secondary'])
        self.convert_button.clicked.connect(self.start_conversion)
        button_layout.addWidget(self.convert_button)

        layout.addLayout(button_layout)

        # Set up progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 2px solid {self.colors['primary']};
                border-radius: 5px;
                text-align: center;
            }}
            QProgressBar::chunk {{
                background-color: {self.colors['secondary']};
                width: 10px;
                margin: 0.5px;
            }}
        """)
        layout.addWidget(self.progress_bar)

        # Set up log text area
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet(f"""
            background-color: white;
            border: 1px solid {self.colors['primary']};
            border-radius: 5px;
            padding: 5px;
        """)
        layout.addWidget(self.log_text)

        self.pdf_files = []

        # Set up logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def select_files(self):
        """
        Open a file dialog to select PDF files.
        """
        files, _ = QFileDialog.getOpenFileNames(self, "PDFs auswählen", "", "PDF Dateien (*.pdf)")
        self.add_files(files)

    def add_files(self, files):
        """
        Add selected files to the conversion list.
        
        :param files: List of file paths to add
        """
        new_files = [f for f in files if f not in self.pdf_files]
        self.pdf_files.extend(new_files)
        self.log_text.append(f"<span style='color: {self.colors['secondary']};'>{len(new_files)} neue PDF(s) hinzugefügt.</span>")
        self.logger.info(f"{len(new_files)} neue PDF(s) zur Konvertierung hinzugefügt.")
        self.update_drop_area_label()

    def update_drop_area_label(self):
        """
        Update the drop area label to show the number of selected files.
        """
        if self.pdf_files:
            self.drop_area.label.setText(f"<span style='font-size: 18px;'>{len(self.pdf_files)} PDF(s) ausgewählt</span>")
        else:
            self.drop_area.label.setText("<span style='font-size: 18px;'>PDF-Dateien hier hineinziehen</span>")
        self.drop_area.label.setStyleSheet(f"color: {self.colors['primary']};")

    def start_conversion(self):
        """
        Start the PDF to DOCX conversion process.
        """
        if not self.pdf_files:
            self.log_text.append(f"<span style='color: {self.colors['accent']};'>Keine PDF-Dateien ausgewählt.</span>")
            return

        self.converter = PDFConverter(self.pdf_files)
        self.converter.update_progress.connect(self.update_progress)
        self.converter.update_log.connect(self.update_log)
        self.converter.finished.connect(self.conversion_finished)
        self.converter.start()

        self.convert_button.setEnabled(False)
        self.select_button.setEnabled(False)

    def update_progress(self, value):
        """
        Update the progress bar.
        
        :param value: Progress value (0-100)
        """
        self.progress_bar.setValue(value)

    def update_log(self, message):
        """
        Update the log text area with a new message.
        
        :param message: Log message to append
        """
        self.log_text.append(f"<span style='color: {self.colors['text']};'>{message}</span>")
        self.logger.info(message)

    def conversion_finished(self):
        """
        Handle the completion of the conversion process.
        """
        self.convert_button.setEnabled(True)
        self.select_button.setEnabled(True)
        self.pdf_files = []
        self.update_drop_area_label()
        self.log_text.append(f"<span style='color: {self.colors['secondary']};'>Konvertierung abgeschlossen.</span>")
        self.logger.info("Konvertierung abgeschlossen.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())