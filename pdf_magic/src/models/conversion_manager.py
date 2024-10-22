from PyQt5.QtCore import QObject, pyqtSignal
from .conversion_model import ConversionModel, ConversionType, ConversionStatus
from utils.pdf_processor import PDFProcessor
import os

class ConversionManager(QObject):
    conversion_started = pyqtSignal(str)
    conversion_progress = pyqtSignal(str, int)
    conversion_completed = pyqtSignal(str)
    conversion_failed = pyqtSignal(str, str)
    log_update = pyqtSignal(str, str) # task_id, message

    def __init__(self, settings_model):
        super().__init__()
        self.conversion_model = ConversionModel()
        self.settings_model = settings_model
        self.active_conversions = {}

    def start_conversion(self, file_paths, conversion_type):
        for file_path in file_paths:
            task_id = self.conversion_model.add_conversion(file_path, conversion_type)
            self.conversion_started.emit(task_id)
            
            output_dir = self._get_output_directory(file_path, conversion_type)
            processor = PDFProcessor([file_path], output_dir, self._get_operation(conversion_type))
            
            processor.progress_changed.connect(lambda progress, tid=task_id: self._update_progress(tid, progress))
            processor.log_changed.connect(lambda message, tid=task_id: self._update_log(tid, message))
            processor.process_completed.connect(lambda tid=task_id: self._complete_conversion(tid))
            
            self.active_conversions[task_id] = processor
            processor.start()

    def _get_output_directory(self, file_path, conversion_type):
        base_output_dir = self.settings_model.get('output_directory', os.path.dirname(file_path))
        return os.path.join(base_output_dir, f"Converted_{conversion_type.name}")

    def _get_operation(self, conversion_type):
        operations = {
            ConversionType.PDF_TO_DOCX: 'convert',
            ConversionType.PDF_TO_IMAGE: 'pdf_to_image',
            ConversionType.IMAGE_TO_PDF: 'image_to_pdf',
            ConversionType.TEXT_EXTRACTION: 'extract_text'
        }
        return operations.get(conversion_type, 'convert')

    def _update_progress(self, task_id, progress):
        self.conversion_model.update_conversion(task_id, progress=progress)
        self.conversion_progress.emit(task_id, progress)

    def _update_log(self, task_id, message):
        # Aktualisiere das Log in der ConversionModel
        self.conversion_model.add_log_entry(task_id, message)

        # Emittiere ein Signal für die UI, um das Log zu aktualisieren
        self.log_updated.emit(task_id, message)

        # Optional: Schreibe das Log in eine Datei
        log_file_path = self._get_log_file_path(task_id)
        with open(log_file_path, 'a', encoding='utf-8') as log_file:
            log_file.write(f"{message}\n")

    def _get_log_file_path(self, task_id):
        # Erstelle einen Ordner für Logs, falls er nicht existiert
        log_dir = os.path.join(self.settings_model.get('output_directory', ''), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        # Erstelle einen Dateinamen basierend auf der task_id
        return os.path.join(log_dir, f"conversion_{task_id}.log")
    
    def add_log_entry(self, task_id, message):
        conversion = self.conversions.get(task_id)
        if conversion:
            if 'log' not in conversion:
                conversion['log'] = []
            conversion['log'].append(message)

    def _complete_conversion(self, task_id):
        conversion = self.conversion_model.get_conversion(task_id)
        if conversion:
            if conversion['progress'] == 100:
                self.conversion_model.update_conversion(task_id, status=ConversionStatus.COMPLETED)
                self.conversion_completed.emit(task_id)
            else:
                error_message = "Konvertierung unvollständig"
                self.conversion_model.update_conversion(task_id, status=ConversionStatus.FAILED, error_message=error_message)
                self.conversion_failed.emit(task_id, error_message)
        
        if task_id in self.active_conversions:
            del self.active_conversions[task_id]

    def cancel_conversion(self, task_id):
        if task_id in self.active_conversions:
            self.active_conversions[task_id].stop()
            self.conversion_model.update_conversion(task_id, status=ConversionStatus.CANCELED)
            del self.active_conversions[task_id]