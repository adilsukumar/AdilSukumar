import unittest,json,xml.etree.ElementTree as ET
from pathlib import Path
from repo_art import KINDS,art,kind_for
from project_directory import generate
from visuals import svg,repo_row

class RepoArtTests(unittest.TestCase):
 def test_all_current_displayed_repositories_have_different_motion_scenes(self):
  root=Path(__file__).resolve().parents[1]
  repos=json.loads((root/'data/repositories.json').read_text(encoding='utf-8'))
  _,public,_=generate(repos)
  self.assertNotIn('Amazon_ML_Challenge_2026',public)
  self.assertEqual({kind_for(name) for name in public},set(KINDS.values()))
  self.assertEqual(len({kind_for(name) for name in public}),len(public))
  for name in public:
   kind=kind_for(name)
   for mobile in [False,True]:
    content=repo_row(name,'A short description',mobile=mobile,kind=kind)
    ET.fromstring(content)
    self.assertIn('data-motion-kind="'+kind+'"',content)
    self.assertIn('class="mini-',content)
 def test_amazon_is_excluded_even_when_api_returns_it(self):
  from test_project_directory import repo
  body,public,_=generate([repo('Amazon_ML_Challenge_2026'),repo('Website')])
  self.assertNotIn('Amazon_ML_Challenge_2026',body)
  self.assertEqual(list(public),['Website'])
if __name__=='__main__':unittest.main()
