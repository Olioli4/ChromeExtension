import subprocess
import struct
import json
import sys

# Prepare the message as Chrome would send it
message = {
    "text": "Simulated input from Chrome",
    "url": "https://example.com",
    "imageSrc": "https://example.com/image.png"
}
encoded = json.dumps(message).encode("utf-8")
packed_len = struct.pack("=I", len(encoded))

# Start main.py as a subprocess
proc = subprocess.Popen(
    [sys.executable, "src/main.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

# Send the message (length prefix + JSON)
proc.stdin.write(packed_len)
proc.stdin.write(encoded)
proc.stdin.flush()

# Read the response (length prefix + JSON)
raw_len = proc.stdout.read(4)
if len(raw_len) < 4:
    print("No response or error from main.py")
    sys.exit(1)
resp_len = struct.unpack("=I", raw_len)[0]
resp = proc.stdout.read(resp_len)
print("Response from main.py:", resp.decode("utf-8"))

# Print any errors
stderr = proc.stderr.read()
if stderr:
    print("main.py stderr:", stderr.decode("utf-8"))