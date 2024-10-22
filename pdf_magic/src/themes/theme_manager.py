from .default_theme import DefaultTheme
from .dark_theme import DarkTheme

class ThemeManager:
    def __init__(self):
        self.themes = {
            "default": DefaultTheme,
            "dark": DarkTheme
         }
    
    def get_theme(self, theme_name):
        return self.themes.get(theme_name)