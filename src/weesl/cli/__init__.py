from weesl.core import Weesl
import argparse

class CLI:

    def __init__(self) -> None:
        parser = argparse.ArgumentParser(
            prog = "weesl",
            description = "scripting utility for defining python scripts in yaml",
        )
        parser.add_argument("filename")
        self.args = parser.parse_args()

    def run_file(self):
        wsl = Weesl.setup(self.args.filename)
        wsl.run()

def run():
    app = CLI()
    app.run_file()

