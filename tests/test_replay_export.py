"""Keep embedded replay text from being interpreted as executable HTML."""
from html.parser import HTMLParser
from pathlib import Path
import json
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from run_match import replay_html


class ReplayExportTests(unittest.TestCase):
    def test_html_like_team_name_stays_inside_json(self):
        class Scripts(HTMLParser):
            def __init__(self):
                super().__init__()
                self.active = False
                self.payload = ''
                self.count = 0

            def handle_starttag(self, tag, attrs):
                if tag == 'script':
                    self.count += 1
                    self.active = dict(attrs).get('id') == 'match-record'

            def handle_endtag(self, tag):
                if tag == 'script':
                    self.active = False

            def handle_data(self, data):
                if self.active:
                    self.payload += data

        record = {'teamNames': ['</script><script>throw new Error("injected")</script>',
                                'Greedy baseline'], 'frames': []}
        parser = Scripts()
        parser.feed(replay_html(record))
        self.assertEqual(json.loads(parser.payload), record)
        self.assertEqual(parser.count, 6)


if __name__ == '__main__':
    unittest.main()
