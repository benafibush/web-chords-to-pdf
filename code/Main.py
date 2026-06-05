from CommandParser import CommandParser
from json2pdf.Orchestrator       import Orchestrator as json2pdfO
# from chord_trnsp.Orchestrator   import Orchestrator as chord_trnspO


class Main:
    def __init__(self) -> None:
        self.parser = CommandParser()

    def main(self) -> None:
        self.args = self.parser.parse_args()
        # if self.args.chord_trnsp:
            # self.orchestrator = chord_trnspO(self.args.json, self.args.dir)
        if self.args.json2pdf:
            self.orchestrator = json2pdfO(self.args.dbjson, self.args.dir, self.args.songids)
        self.orchestrator.orchestrate()


if __name__=="__main__":
    Main().main()