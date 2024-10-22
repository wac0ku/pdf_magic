# Logger for debugging

import logging
import os

def setup_logger():
    # Erstellen Sie einen Logger
    logger = logging.getLogger('pdf_magic')
    logger.setLevel(logging.DEBUG)

    # Erstellen Sie einen FileHandler
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    file_handler = logging.FileHandler(os.path.join(log_dir, 'pdf_magic.log'))
    file_handler.setLevel(logging.DEBUG)

    # Erstellen Sie einen StreamHandler für die Konsolenausgabe
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Erstellen Sie ein Formatter und fügen Sie es den Handlern hinzu
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Fügen Sie die Handler zum Logger hinzu
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Erstellen Sie eine globale Logger-Instanz
logger = setup_logger()