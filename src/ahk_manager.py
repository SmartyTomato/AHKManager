import sys
import traceback

from src.app.application.application import Application


def main():
    try:
        app = Application()
        app.exec()
    except Exception as error:
        print("Unexpected error:", sys.exc_info()[0])
        print(error)
        print(traceback.format_exc())


if __name__ == '__main__':
    main()
