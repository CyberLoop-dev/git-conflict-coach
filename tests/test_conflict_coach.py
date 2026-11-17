import unittest
from conflict_coach import parse_conflicts,render_html

class ConflictTests(unittest.TestCase):
    def test_complete_conflict_block(self):
        found=parse_conflicts("one\n<<<<<<< HEAD\na\n=======\nb\n>>>>>>> branch\n")
        self.assertEqual(len(found),1)
        self.assertEqual(found[0]["start_line"],2)
        self.assertEqual(found[0]["end_line"],6)

    def test_incomplete_block_is_reported(self):
        found=parse_conflicts("<<<<<<< HEAD\nunfinished")
        self.assertEqual(found[0]["kind"],"incomplete conflict block")

    def test_html_report_escapes_paths(self):
        html=render_html([{"file":"<script>","start_line":1,"end_line":2,"kind":"unresolved"}])
        self.assertNotIn("<script>",html)
        self.assertIn("&lt;script&gt;",html)

if __name__=="__main__": unittest.main()
