# coding=UTF-8
import unittest
from getthefacts.fact.jinja import ActorExtension, JinjaFactTemplate
from getthefacts.actor import Actor
from getthefacts.rules import *
from jinja2 import Environment

class JinjaExtensionTests(unittest.TestCase):
    def testActorSyntax(self):
        e = Environment(extensions = [ActorExtension])
        template = e.from_string(' {% actor "author", "(old, beard)" %} ')
        assert e.actorPlaceholders is not None
        assert len(e.actorPlaceholders) == 1
        assert e.actorPlaceholders[0].index == 'author'
        assert e.actorPlaceholders[0].rule == AndRule([TagRule('old'), TagRule('beard')])

    def testActorWithoutRulesSyntax(self):
        e = Environment(extensions = [ActorExtension])
        template = e.from_string(' {% actor "author" %}')
        assert e.actorPlaceholders is not None
        assert len(e.actorPlaceholders) == 1
        assert e.actorPlaceholders[0].index == 'author'
        assert e.actorPlaceholders[0].rule == TrueRule()

    def testMultipleActorSyntax(self):
        e = Environment(extensions = [ActorExtension])
        template = e.from_string("""
                {% actor "author1", "(old, beard)" %}
                {% actor "author2", "(!old, beard)" %}
                {% actor "author3", "(old, !beard)" %}
                """)
        assert e.actorPlaceholders is not None
        assert len(e.actorPlaceholders) == 3
        assert e.actorPlaceholders[0].index == 'author1'
        assert e.actorPlaceholders[0].rule == AndRule([TagRule('old'), TagRule('beard')])

        assert e.actorPlaceholders[1].index == 'author2'
        assert e.actorPlaceholders[1].rule == AndRule([NotRule(TagRule('old')), TagRule('beard')])

        assert e.actorPlaceholders[2].index == 'author3'
        assert e.actorPlaceholders[2].rule == AndRule([TagRule('old'), NotRule(TagRule('beard'))])

class JinjaFactTemplateTests(unittest.TestCase):
    def test(self):
        s = """
            {% actor "author", "(old, beard)" %}
            {{ author.name }} was old and had a huge beard, but still he's a genius!
        """
        t = JinjaFactTemplate(s)
        f = t.buildup()
        a = Actor("Ernest Hemingway", ["old", "beard"])
        r = f.getFactAbout(a)
        print r
        assert r.strip() == "Ernest Hemingway was old and had a huge beard, but still he's a genius!"