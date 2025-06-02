from PyQt6.QtWidgets import QApplication
from main import inputbox
import sys

if __name__ == "__main__":
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    # Show the form with a sample prompt
    result = inputbox("Test Prompt", "Test Title", "Default text")
    print("Form result:", result)
    sys.exit()
