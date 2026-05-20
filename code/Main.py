from CommandParser import CommandParser
from url2txt import Orchestrator as url2txtO
from txt2pdf import Orchestrator as txt2pdfO

class Main:
    def __init__(self) -> None:
        self.parser = CommandParser()

    def main(self) -> None:
        self.args = self.parser.parse_args()
        if self.args.url2txt:
            self.orchestrator = url2txtO(self.args.csv, self.args.dir)
        if self.args.txt2pdf:
            self.orchestrator = txt2pdfO(self.args.csv, self.args.dir)
        self.orchestrator.orchestrate()


if __name__=="__main__":
    Main().main()