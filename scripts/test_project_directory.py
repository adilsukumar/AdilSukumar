import unittest
from project_directory import generate, classify

def repo(name,**fields):
 return {'name':name,'private':False,'owner':{'login':'adilsukumar'},'description':'','topics':[],**fields}

class DirectoryTests(unittest.TestCase):
 def test_visibility_and_ownership(self):
  _,public,_=generate([repo('hello'),repo('private-project',private=True),repo('foreign',owner={'login':'someone-else'})])
  self.assertEqual(list(public),['hello'])
 def test_unknown_stays_visible(self):
  body,_,counts=generate([repo('a-brand-new-thing')])
  self.assertEqual(counts['new'],1)
  self.assertIn('a-brand-new-thing',body)
 def test_new_repo_topic_routes_to_field(self):
  self.assertEqual(classify(repo('new-genomics-tool',topics=['bioinformatics']))[0],'bio')
  self.assertEqual(classify(repo('new-device',topics=['sector-robotics']))[0],'hardware')
 def test_untrusted_metadata_is_escaped(self):
  body,_,_=generate([repo('brand-new',description='<script>alert(1)</script> & text')])
  self.assertNotIn('<script>',body)
  self.assertIn('&lt;script&gt;',body)
 def test_forks_keep_credit(self):
  body,_,_=generate([repo('leetcode-company-wise-problems-2022',fork=True)])
  self.assertIn('upstream fork',body)
 def test_repeated_results_appear_once(self):
  body,public,_=generate([repo('hello'),repo('hello')])
  self.assertEqual(len(public),1)
  self.assertEqual(body.count('<li>'),1)
 def test_empty_response_is_not_written(self):
  with self.assertRaises(ValueError):generate([])

if __name__=='__main__':unittest.main()
