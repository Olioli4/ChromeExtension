import os
import datetime
import sys
import json
import struct
from pyexcel_ods3 import get_data, save_data
from collections import OrderedDict
from PyQt6.QtWidgets import (QApplication, QDialog, QVBoxLayout, QHBoxLayout, 
                            QLabel, QLineEdit, QPushButton, QTextEdit, QFrame, QCheckBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPalette, QColor, QPainter, QBrush
from toggle_image_widget import ToggleImageWidget

ODS_PATH = "C:\\Users\\olivi\\Documents\\MeineAblage.ods"
SHEET_NAME = "Sheet1"

def inputbox(prompt, title="Eingabe", default_long_text=""):
    app = QApplication.instance()
    app_created = False
    if not app:
        app = QApplication(sys.argv)
        app_created = True

    # Subclass QDialog to override paintEvent for opaque rounded background
    class RoundedDialog(QDialog):
        def paintEvent(self, event):
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            rect = self.rect()
            color = QColor("#192a56")  # main background
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(rect, 24, 24)
            super().paintEvent(event)

    dialog = RoundedDialog()
    # Remove title bar and window frame, keep always-on-top
    dialog.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
    dialog.setFixedSize(400, 400)  # Increased height for new edit box
    # Enable window transparency for rounded corners to show
    dialog.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    # Set modern dark blue style and font
    darkblue = "#192a56"  # main background
    accent = "#233e70"    # accent blue
    textcolor = "#f5f6fa" # light text
    bordercolor = "#ff9800" # orange highlight
    bordercolor_unfocused = "#0099cc" # blue for unfocused
    style = f"""
        QDialog {{
            /* background: {darkblue}; removed, now painted in paintEvent */
            border-radius: 24px;
        }}
        QLabel, QLineEdit, QCheckBox, QPushButton {{
            color: {textcolor};
            font-size: 24px;
            font-family: 'Segoe UI', 'Arial', sans-serif;
        }}
        QLineEdit, QCheckBox {{
            background: {accent};
            border: 2px solid {bordercolor_unfocused};
            border-radius: 8px;
            padding: 8px 12px;
        }}
        QLineEdit:focus, QCheckBox:focus {{
            border: 2px solid {bordercolor};
            background: #233e70;
        }}
        QPushButton {{
            background: {accent};
            border: 2px solid {bordercolor};
            border-radius: 8px;
            padding: 8px 24px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background: {bordercolor};
            color: {darkblue};
        }}
    """
    dialog.setStyleSheet(style)

    # Set font for all widgets except checkbox
    font = QFont('Segoe UI', 24)
    dialog.setFont(font)
    
    # Set font for widgets individually, except checkbox
    for widget in dialog.findChildren((QLabel, QLineEdit, QPushButton)):
        widget.setFont(font)
    # Do not set font for QCheckBox here

    # Main layout
    layout = QVBoxLayout()
    layout.setSpacing(20)  # Increased spacing between elements
    layout.setContentsMargins(10, 15, 10, 15)  # Increased vertical margins
    dialog.setLayout(layout)
    
    # Title label
    title_label = QLabel(prompt)
    title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title_label.setFont(font)
    layout.addWidget(title_label)
    
    # New edit box under prompt
    new_edit = QLineEdit()
    new_edit.setPlaceholderText("Enter additional text...")
    new_edit.setFont(font)
    new_edit.setFixedHeight(64)
    new_edit.setText(default_long_text)  # Set default text
    layout.addWidget(new_edit)
    
    # Add stretch before form_frame for vertical centering
    layout.addStretch()

    # Container frame for form elements with extra spacing
    form_frame = QFrame()
    form_frame.setFixedWidth(400)  # Set a fixed width for better centering
    form_layout = QVBoxLayout()
    form_layout.setSpacing(24)
    form_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    form_frame.setLayout(form_layout)

    # Horizontal layout for input and checkbox
    input_layout = QHBoxLayout()
    input_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    # Add stretch before
    input_layout.addStretch(1)
    # 5-character edit field
    char_edit = QLineEdit()
    char_edit.setMaxLength(5)
    char_edit.setFixedWidth(120)
    char_edit.setFixedHeight(64)
    char_edit.setFont(font)
    input_layout.addWidget(char_edit)
    # Add spacing between edit and checkbox
    input_layout.addSpacing(32)
    # Add custom toggle widget using icons from Assets
    toggle_widget = ToggleImageWidget()
    toggle_widget.setFixedSize(64, 64)
    input_layout.addWidget(toggle_widget)
    # Add stretch after
    input_layout.addStretch(1)

    form_layout.addLayout(input_layout)
    layout.addWidget(form_frame)

    # Add stretch after form_frame for vertical centering
    layout.addStretch()

    # Button layout
    button_layout = QHBoxLayout()
    button_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)  # Center the button horizontally
    ok_button = QPushButton("OK")
    ok_button.setFont(font)
    ok_button.setFixedHeight(72)
    ok_button.setFixedWidth(220)
    button_layout.addWidget(ok_button)
    layout.addLayout(button_layout)

    # Connect button
    ok_button.clicked.connect(dialog.accept)
    
    # Center the dialog
    screen = app.primaryScreen().geometry()
    dialog.resize(800, 600)
    dialog.move(
        (screen.width() - dialog.width()) // 2,
        (screen.height() - dialog.height()) // 2
    )

    # Set focus to the appropriate field
    if default_long_text == "Fill":
        new_edit.setFocus()
    else:
        char_edit.setFocus()
    # Execute dialog and get result
    text_result = ""
    check_result = False
    new_edit_result = ""
    if dialog.exec() == QDialog.DialogCode.Accepted:
        text_result = char_edit.text().strip()
        check_result = toggle_widget.checked
        new_edit_result = new_edit.text().strip()
    
    # Clean up dialog
    dialog.deleteLater()
    
    # Properly quit the app if we created it
    if app_created:
        QTimer.singleShot(0, app.quit)
    
    return text_result, check_result, new_edit_result

def append_row_to_ods(text, second_value, date_str, url, checkbox_state=False):
    # Read existing data
    if os.path.exists(ODS_PATH):
        data = get_data(ODS_PATH)
        sheet = data.get(SHEET_NAME, [])
    else:
        sheet = []

    # Append new row with URL as 4th column and checkbox as 5th
    sheet.append([text, second_value, date_str, url, "1" if checkbox_state else "0"])

    # Save back
    data = OrderedDict()
    data[SHEET_NAME] = sheet
    save_data(ODS_PATH, data)

if __name__ == "__main__":
    # Native messaging functions without error handling
    def read_native_message():
        print("DEBUG: Reading native message...")
        raw_length = sys.stdin.buffer.read(4)
        print(f"DEBUG: Read raw length: {len(raw_length)} bytes")
        message_length = struct.unpack('=I', raw_length)[0]
        print(f"DEBUG: Message length: {message_length}")
        message = sys.stdin.buffer.read(message_length)
        print(f"DEBUG: Raw message: {message}")
        return json.loads(message.decode('utf-8'))

    def send_native_message(obj):
        print("DEBUG: Sending response...")
        response_bytes = json.dumps(obj).encode('utf-8')
        print(f"DEBUG: Response bytes length: {len(response_bytes)}")
        sys.stdout.buffer.write(struct.pack('=I', len(response_bytes)))
        sys.stdout.buffer.write(response_bytes)
        sys.stdout.buffer.flush()
        print("DEBUG: Response sent and flushed")

    def log_debug(message):
        print(f"DEBUG: {message}")
        
    # Main execution without try/except
    log_debug("Script starting...")
    
    # Try to read from native messaging (Chrome)
    msg = read_native_message()
    log_debug(f"Received message: {msg}")
    
    if msg and 'text' in msg:
        if not msg['text']:
            text = "Fill"
        else:
            text = msg['text']
            log_debug(f"Using text from Chrome: {text}")
        url = msg.get('url', '')
    else:
        log_debug("No Chrome message, showing inputbox for first column")
        text = "Fill"
        url = msg.get('url', '')
       

    log_debug("Showing inputbox for second column")
    # Get both text and checkbox state for second column
    zweiter_text, zweiter_checked, new_edit_value = inputbox("Folgen", "", default_long_text=text)
    zweiter_wert = zweiter_text if zweiter_text else ""
    log_debug(f"Second value: {zweiter_wert}, Checkbox: {zweiter_checked}, New edit: {new_edit_value}")

    date_str = datetime.datetime.now().strftime('%d.%m.%Y')
    log_debug(f"Saving to ODS: text={text}, second={zweiter_wert}, date={date_str}, url={url}, checkbox={zweiter_checked}")
    
    append_row_to_ods(new_edit_value, zweiter_wert, date_str, url, zweiter_checked)
    log_debug("Successfully saved to ODS")

    # Send response back to Chrome
    if msg:
        log_debug("Sending response to Chrome")
        send_native_message({"result": "OK"})
        log_debug("Response sent successfully")
    else:
        print("Gespeichert!")
        
    log_debug("Script completed successfully")
    
    # Ensure Qt application exits properly
    app = QApplication.instance()
    if app:
        app.quit()