# main.py
# Native messaging host and PyQt6 dialog for writing to ODS spreadsheet

from Functions import append_row_to_ods, read_native_message, send_native_message, log_debug
from form_widget import inputbox
import os
import datetime
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# --- Config ---
ODS_PATH = "C:\\Users\\olivi\\Documents\\MeineAblage.ods"
SHEET_NAME = "Sheet1"

# --- Main Execution ---
if __name__ == "__main__":
    log_debug("Script starting...")
    msg = read_native_message()
    log_debug(f"Received message: {msg}")
    if msg and 'text' in msg:
        text = msg['text'] if msg['text'] else "Fill"
        url = msg.get('url', '')
        image_src = msg.get('imageSrc', '')  # Extract the image source
        log_debug(f"Using text from Chrome: {text}")
        log_debug(f"Image source: {image_src}")
    else:
        log_debug("No Chrome message, showing inputbox for first column")
        text = "Fill"
        url = msg.get('url', '') if msg else ''
        image_src = ""  # No image source for manual input
    log_debug("Showing inputbox for second column")
    zweiter_text, zweiter_checked, new_edit_value = inputbox("Folgen", "", default_long_text=text)
    zweiter_wert = zweiter_text if zweiter_text else ""
    log_debug(f"Second value: {zweiter_wert}, Checkbox: {zweiter_checked}, New edit: {new_edit_value}")
    date_str = datetime.datetime.now().strftime('%d.%m.%Y')
    log_debug(f"Saving to ODS: text={text}, second={zweiter_wert}, date={date_str}, url={url}, checkbox={zweiter_checked}, image_src={image_src}")
    append_row_to_ods(new_edit_value, zweiter_wert, date_str, url, zweiter_checked, image_src)
    log_debug("Successfully saved to ODS")
    if msg:
        log_debug("Sending response to Chrome")
        send_native_message({"result": "OK"})
        log_debug("Response sent successfully")
    else:
        print("Gespeichert!")
    log_debug("Script completed successfully")
    app = QApplication.instance()
    if app:
        app.quit()