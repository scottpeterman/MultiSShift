# Fetch the existing Fusion style
from PyQt6 import QtWidgets, QtGui

def set_theme_green(app):
    # Fetch the existing Fusion style
        fusion = QtWidgets.QStyleFactory.create('Fusion')

        # Create a new palette using the Fusion palette as a base
        palette = QtGui.QPalette(fusion.standardPalette())

        # Define your green color
        green = QtGui.QColor('#376b34')

        # Set lighter color for the main interface elements (which was previously darker)
        palette.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor(35, 35, 35))  # Lighter background color

        # Set darker color for the TreeWidget background (which was previously lighter)
        palette.setColor(QtGui.QPalette.ColorRole.Base, QtGui.QColor(53, 53, 53))  # Darker element background

        palette.setColor(QtGui.QPalette.ColorRole.Button, QtGui.QColor(53, 53, 53))  # Button color

        # Set the bright text color for better readability
        bright_text_color = QtGui.QColor('#e0e0e0')  # Light gray for text

        palette.setColor(QtGui.QPalette.ColorRole.WindowText, bright_text_color)  # Bright text color for window titles
        palette.setColor(QtGui.QPalette.ColorRole.ButtonText, bright_text_color)  # Bright text for buttons
        palette.setColor(QtGui.QPalette.ColorRole.Text, bright_text_color)  # Bright text for general use
        palette.setColor(QtGui.QPalette.ColorRole.Highlight, green)  # Highlight color for selected items
        palette.setColor(QtGui.QPalette.ColorRole.HighlightedText, bright_text_color)  # Bright text for highlighted items

            # Set bright text color for inactive window text (if needed)
        palette.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.WindowText, bright_text_color)

        # Set the modified palette back to the application
        app.setPalette(palette)


        app.setStyle(fusion)

        # Set the Fusion style

def set_theme_orange(app):
    fusion = QtWidgets.QStyleFactory.create('Fusion')
    palette = QtGui.QPalette(fusion.standardPalette())

    # Define the orange color
    orange = QtGui.QColor('#b3721d')

    # Set the palette colors
    palette.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor(53, 53, 53))  # Dark background color
    palette.setColor(QtGui.QPalette.ColorRole.Base, QtGui.QColor(35, 35, 35))  # Darker element background
    palette.setColor(QtGui.QPalette.ColorRole.Button, QtGui.QColor(53, 53, 53))  # Button color

    # Set the bright text color for better readability
    bright_text_color = QtGui.QColor('#e0e0e0')  # Light gray for text

    # Use orange for highlights and buttons
    palette.setColor(QtGui.QPalette.ColorRole.Highlight, orange)
    palette.setColor(QtGui.QPalette.ColorRole.ButtonText, bright_text_color)  # Bright text for buttons
    palette.setColor(QtGui.QPalette.ColorRole.WindowText, bright_text_color)  # Bright text for window titles
    palette.setColor(QtGui.QPalette.ColorRole.Text, bright_text_color)  # Bright text for general use
    palette.setColor(QtGui.QPalette.ColorRole.HighlightedText, QtGui.QColor(255, 255, 255))  # White text for highlighted items

    # Set bright text color for inactive window text
    palette.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.WindowText, bright_text_color)

    app.setPalette(palette)
    app.setStyle(fusion)
