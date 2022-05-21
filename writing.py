from pyfiglet import Figlet
from plumbum import colors, cli 
import questionary
import yaml, ruamel.yaml

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

#(1) buy the journal
def create_journal():
    #prompt user to name journal
    global author, path
    author = ruamel.yaml.scalarstring.DoubleQuotedScalarString(questionary.text("What is your name?").ask())
    
    #find the place to save the journal
    path = ruamel.yaml.scalarstring.DoubleQuotedScalarString(questionary.text("What is the name of your journal?").ask())

    my_dict = dict(author=author, path=path)
    yaml = ruamel.yaml.YAML()

    with open('config.yml', 'w') as outfile:
        yaml.dump(my_dict, outfile)

    #making the directory
    try:
        os.makedirs(path)
    except OSError:
        print(f"Creating the directory {path} has failed.")
    else:
        print(f"Successfully created {author}'s journal at {path}")


class GJournal(cli.Application):
    VERSION = "0.0"

    def main(self):
        global path,author
        load_path_author()
        print_banner("Gratitude Journal")
        choice = questionary.select(
        "What would you like to do",
        choices=[
            'Journal',
            'Read Entries',
            'Quit'
        ]).ask()
        if choice == 'Journal':
            if path == "":
                create_journal()
            else:
                print("open_journal()")
        elif choice == 'Read Entries':
            print("read_entries()")
        elif choice == 'Quit':
            print("Goodbye, have a lovely day!")

if __name__ == "__main__":
    GJournal()