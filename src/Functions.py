import os
import datetime
import sys
import json
import struct
from pyexcel_ods3 import get_data, save_data
from collections import OrderedDict

# --- Config ---
ODS_PATH = "C:\\Users\\olivi\\Documents\\MeineAblage.ods"
SHEET_NAME = "Sheet1"

def append_row_to_ods(text, second_value, date_str, url, checkbox_state=False, image_src=""):
    """
    Append a row to the ODS spreadsheet with the given values.
    Columns: text, second_value, date_str, url, checkbox_state, image_src
    """
    if os.path.exists(ODS_PATH):
        data = get_data(ODS_PATH)
        sheet = data.get(SHEET_NAME, [])
    else:
        sheet = []
    sheet.append([text, second_value, date_str, url, "1" if checkbox_state else "0", image_src])
    data = OrderedDict()
    data[SHEET_NAME] = sheet
    save_data(ODS_PATH, data)

def read_native_message():
    """Read a message from Chrome native messaging (raw binary)."""
    raw_length = sys.stdin.buffer.read(4)
    if len(raw_length) < 4:
        return None
    message_length = struct.unpack('=I', raw_length)[0]
    message = sys.stdin.buffer.read(message_length)
    return json.loads(message.decode('utf-8'))

def send_native_message(obj):
    """Send a message to Chrome native messaging (raw binary)."""
    response_bytes = json.dumps(obj).encode('utf-8')
    sys.stdout.buffer.write(struct.pack('=I', len(response_bytes)))
    sys.stdout.buffer.write(response_bytes)
    sys.stdout.buffer.flush()

def log_debug(message):
    with open("debug.log", "a", encoding="utf-8") as f:
        f.write(f"DEBUG: {message}\n")
