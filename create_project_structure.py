import os

def create_directory_structure(base_path):
    structure = {
        'src': {
            'ui': ['__init__.py', 'main_window.py', 'docking_system.py', 'menu_bar.py', 'toolbar.py', 'tab_system.py', 'settings_dialog.py', 'file_preview.py', 'custom_widgets.py'],
            'models': ['__init__.py', 'conversion_model.py', 'settings_model.py', 'file_model.py'],
            'controllers': ['__init__.py', 'main_controller.py', 'conversion_controller.py', 'settings_controller.py'],
            'utils': ['__init__.py', 'pdf_processor.py', 'file_handler.py', 'logger.py', 'error_handler.py'],
            'workers': ['__init__.py', 'conversion_worker.py'],
            'themes': ['__init__.py', 'default_theme.py', 'dark_theme.py'],
            'i18n': ['__init__.py', 'en.json', 'de.json'],
            'main.py': None
        },
        'tests': ['__init__.py', 'test_pdf_processor.py', 'test_file_handler.py', 'test_conversion_model.py'],
        'docs': ['user_manual.md', 'developer_guide.md'],
        'resources': {
            'icons': [],
            'styles': []
        },
        'plugins': ['__init__.py'],
        'config': ['settings.json'],
        'requirements.txt': None,
        'setup.py': None,
        'README.md': None
    }

    def create_structure(current_path, structure):
        for key, value in structure.items():
            path = os.path.join(current_path, key)
            if isinstance(value, dict):
                os.makedirs(path, exist_ok=True)
                create_structure(path, value)
            elif isinstance(value, list):
                os.makedirs(path, exist_ok=True)
                for item in value:
                    open(os.path.join(path, item), 'a').close()
            elif value is None:
                open(path, 'a').close()

    create_structure(base_path, structure)
    print(f"Verzeichnisstruktur wurde erstellt in: {base_path}")

if __name__ == "__main__":
    base_path = os.path.join(os.getcwd(), "pdf_magic")
    create_directory_structure(base_path)