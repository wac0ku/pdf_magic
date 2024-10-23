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
        logger.info(f"Using {self.thread_pool.maxThreadCount()} threads")
        
        self.initialize_components()
        self.setup_workers()
        self.setup_controllers()
        self.setup_theme()
        self.connect_signals_and_slots()
        
    def initialize_components(self):
        """Initialisiert alle Hauptkomponenten der Anwendung"""
        # Utils
        self.config_manager = ConfigManager('config.json')
        self.error_handler = ErrorHandler()
        self.file_handler = FileHandler()
        self.pdf_processor = PDFProcessor()
        
        # Models
        self.settings_model = SettingsModel(self.config_manager)
        self.conversion_model = ConversionModel(self.pdf_processor)
        self.extraction_model = ExtractionModel(self.pdf_processor)
        self.conversion_manager = ConversionManager(
            self.conversion_model,
            self.extraction_model
        )
        
        # Themes
        self.theme_manager = ThemeManager(self.settings_model)
        
        # UI
        self.main_window = MainWindow(self.theme_manager)
        
    def setup_workers(self):
        """Initialisiert und konfiguriert alle Worker"""
        self.worker_signals = WorkerSignals()
        
        # Worker-Instanzen erstellen
        self.pdf_converter = PDFConverterWorker(self.pdf_processor)
        self.text_extractor = TextExtractorWorker(self.pdf_processor)
        self.metadata_extractor = MetadataExtractorWorker(self.pdf_processor)
        self.image_to_pdf = ImageToPDFWorker(self.pdf_processor)
        
        # Worker mit Models verbinden
        self.conversion_model.register_worker(self.pdf_converter)
        self.conversion_model.register_worker(self.image_to_pdf)
        self.extraction_model.register_worker(self.text_extractor)
        self.extraction_model.register_worker(self.metadata_extractor)
        
        # Worker-Signale verbinden
        for worker in [self.pdf_converter, self.text_extractor, 
                      self.metadata_extractor, self.image_to_pdf]:
            worker.signals.progress.connect(self.main_window.update_progress)
            worker.signals.error.connect(self.error_handler.handle_error)
            worker.signals.finished.connect(self.main_window.on_task_completed)

    def setup_controllers(self):
        """Initialisiert und konfiguriert alle Controller"""
        # Controller erstellen
        self.main_controller = MainController(
            view=self.main_window,
            conversion_manager=self.conversion_manager,
            settings_model=self.settings_model
        )
        
        self.conversion_controller = ConversionController(
            model=self.conversion_model,
            view=self.main_window.conversion_tab,
            thread_pool=self.thread_pool,
            file_handler=self.file_handler
        )
        
        self.extraction_controller = ExtractionController(
            model=self.extraction_model,
            view=self.main_window.extraction_tab,
            thread_pool=self.thread_pool,
            file_handler=self.file_handler
        )
        
        self.settings_controller = SettingsController(
            model=self.settings_model,
            view=self.main_window.settings_dialog,
            theme_manager=self.theme_manager
        )
        
        # Controller miteinander verbinden
        self.main_controller.set_conversion_controller(self.conversion_controller)
        self.main_controller.set_extraction_controller(self.extraction_controller)
        self.main_controller.set_settings_controller(self.settings_controller)

    def setup_theme(self):
        """Konfiguriert und wendet das aktuelle Theme an"""
        current_theme = self.theme_manager.get_theme(self.settings_model.get_theme())
        self.main_window.apply_theme(current_theme)

    def connect_signals_and_slots(self):
        """Verbindet alle Signale und Slots der Anwendung"""
        # Main Window Signale
        self.main_window.show_conversion_tab_signal.connect(
            self.main_controller.show_conversion_tab)
        self.main_window.show_extraction_tab_signal.connect(
            self.main_controller.show_extraction_tab)
        self.main_window.show_settings_dialog_signal.connect(
            self.main_controller.show_settings_dialog)

        # Conversion Tab Signale
        conv_tab = self.main_window.conversion_tab
        conv_tab.start_conversion_signal.connect(
            self.conversion_controller.start_conversion)
        conv_tab.cancel_conversion_signal.connect(
            self.conversion_controller.cancel_conversion)
        conv_tab.file_dropped_signal.connect(
            self.conversion_controller.handle_file_drop)
        
        # Extraction Tab Signale
        ext_tab = self.main_window.extraction_tab
        ext_tab.start_extraction_signal.connect(
            self.extraction_controller.start_extraction)
        ext_tab.cancel_extraction_signal.connect(
            self.extraction_controller.cancel_extraction)
        ext_tab.file_dropped_signal.connect(
            self.extraction_controller.handle_file_drop)
            
        # Settings Dialog Signale
        settings = self.main_window.settings_dialog
        settings.theme_changed_signal.connect(
            self.theme_manager.change_theme)
        settings.settings_saved_signal.connect(
            self.settings_model.save_settings)
            
        # Error Handler Signale
        self.error_handler.error_occurred_signal.connect(
            self.main_window.show_error_message)

    def run(self):
        """Startet die Anwendung"""
        try:
            logger.info("Starting PDF Magic application")
            self.main_window.show()
            logger.info("Main window displayed")
            return self.app.exec_()
        except Exception as e:
            logger.critical(f"Fatal error during application startup: {str(e)}")
            self.error_handler.handle_error(e)
            return 1

def main():
    pdf_magic = PDFMagicApp()
    sys.exit(pdf_magic.run())

if __name__ == "__main__":
    main()