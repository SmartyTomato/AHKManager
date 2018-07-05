import sys
import traceback

from app.application import Application

try:
    Application()
except Exception as error:
    print("Unexpected error:", sys.exc_info()[0])
    print(traceback.format_exc())
