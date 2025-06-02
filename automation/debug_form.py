import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from form_widgets import inputbox
from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    # Show the form with a sample prompt for debugging
    result = inputbox("Debug Prompt", "Debug Title", "Default debug text")
    print("Form result:", result)
    sys.exit()
