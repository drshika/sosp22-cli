import os, fnmatch
from datetime import datetime
from pyfiglet import Figlet
from plumbum import colors, cli 
import questionary
from questionary import prompt
import yaml, ruamel.yaml
from rich.progress import Progress
from plumbum.cmd import git
import textwrap
import time

def print_banner(text):
    with colors['LIGHT_SEA_GREEN']:
        print(Figlet(font='slant').renderText(text))

author = ""
journal_name = ""

# loads a journal yaml config file, creating it if missing
def load_config(filename):
    global author, journal_name
    if not os.path.exists(filename):
        save_config(filename, {
            "author": '',
            "journal_name": ''
        })

    with open(filename, "r") as file:
        data = yaml.safe_load(file)
    author = data['author']
    journal_name = data['journal_name']

# save the config to a file
def save_config(filename, config):
    yaml = ruamel.yaml.YAML()

    with open(filename, "w") as file:
            yaml.dump(config, file)

def init_folder(folder_name):
    #making the directory
    try:
        os.makedirs(folder_name)
    except OSError:
        print(f"Creating the directory {folder_name} has failed.")

    os.chdir(journal_name)
    add_page()

#(1) buy the journal
def create_journal():
    #prompt user to name journal
    global author, journal_name
    author = ruamel.yaml.scalarstring.DoubleQuotedScalarString(questionary.text("What is your name?").ask())
    
    #find the place to save the journal
    journal_name = ruamel.yaml.scalarstring.DoubleQuotedScalarString(author + "-Journal")

    my_dict = dict(author=author, journal_name=journal_name)

    save_config("config.yml", my_dict)
    init_folder(journal_name)

def add_content(title):
    with open(title, 'a') as entry:
        writing = questionary.text("What are you grateful for?").ask()
        prettier_writing = textwrap.fill(writing) + "\n"
        entry.write(prettier_writing)

#flip to the right page
def add_page():
    entry_name = str(datetime.today().strftime('%Y-%m-%d'))+ ".txt"
    open(entry_name, 'x')
    print("Created Entry" + entry_name)
    add_content(entry_name)

#open the journal
def open_journal():
    entry_name = str(datetime.today().strftime('%Y-%m-%d')) + ".txt"

    os.chdir(journal_name)
    journal_list = os.listdir()

    #looping through the list of journals to check if there is an entry for today
    if not journal_list:
        add_page()
    for journal in journal_list:
        if fnmatch.fnmatch(journal, entry_name):
            add_content(entry_name)
        else:
            add_page()

# flip through past pages
def read_entries():
    global journal_name
    os.chdir(journal_name)
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

# Code credit to harsh183
def display_push_progress():
    # Note: Actually getting progress from git is surprisingly non-trivial
    # So I've hard coded an example for now, but in real code, emit things as they happen
    with Progress() as progress:
        push_progress = progress.add_task("Pushing files :partying_face:")

        for i in range(100):
            progress.update(push_progress, advance=1)
            time.sleep(0.05)

class GJournal(cli.Application):
    VERSION = "0.0"

    push = cli.Flag(['p', 'push'], help="Commits and pushes the added files as well")

    def main(self):
        global journal_name,author,push

        load_config("config.yml")
        print_banner("Gratitude Journal")
    
        choice = questionary.select(
        "What would you like to do",
        choices=[
            'Journal',
            'Read Entries',
            'Quit'
        ]).ask()
        if choice == 'Journal':
            if journal_name == "":
                create_journal()
            else:
                open_journal()
        elif choice == 'Read Entries':
            read_entries()
        elif choice == 'Quit':
            print("Goodbye, have a lovely day!")

        timestamp = str(datetime.now())
        entry_name = str(datetime.today().strftime('%Y-%m-%d')) + ".txt"

        if self.push:
            git('add', entry_name)
            git('commit', '-m', timestamp + ' make update to daily entry')
            git('push')
            display_push_progress()

if __name__ == "__main__":
    GJournal()