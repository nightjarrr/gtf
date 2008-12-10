

class Taggable:
    "Defines an object that can be assigned with several descriptive tags"
    def __init__(self, tags):
        self.tags = tags
    
    def hasTags(self):
        return len(self.tags) > 0
    
    def isTaggedWith(self, tag):
        return tag in self.tags
        
    def isTaggedWithAny(self, tags):
        for tag in tags:
            if self.isTaggedWith(tag): return True
        return False