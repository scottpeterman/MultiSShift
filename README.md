
# MultiSSHift Terminal

## Overview
`MultiSSHift Terminal` is an advanced SSH management tool designed for network professionals who require a robust and efficient way to manage multiple SSH sessions. Built with PyQt6 and integrating a web-based terminal interface, it offers a comprehensive solution for managing network devices and servers.


## Key Features

<div align="center">
  <img src="https://raw.githubusercontent.com/scottpeterman/MultiSShift/main/screen-shots/terminal1.png" alt="screen 1" width="400px">
  <hr>
  <img src="https://raw.githubusercontent.com/scottpeterman/MultiSShift/main/screen-shots/terminal12.png" alt="screen 2" width="400px">
</div>


- **Session Management**: Effortlessly manage multiple SSH sessions with an intuitive tree-view interface. Organize and access your sessions with ease.
- **Embedded Web View**: Integrated web view for seamless interaction with web-based management tools and documentation.
- **Versatile Tools**: Includes built-in features such as a log viewer, file editor, and ad-hoc connection dialog, providing a one-stop solution for various network management tasks.
- **Themes**: Choose between light standard Qt and dark emerald themes for optimal user experience. Personalize your workspace according to your preference.
- **Dynamic Toolbar**: Quick access toolbar with essential shortcuts, enhancing your workflow efficiency.
- **Centralized Settings Management**: Manage credentials and application settings in a centralized manner, ensuring a streamlined and consistent configuration.

## Technical Highlights
- Built with **PyQt6**, providing a modern and responsive user interface.
- Utilizes **YAML** for session and settings management, offering a human-readable and easily configurable format.
- Implements a sophisticated logging, error handling and notification system for reliability and ease of debugging.
- Integrates seamlessly with **QWebEngineView** for embedded browser functionality.
- Supports custom JavaScript and CSS for a personalized user experience.

## Installation and Setup
* To do

## Usage
* To do

## Package Distribution

```python
# Create a source distribution and a wheel
python setup.py sdist bdist_wheel

# Set up a new virtual environment
python -m venv test_env

# Activate the virtual environment
source test_env/bin/activate  # On Linux/Mac
test_env\Scripts\activate     # On Windows

# Install the wheel
pip install dist/uglypty-0.1-py3-none-any.whl

# Test your script
python or pythonw -m uglypty

# Use `twine` to upload your package to PyPI: 
twine upload dist/* 