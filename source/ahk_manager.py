import sys
import traceback

from app.application.application import Application


def main():
    try:
        Application()
    except Exception as error:
        print("Unexpected error:", sys.exc_info()[0])
        print(error)
        print(traceback.format_exc())


if __name__ == '__main__':
    main()
