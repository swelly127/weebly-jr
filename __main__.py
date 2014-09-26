"""__main__ module

This is the module with the application code. Make sure that this module is
in a folder with the file controller.py (the primary controller class)

You should have the following subfolders

    Fonts
    Sounds        (sound effects for the game)
    Images
    Style      
    Javascript

Moving any of these folders or files will prevent the game from working properly"""

from kivy.app import App
from kivy.config import Config
import controller
import sys


class BreakoutApp(App):
    """Application class for Breakout.

    Extends the Kivy App class.  It integrates the .kv file with .py methods
    It is invoked at start-up and then never used again."""
    _controller = None # The controller class (held as field to prevent garbage collection)

    def build(self):
        """Creates the new Window and instantiates the game controller."""""
        Config.set('graphics', 'width', str(controller.GAME_WIDTH))
        Config.set('graphics', 'height', str(controller.GAME_HEIGHT))
        self._controller = controller.Breakout()
        return self._controller.view


def fix_bricks(args):
    """Changes constants BRICKS_IN_ROW, BRICK_ROWS, and BRICK_WIDTH to match command line arguments

    If args does not have exactly three elements, or the last two elements do not represent
    positive integers, DON'T DO ANYTHING.

    If args has exactly three elements, and the last two represent positive integers,
    do the following:
    Convert the second element to an int and store it in BRICKS_IN_ROW.
    Convert the third element to an int and store it in BRICK_ROWS.
    Recompute BRICK_WIDTH using the formula given in its declaration in module controller.

    To reset the above three 'constants', note that you can treat global variables in a module
    just like they were fields.  Simply use the command

        controller.BRICKS_IN_ROW = new_value

    Precondition: args is a list of strings."""
    try:
        if int(args[1])<25:
            controller.BRICKS_IN_ROW = int(args[1])
            controller.BRICK_WIDTH = float(controller.GAME_WIDTH)/ int(args[1]) - controller.BRICK_SEP_H
        if int(args[2])<25:
            controller.BRICK_ROWS = int(args[2])
        else:
            pass
    except:
        pass



# Application code
if __name__ == '__main__':
    fix_bricks(sys.argv)
    BreakoutApp().run()
