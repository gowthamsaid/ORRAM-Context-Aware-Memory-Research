import pathlib, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
class TestContract(unittest.TestCase):
    def test_shape(self):
        s=(ROOT/'scripts/generate_ram.tcl').read_text()
        for token in ('-word_size 8','-num_words 32','-rw_ports 1','-decoder $variant'):
            self.assertIn(token,s)
    def test_guardrails(self):
        a=(ROOT/'scripts/evaluate_context.py').read_text()
        self.assertIn('BLOCKED:',a)
        self.assertIn('NO_REVERSAL_IN_ISOLATED_BOUNDARY_SCREEN',a)
    def test_automation(self):
        self.assertIn('ORRAM boundary-context feasibility',(ROOT/'.github/workflows/feasibility.yml').read_text())
    def test_no_false_publication_claim(self):
        self.assertIn('not', (ROOT/'README.md').read_text().lower())
