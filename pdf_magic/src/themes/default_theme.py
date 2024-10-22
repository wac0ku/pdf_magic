class DefaultTheme:
    name = "Default"
    
    # Farben
    primary_color = "#007bff"
    secondary_color = "#6c757d"
    background_color = "#ffffff"
    text_color = "#000000"
    
    # Schriftarten
    font_family = "Arial, sans-serif"
    font_size = "12px"
    
    # Styles
    button_style = f"""
        QPushButton {{
            background-color: {primary_color};
            color: white;
            border: none;
            padding: 5px 10px;
            border-radius: 3px;
        }}
        QPushButton:hover {{
            background-color: #0056b3;
        }}
    """
    
    progress_bar_style = f"""
        QProgressBar {{
            border: 2px solid {secondary_color};
            border-radius: 5px;
            text-align: center;
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