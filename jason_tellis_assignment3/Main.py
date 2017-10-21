import logging

from ImageClassifierEnvironment import ImageClassifierEnvironment


class Main:
    @staticmethod
    def main():
        """
        Entry point to the program
        """

        ice = ImageClassifierEnvironment()
        ice.percept()


logging.basicConfig(level=logging.INFO, format="%(message)s")
Main.main()
