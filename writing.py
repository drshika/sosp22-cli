import os, fnmatch
from datetime import datetime
from pyfiglet import Figlet
from plumbum import colors, cli 
import questionary
from questionary import prompt
import yaml, ruamel.yaml
from plumbum.cmd import git
import textwrap

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

    os.chdir(path)
    add_page()

def add_content(title):
    timestamp = str(datetime.now())
    with open(title, 'a') as entry:
        writing = questionary.text("What are you grateful for?").ask()
        prettier_writing = textwrap.fill(writing) + "\n"
        entry.write(prettier_writing)
    git('add', title)
    git('commit', '-m', timestamp + ' make update to daily entry')
    git('push')

#flip to the right page
def add_page():
    entry_name = str(datetime.today().strftime('%Y-%m-%d'))+ ".txt"
    open(entry_name, 'x')
    print("Created Entry" + entry_name)
    add_content(entry_name)

#open the journal
def open_journal():
    today_entry = str(datetime.today().strftime('%Y-%m-%d')) + ".txt"

    os.chdir(path)
    journal_list = os.listdir()

    #looping through the list of journals to check if there is an entry for today
    if not journal_list:
        add_page()
    for journal in journal_list:
        if fnmatch.fnmatch(journal, today_entry):
            add_content(today_entry)
        else:
            add_page()

# flip through past pages
def read_entries():
    os.chdir(path)
    journal_list = os.listdir()

    question = [{
        "type": "select",
        "name": "select_entry",
        "message": "Choose an entry to read",
        "choices": journal_list
    },]
    entry = prompt(question)['select_entry']
    with open(entry, 'r') as e:
        print(e.read())

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
                open_journal()
        elif choice == 'Read Entries':
            read_entries()
        elif choice == 'Quit':
            print("Goodbye, have a lovely day!")

if __name__ == "__main__":
    GJournal()