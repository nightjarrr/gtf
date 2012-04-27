# coding=UTF-8
import unittest
from getthefacts.fact.jinja import ActorExtension
from getthefacts.actor import Actor
from getthefacts.rules import *
from jinja2 import Environment

class JinjaFactTemplateTests(unittest.TestCase):
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
