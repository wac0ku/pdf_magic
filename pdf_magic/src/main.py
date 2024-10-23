import sys
import traceback
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThreadPool

# UI
from ui.main_window import MainWindow

# Models
from models.conversion_manager import ConversionManager
from models.settings_model import SettingsModel
from models.conversion_model import ConversionModel
from models.extraction_model import ExtractionModel

# Controllers
from controllers.main_controller import MainController
from controllers.conversion_controller import ConversionController
from controllers.extraction_controller import ExtractionController
from controllers.settings_controller import SettingsController

# Workers
from workers.base_worker import BaseWorker, WorkerSignals
from workers.pdf_converter_worker import PDFConverterWorker
from workers.text_extractor_worker import TextExtractorWorker
from workers.metadata_extractor_worker import MetadataExtractorWorker
from workers.image_to_pdf_worker import ImageToPDFWorker

# Themes
from themes.theme_manager import ThemeManager

# Utils
from utils.logger import logger
from utils.error_handler import ErrorHandler
from utils.config_manager import ConfigManager
from utils.file_handler import FileHandler
from utils.pdf_processor import PDFProcessor

def exception_hook(exctype, value, tb):
    logger.error(f"Uncaught exception: {exctype}, {value}")
    logger.error(''.join(traceback.format_tb(tb)))
    sys.__excepthook__(exctype, value, tb)

sys.excepthook = exception_hook

class PDFMagicApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.thread_pool = QThreadPool()
        
        # Models
        self.conversion_manager = ConversionManager()
        self.settings_model = SettingsModel()
        self.conversion_model = ConversionModel()
        self.extraction_model = ExtractionModel()
        
        # Utils
        self.config_manager = ConfigManager('config.json')
        self.file_handler = FileHandler()
        self.pdf_processor = PDFProcessor()
        self.error_handler = ErrorHandler()
        
        # Themes
        self.theme_manager = ThemeManager()
        
        # UI
        self.main_window = MainWindow()
        
        # Controllers
        self.main_controller = MainController(self.main_window)
        self.conversion_controller = ConversionController(self.conversion_model, self.main_window.conversion_tab, self.thread_pool)
        self.extraction_controller = ExtractionController(self.extraction_model, self.main_window.extraction_tab, self.thread_pool)
        self.settings_controller = SettingsController(self.settings_model, self.main_window.settings_dialog)

        # Workers
        self.worker_signals = WorkerSignals(PDFConverterWorker, TextExtractorWorker, MetadataExtractorWorker,  ImageToPDFWorker)
        self.base_worker = BaseWorker()

        self.setup_controllers()
        self.setup_theme()

    def setup_controllers(self):
        self.main_controller.set_conversion_controller(self.conversion_controller)
        self.main_controller.set_extraction_controller(self.extraction_controller)
        self.main_controller.set_settings_controller(self.settings_controller)

    def setup_theme(self):
        current_theme = self.theme_manager.get_theme(self.settings_model.get_theme())
        self.main_window.apply_theme(current_theme)

    def connect_signals_and_slots(self):
        # Main Window signals
        self.main_window.show_conversion_tab_signal.connect(self.main_controller.show_conversion_tab)
        self.main_window.show_extraction_tab_signal.connect(self.main_controller.show_extraction_tab)
        self.main_window.show_settings_dialog_signal.connect(self.main_controller.show_settings_dialog)

        # Conversion signals
        self.main_window.conversion_tab.start_conversion_signal.connect(self.conversion_controller.start_conversion)
        self.main_window.conversion_tab.cancel_conversion_signal.connect(self.conversion_controller.cancel_conversion)

        # Extraction signals
        self.main_window.extraction_tab.start_extraction_signal.connect(self.extraction_controller.start_extraction)
        self.main_window.extraction_tab.cancel_extraction_signal.connect(self.extraction_controller.cancel_extraction)

    def run(self):
        logger.info("Starting PDF Magic application")
        self.connect_signals_and_slots()
        self.main_window.show()
        logger.info("Main window displayed")
        return self.app.exec_()

def main():
    pdf_magic = PDFMagicApp()
    sys.exit(pdf_magic.run())

if __name__ == "__main__":
    main()