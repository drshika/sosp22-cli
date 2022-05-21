from plumbum import cli 

class GJournal(cli.Application):
    def main(self):
        print("Hello World")
if __name__ == "__main__":
    GJournal()