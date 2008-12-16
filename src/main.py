# coding=UTF-8
import cmd
import random
import gettext
from getthefacts.fact import *
from getthefacts.actor import *

try:
    t = gettext.translation("getthefacts", "lang")
    _ = t.gettext
except:
    _ = lambda msg: msg

__version__ = "0.2a2"

def readList(fileName, formatter):
    list = []
    try:
        list = [formatter.read(line) for line in file(fileName).readlines()
                if not (line == "\n" or line.startswith("#"))]
    finally:
        return list

class GtfCmd(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self, "\t")
        self.actors = []
        self.facts = []

    def preloop(self):
        self.actors = readList("../data/actors.txt", ActorFormatter())
        self.facts = readList("../data/facts.txt", FactFormatter())
        self.chooser = FactChooser(self.facts)
        print _("Loaded %d facts and %d actors.") % (len(self.facts),
                                                     len(self.actors))

    def postcmd(self, stop, line):
        return stop

    def do_quit(self, line):
        return True

    def do_say(self, name):
        actor = None
        if len(name) == 0:
            actor = self.__getRandomActor()
        else:
            actor = self.__findActor(name)
        self.__say_about(actor)
        return False

    def __getRandomActor(self):
        return random.choice(self.actors)

    def __findActor(self, name):
        for a in self.actors:
            if a.name == name:
                return a

    def __say_about(self, actor):
        try:
            fact = self.chooser.choose(actor)
            if fact == None:
                print _("Sorry, I don't know anything about %s.") % actor.name
            else:
                print fact.getFactAbout(actor)
        except:
            print _("Error occurred. Please try once again.")


if __name__ == "__main__":
    print _("Welcome to GetTheFacts v. %s") % __version__
    cmd = GtfCmd()
    cmd.intro = _("Type 'say <name>' to learn something interesting about" +
                  "'name', or 'say' for random fact.")
    cmd.prompt = ">>"
    cmd.cmdloop()