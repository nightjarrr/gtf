# coding=UTF-8

class Taggable:

    """Object that can be labelled with tags."""
    
    def __init__(self, tags):
        """Initialize new instance of Taggable."""
        self.tags = tags
    
    def hasTags(self):
        """Return True if any tags are assigned to this instance."""
        return len(self.tags) > 0
    
    def isTaggedWith(self, tag):
        """Return True if this instance is tagged with specified tag."""
        return tag in self.tags
        
    def isTaggedWithAny(self, tags):
        """Return True if this instance is tagged with any of specified tags."""
        for tag in tags:
            if self.isTaggedWith(tag): return True
        return False