import WebPage
import Songbook


class Orchestrator:

    def browse(self, urls: list[str]) -> [WebPage]:
        if not urls:
            raise ValueError("URL list is empty")

    def parse(self, webpages) -> Songbook:
        raise NotImplementedError

    def publish(self, songbook) -> None:
        raise NotImplementedError
