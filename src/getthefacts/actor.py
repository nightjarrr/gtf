# coding=UTF-8

import json
from taggable import Taggable

class Actor(Taggable):

    """Object that can be a character of fact."""

    def __init__(self, name, tags = []):
        """Initialize new instance of Actor."""
        Taggable.__init__(self, tags)
        self.name = name

        
class ActorFormatter:

    "Read or write Actor to string"
    
    def read(self, actorString):
        """Read Actor from string representation."""
        if actorString.find("|") == -1:
            return Actor(actorString.strip())
        [actorName, tagList] = actorString.split("|", 1)
        tags = [tag.strip() for tag in tagList.split(",")]
        return Actor(actorName.strip(), tags)
    
    def write(self, actor):
        """Write Actor to string representation."""
        if actor.hasTags():
            return "%s| " % actor.name + ", ".join(actor.tags)
        else: return actor.name

class ActorJsonFormatter:
    def read(self, actorString):
        d = json.loads(actorString)
        if not "name" in d:
            return None
        a = Actor(None)
        for k,v in d.iteritems():
            setattr(a, k, v)
        return a

    def write(self, actor):
        pass