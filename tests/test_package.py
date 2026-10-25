"""Check the files that an installed skill actually needs, not instruction wording."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'videodeck'


class PackageTest(unittest.TestCase):
    def test_installable_entrypoints_exist(self):
        self.assertTrue((SKILL / 'SKILL.md').is_file())
        self.assertTrue((SKILL / 'agents/openai.yaml').is_file())

    def test_local_markdown_links_resolve(self):
        for document in SKILL.rglob('*.md'):
            if 'node_modules' in document.parts:
                continue
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', document.read_text()):
                if re.match(r'[a-z][a-z0-9+.-]*:|#', target):
                    continue
                path = target.split('#', 1)[0]
                resolved = (document.parent / path).resolve()
                with self.subTest(document=document.relative_to(ROOT), target=target):
                    self.assertTrue(resolved.is_relative_to(SKILL))
                    self.assertTrue(resolved.exists(), 'missing installed resource')

    def test_no_private_paths_in_portable_skill(self):
        for document in SKILL.rglob('*'):
            if not document.is_file() or 'node_modules' in document.parts:
                continue
            if document.name.endswith('.local.json'):
                continue  # Personal settings are ignored and never distributed.
            if document.suffix not in {'.md', '.json', '.html', '.py', '.yaml', '.mjs'}:
                continue
            text = document.read_text()
            with self.subTest(document=document.relative_to(ROOT)):
                self.assertNotIn('/Users/', text)
                self.assertNotIn('/private/tmp/', text)


if __name__ == '__main__':
    unittest.main()
