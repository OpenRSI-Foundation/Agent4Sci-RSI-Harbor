import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import publish_index


class IndexPublicationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files=publish_index.payload('HEAD')

    def test_complete_packages_with_exact_source_and_published_hashes(self):
        receipts=[(name,content) for name,(content,_) in self.files.items() if name.endswith('/publication.json')]
        self.assertEqual(len(receipts),26)
        for name,content in receipts:
            receipt=json.loads(content)
            self.assertRegex(receipt['source_commit'],r'^[0-9a-f]{40}$')
            for relative,record in receipt['published_files'].items():
                data,mode=self.files[f'{receipt["public_path"]}/{relative}']
                self.assertEqual(hashlib.sha256(data).hexdigest(),record['sha256'])
                self.assertEqual((len(data),mode),(record['bytes'],record['mode']))
            # Runtime authority is byte-identical to the pinned source; only documentation/licensing is adapted.
            for relative in ('task.toml','tests/verifier.py','environment/Dockerfile'):
                self.assertEqual(receipt['original_files'][relative]['sha256'],
                                 receipt['published_files'][relative]['sha256'])

    def test_export_is_idempotent_and_detects_modified_package(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            publish_index.publish(root,self.files)
            publish_index.publish(root,self.files,check=True)
            name=next(p for p in self.files if p.endswith('/tests/verifier.py'))
            (root/name).write_text('# modified evaluator')
            with self.assertRaisesRegex(ValueError,'differs'):
                publish_index.publish(root,self.files,check=True)

    def test_cannot_overwrite_unrelated_task_or_follow_symlinks(self):
        name=next(p for p in self.files if p.endswith('/publication.json'))
        for symlink in (False,True):
            with self.subTest(symlink=symlink),tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp);folder=root/Path(name).parent
                folder.parent.mkdir(parents=True)
                if symlink:
                    target=root/'elsewhere';target.mkdir();folder.symlink_to(target,target_is_directory=True)
                else:folder.mkdir()
                with self.assertRaises(ValueError):publish_index.publish(root,self.files)


if __name__=='__main__':unittest.main()
