from plumbum import cli 

class GJournal(cli.Application):
    VERSION = "0.0"

    def main(self):
        print("Hello World")
if __name__ == "__main__":
    GJournal()