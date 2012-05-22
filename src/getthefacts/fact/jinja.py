# coding=UTF-8

from . import *
from .. import rules

from jinja2 import Environment
from jinja2.ext import Extension

class ActorExtension(Extension):
    """
    The Jinja2 extension that allows to define actor rules in Jinja template
    Sample usage is as follows:

        {% actor 'author', '(bear, big, !toy, !@Baloo)' %}

    Here 'author' is the actor name that can be used further throughout the template,
    and '(bear, big, !toy, !@Baloo)' is a rule definition for the actor.
    Rule sting is optional, and in case it is missing, any actor is deemed suitable

        {% actor 'author' %}
    """

    tags = set(["actor"])

    def __init__(self, environment):
        super(ActorExtension, self).__init__(environment)
        if not hasattr(self.environment, 'actorPlaceholders'):
            self.environment.actorPlaceholders = []

    def parse(self, parser):
        # Skip the tag name
        lineno = parser.stream.next().lineno
        name = parser.parse_expression().value
        if parser.stream.skip_if('comma'):
            r = parser.parse_expression().value
            try:
                rule = rules.RuleParser(r).parse()
            except rules.RuleParserError:
                parser.fail('Invalid rule syntax: "%s"' % r, lineno, exc = rules.RuleParserError)
        else:
            rule = rules.TrueRule()
        if not parser.stream.current.test('block_end'):
            parser.fail('"actor" statement not finished.', lineno)

        # Register the actor definition
        a = ActorPlaceholder(name, rule)
        self.environment.actorPlaceholders.append(a)
        # No need to actually return anything to the template
        return []

class JinjaFactTemplate(FactTemplate):
    def __init__(self, factString):
        FactTemplate.__init__(self)
        self.factString = factString

    def __parse__(self):
        self.e = Environment(extensions = [ActorExtension])
        self.template = self.e.from_string(self.factString)
        return self.e.actorPlaceholders

    def render(self, ctx):
        return self.template.render(ctx)

class JinjaFactFormatter:

    """Read and write Facts to and from string."""

    def read(self, factString):
        t = JinjaFactTemplate(factString)
        return t
