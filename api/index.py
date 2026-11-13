import os
import sys

# Ensure project root is in sys.path so app and its dependencies can be imported
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from app import app

# Export the WSGI app for Vercel
app = app

