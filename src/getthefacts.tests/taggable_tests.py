import unittest
from getthefacts.taggable import Taggable

class HasTagsTestCase(unittest.TestCase):
    def runTest(self):
        t = Taggable(["tag1"])
        assert t.hasTags()
        
class HasNotTagsTestCase(unittest.TestCase):
    def runTest(self):
        t = Taggable([])
        assert not t.hasTags()
        
class IsTaggedWithTestCase(unittest.TestCase):
    def runTest(self):
        t = Taggable(["tag1", "tag2"])
        assert t.isTaggedWith("tag1")

class IsNotTaggedWithTestCase(unittest.TestCase):
    def runTest(self):
        t = Taggable(["tag1", "tag2"])
        assert not t.isTaggedWith("tag3")

class IsTaggedWithAnyTestCase(unittest.TestCase):
    def runTest(self):
        t = Taggable(["tag1", "tag2"])
        assert t.isTaggedWithAny(["tag1", "tag3"])

class IsNotTaggedWithAnyTestCase(unittest.TestCase):
    def runTest(self):
        t = Taggable(["tag1", "tag2"])
        assert not t.isTaggedWithAny(["tag0", "tag3"])

if __name__ == "__main__":
    unittest.main()