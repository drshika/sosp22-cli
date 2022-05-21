from pyfiglet import Figlet
from plumbum import colors, cli 

def print_banner(text):
    with colors['LIGHT_SEA_GREEN']:
        print(Figlet(font='slant').renderText(text))

class GJournal(cli.Application):
    VERSION = "0.0"

    def main(self):
        print_banner("Gratitude Journal")

if __name__ == "__main__":
    GJournal()