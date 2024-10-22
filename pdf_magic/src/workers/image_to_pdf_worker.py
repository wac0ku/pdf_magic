import os
from PyQt5.QtCore import QRunnable, pyqtSlot
from PyQt5.QtCore import QObject, pyqtSignal
from PIL import Image
from utils.error_handler import ErrorHandler

class ImageToPDFWorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(str)
    progress = pyqtSignal(int)
    result = pyqtSignal(str)  # Emits output PDF file path

class ImageToPDFWorker(QRunnable):
    def __init__(self, image_paths, output_dir):
        super(ImageToPDFWorker, self).__init__()
        self.image_paths = image_paths
        self.output_dir = output_dir
        self.signals = ImageToPDFWorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            images = []
            for i, image_path in enumerate(self.image_paths):
                image = Image.open(image_path)
                if image.mode == 'RGBA':
                    image = image.convert('RGB')
                images.append(image)
                progress = int((i + 1) / len(self.image_paths) * 100)
                self.signals.progress.emit(progress)

            # Create output filename
            base_name = os.path.basename(self.image_paths[0]).split('.')[0]
            output_path = os.path.join(self.output_dir, f"{base_name}.pdf")

            # Save images to PDF
            images[0].save(output_path, "PDF", resolution=100.0, save_all=True, append_images=images[1:])

            self.signals.result.emit(output_path)
            self.signals.finished.emit()

        except Exception as e:
            error_message = f"Error converting images to PDF: {str(e)}"
            ErrorHandler.handle_error(error_message)
            self.signals.error.emit(error_message)