from source.configure import configs

import PyQt5
import tkinter
import logging


def create_window(width=configs.window.default_height,
                  height=configs.window.default_height):
    """
    Create new window with defined width and height
    :param width: the width of the window
    :param height: the height of the window
    :return: created window header
    """
    logging.info("Creating window width = {width}, height = {height}"
                 .format(width=width, height=height))
    window = tkinter.Tk()
    window.geometry("{width}x{height}".format(width=width, height=height))

    return window
