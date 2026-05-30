from urllib.parse import urlparse
from playwright.sync_api import sync_playwright, Browser as pw_Browser, BrowserContext, Page
import pandas as pd


class Browser:
    def __init__(self) -> None:
        self.tab4u_text: str = "song_block_content"
        self.tab4u_chord: str = "c_C"
        self.tab4u_lyrics: str = "song"
        self.ultimate_guitar_text: str = "k_vI3 KLhHx fGc1h"
        self.ultimate_guitar_chord: str = "eSJpP _6Im1s HslD7"
        self.ultimate_guitar_lyrics: str = ""
        self.text = []
        self.playwright = None
        self.browser: pw_Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None

    def process_row(self, row: pd.Series) -> pd.Series:
        link: str = str(row.get('Link'))
        text: str = self.browse_and_extract(link)
        row['Text'] = text
        return row

    def _ensure_browser(self) -> None:
        if self.browser is not None and self.page is not None:
            return

        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(channel="msedge", headless=False)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

    def browse_and_extract(self, link: str) -> str:
        self._ensure_browser()

        hostname = urlparse(link).hostname or ""
        page = self.page
        try:
            try:
                page.goto(link, timeout=15000)
            except Exception:
                # continue even if navigation times out; try to get content
                pass

            if "tab4u" in hostname or "tab4u.com" in link:
                page.wait_for_selector(f".{self.tab4u_text}")
                elems = page.query_selector_all(f".{self.tab4u_text}")
                texts = [el.inner_text().strip() for el in elems if el]
                content = "\n\n".join(texts)
            elif "ultimate-guitar" in hostname or "ultimate-guitar.com" in link:
                page.wait_for_selector(f".{self.ultimate_guitar_text}")
                elems = page.query_selector_all(f".{self.ultimate_guitar_text}")
                texts = [el.inner_text().strip() for el in elems if el]
                content = "\n\n".join(texts)
            else:
                # generic fallback: return visible text
                content = page.inner_text('body')
        except Exception as e:
            content = f"EXTRACT_ERROR: {e}"

        return content
