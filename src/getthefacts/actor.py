from taggable import Taggable

class Actor(Taggable):
    ""
    def __init__(self, name, tags = []):
        Taggable.__init__(self, tags)
        self.name = name
        
class ActorFormatter:
    "Enables saving and loading the Actor to string"
    
    def read(self, actorString):
        if actorString.find("|") == -1:
            return Actor(actorString.strip())
        [actorName, tagList] = actorString.split("|", 1)
        tags = [tag.strip() for tag in tagList.split(",")]
        return Actor(actorName.strip(), tags)
    
    def write(self, actor):
        if actor.hasTags():
            return "%s| " % actor.name + ", ".join(actor.tags)
        else: return actor.name
