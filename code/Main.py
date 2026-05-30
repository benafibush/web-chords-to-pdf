from CommandParser import CommandParser
from url2txt.Orchestrator       import Orchestrator as url2txtO
# from chord_trnsp.Orchestrator   import Orchestrator as chord_trnspO
# from txt2pdf.Orchestrator       import Orchestrator as txt2pdfO


class Main:
    def __init__(self) -> None:
        self.parser = CommandParser()

    def main(self) -> None:
        self.args = self.parser.parse_args()
        if self.args.url2txt:
            self.orchestrator = url2txtO(self.args.json, self.args.dir)
        # if self.args.chord_trnsp:
            # self.orchestrator = chord_trnspO(self.args.json, self.args.dir)
        if self.args.txt2pdf:
            self.orchestrator = txt2pdfO(self.args.json, self.args.dir)
        self.orchestrator.orchestrate()


if __name__=="__main__":
    Main().main()