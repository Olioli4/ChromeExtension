import sys
import os

# Remove src/ from sys.path if present
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# ...existing code...