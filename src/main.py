# coding=UTF-8
import os
import cmd
import random
import gettext
import os.path
from getthefacts.fact.simple import SimpleStringFactFormatter
from getthefacts.fact.jinja import JinjaFactFormatter
from getthefacts.fact.choosers import *
from getthefacts.actor import *

try:
    t = gettext.translation("getthefacts", "lang")
    _ = t.gettext
except:
    _ = lambda msg: msg

__version__ = "0.2"

def readList(fileName, formatter):
    list = []
    try:
        list = [formatter.read(line.strip()) for line in file(fileName).readlines()
                if not (line == "\n" or line.startswith("#"))]
    except Exception, e:
        print "Error occurred while reading the file %s" % fileName
        print e
    finally:
        return list

class GtfCmd(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self, "\t")
        self.actors = []
        self.facts = []

    def preloop(self):
        pass

    def postcmd(self, stop, line):
        return stop

    def __load_plain(self):
        self.actors = readList("../data/actors.txt", ActorFormatter())
        self.facts = readList("../data/facts.txt", SimpleStringFactFormatter())

    def __load_dir(self, _dir, formatter):
        r = []
        ff = os.listdir(_dir)
        for f in ff:
            fl = os.path.join(_dir,f)
            if os.path.isfile(fl):
                r.append(formatter.read(open(fl).read()))
        return r

    def __load_jinja(self):
        self.actors = self.__load_dir("../j/actors", ActorJsonFormatter())
        self.facts = self.__load_dir("../j/facts", JinjaFactFormatter())

    STORES = {
        "plain" : __load_plain,
        "jinja" : __load_jinja,
    }

    def do_load(self, store):
        store = store or "jinja"
        if store in GtfCmd.STORES:
            doload = GtfCmd.STORES[store]
            doload(self)
            print _("Loaded %d facts and %d actors.") % (len(self.facts), len(self.actors))
        else:
            print _("Unknown storage format: %s") % store
            print _("Availavle formats: %s") % ", ".join(GtfCmd.STORES.iterkeys())

    def do_quit(self, line):
        return True

    def do_say(self, name):
        actor = None
        if len(name) == 0:
            chooser = RandomFactChooser(self.facts, self.actors)
        else:
            actor = self.__findActor(name)
            if actor is None:
                print _("Sorry, I could not find %s.") % name
                return False
            chooser = ActorBasedRandomFactChooser(actor, self.facts, self.actors)
        self.__say_fact(chooser)
        return False

    def __findActor(self, name):
        for a in self.actors:
            if a.name == name:
                return a

    def __say_fact(self, chooser):
        try:
            fact = chooser.choose()
            if fact is None:
                print _("Sorry, I could not find such fact.")
            else:
                print fact
        except Exception, e:
            print _("Error occurred. Please try once again.")
            print e

    def help_say(self):
        print _("Show a fact about an actor.")
        print _("Command format:")
        print _("")
        print _("say [name]")
        print _("")
        print _("Parameters:")
        print _("    name (optional): the name of an actor. If the name is "
                "provided, a fact about this actor is displayed. If the name "
                "is omitted, a fact about random actor is displayed.")

    def help_help(self):
        print _("Display this help.")

    def help_quit(self):
        print _("Quit the program.")


if __name__ == "__main__":
    print _("Welcome to GetTheFacts v. %s") % __version__
    cmd = GtfCmd()
    cmd.intro = _("Enter the command. Enter '?' or 'help' for the "
                  "list of available commands.")
    cmd.prompt = ">>"
    cmd.cmdloop()