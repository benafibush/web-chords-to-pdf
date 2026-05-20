import unittest
from old.Orchestrator import Orchestrator


class TestOrchestrator(unittest.TestCase):

    def setUp(self) -> None:
        self.o = Orchestrator()

    def test_browse(self) -> None:
        urls = []
        url = 'https://tabs.ultimate-guitar.com/tab/meat-loaf/its-all-coming-back-to-me-now-chords-419192|+1'
        with self.assertRaises(ValueError):
            self.o.browse([])
        # single_webpage = self.o.browse([url])[0]
        # self.assertEqual(single_webpage._url, url)

    def test_parse(self) -> None:
        pass

    def test_publish(self) -> None:
        pass


if __name__ == '__main__':
    unittest.main()
