from .logger import logger

class ErrorHandler:
    @staticmethod
    def handle_error(error, context=""):
        error_message = f"Error in {context}: {str(error)}"
        logger.error(error_message)
        # Hier können Sie zusätzliche Fehlerbehandlung implementieren,
        # z.B. einen Fehlerdialog anzeigen oder eine Benachrichtigung senden

    @staticmethod
    def log_warning(message, context=""):
        warning_message = f"Warning in {context}: {message}"
        logger.warning(warning_message)

    @staticmethod
    def log_info(message, context=""):
        info_message = f"Info in {context}: {message}"
        logger.info(info_message)