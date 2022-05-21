from pyfiglet import Figlet
from plumbum import colors, cli 
import questionary
import yaml

def print_banner(text):
    with colors['LIGHT_SEA_GREEN']:
        print(Figlet(font='slant').renderText(text))

author = ""
path = ""

def load_path_author():
    global author, path
    with open("config.yml", "r") as yamlfile:
        data = yaml.safe_load(yamlfile)
    author = data['author']
    path = data['path']


class GJournal(cli.Application):
    VERSION = "0.0"

    def main(self):
        global path,author
        load_path_author()
        print_banner("Gratitude Journal")

if __name__ == "__main__":
    GJournal()