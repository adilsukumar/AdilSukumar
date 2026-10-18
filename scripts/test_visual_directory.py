from pathlib import Path
import tempfile,unittest,xml.etree.ElementTree as ET
from unittest.mock import patch
import project_directory as pd
from test_project_directory import repo

class VisualDirectoryTests(unittest.TestCase):
 def test_visual_assets_escape_metadata_and_do_not_change_between_runs(self):
  source=[repo('new-project',description='A <script> & "quoted" description')]
  _,public,counts=pd.generate(source)
  with tempfile.TemporaryDirectory() as tmp,patch.object(pd,'ROOT',Path(tmp)):
   body=pd.generate_visual(public,counts)
   assets=list((Path(tmp)/'assets/directory').glob('*.svg'))
   self.assertEqual(len(assets),5)
   for f in assets:ET.parse(f)
   snapshots={f.name:f.read_bytes() for f in assets}
   self.assertEqual(body,pd.generate_visual(public,counts))
   self.assertEqual(snapshots,{f.name:f.read_bytes() for f in assets})
   self.assertIn('new-project',body)
   self.assertNotIn('<script>',body)
   self.assertEqual(body.count('href="https://github.com/adilsukumar/new-project"'),1)
   self.assertTrue(all('@media(prefers-reduced-motion:reduce)' in f.read_text() for f in assets))

if __name__=='__main__':unittest.main()
