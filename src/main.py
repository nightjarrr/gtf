import random
# coding=UTF-8
from getthefacts.fact import *
from getthefacts.actor import *

#t = gettext.translation("getthefacts", "lang")
_ = lambda msg: msg#t.gettext

def readList(fileName, formatter):
    list = []
    try:
        list = [formatter.read(line) for line in file(fileName).readlines() if not (line == "\n" or line.startswith("#"))]
    finally:
        return list

if __name__ == "__main__":
    # Not sure whether this should be permanent or eclipse-specific
    #os.chdir(os.path.dirname(__file__))
    
    print _("Welcome!")
    print _("Loading...")
    
    actors = readList("../data/actors.txt", ActorFormatter())
    facts = readList("../data/facts.txt", FactFormatter())
    print _("Loaded %d facts and %d actors.") % (len(facts), len(actors))
    print _("\nEnter the actor name or 'Enter' for random:")
    actorName = raw_input().strip()
    
    actor = None
    if actorName == "":
        actor = random.choice(actors)
    else:
        foundActor = False
        for a in actors:
            if a.name == actorName:
                actor = a
                foundActor = True
                break
        if not foundActor:
            actor = Actor(actorName)

    chooser = FactChooser(facts)
    chosenFact = chooser.choose(actor)
    if chosenFact == None:
        print _("Sorry, I don't know anything about %s.") % actorName
    else:
        print _("Here is something interesting:\n")
        print chosenFact.getFactAbout(actor)
    print _("\nPress 'Enter' to exit.")
    raw_input()
