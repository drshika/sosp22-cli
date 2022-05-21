from datetime import datetime
import os, fnmatch
import textwrap
import questionary
from questionary import prompt
from pyfiglet import Figlet
from plumbum import colors
import yaml, ruamel.yaml

with open("config.yaml", "r") as yamlfile:
    data = yaml.safe_load(yamlfile)
author = data['author']
path = data['path']

#(1) buy the journal
def create_journal():
    #prompt user to name journal
    global author, path
    author = ruamel.yaml.scalarstring.DoubleQuotedScalarString(questionary.text("What is your name?").ask())
    
    #find the place to save the journal
    path = ruamel.yaml.scalarstring.DoubleQuotedScalarString(questionary.text().ask("What is the absolute path of your journal?"))

    my_dict = dict(author=author, path=path)
    yaml = ruamel.yaml.YAML()

    with open('data.yml', 'w') as outfile:
        yaml.dump(my_dict, outfile)

    #making the directory
    try:
        os.makedirs(path)
    except OSError:
        print(f"Creating the directory {path} has failed.")
    else:
        print(f"Successfully created {author}'s journal at {path}")

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

def main():
    global path,author
    greeting = "Gratitude Journal"
    with colors['LIGHT_SEA_GREEN']:
        print(Figlet(font='slant').renderText(greeting))
    choice = questionary.select(
    "What would you like to do",
    choices=[
        'Journal',
        'Read Entries',
        'Quit'
    ]).ask()
    if choice == 'Journal':
        if path == "": #fix this part later
            create_journal()
        open_journal()
    elif choice == 'Read Entries':
        read_entries()
    elif choice == 'Quit':
        print("Goodbye, have a lovely day!")
main()