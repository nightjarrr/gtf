# coding=UTF-8

from . import *
from .. import rules

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

    def parse(self, parser):
        pass

