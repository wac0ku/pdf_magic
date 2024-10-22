class DarkTheme:
    name = "Dark"
    
    # Farben
    primary_color = "#bb86fc"
    secondary_color = "#03dac6"
    background_color = "#121212"
    text_color = "#ffffff"
    
    # Schriftarten
    font_family = "Arial, sans-serif"
    font_size = "12px"
    
    # Styles
    button_style = f"""
        QPushButton {{
            background-color: {primary_color};
            color: {background_color};
            border: none;
            padding: 5px 10px;
            border-radius: 3px;
        }}
        QPushButton:hover {{
            background-color: #9965f4;
        }}
    """
    
    progress_bar_style = f"""
        QProgressBar {{
            border: 2px solid {secondary_color};
            border-radius: 5px;
            text-align: center;
            color: {text_color};
        }}
        QProgressBar::chunk {{
            background-color: {primary_color};
            width: 10px;
        }}
    """
    
    text_edit_style = f"""
        QTextEdit {{
            background-color: {background_color};
            color: {text_color};
            border: 1px solid {secondary_color};
            border-radius: 3px;
        }}
    """