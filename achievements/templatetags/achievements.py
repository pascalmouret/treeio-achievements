"""
These templatetags are used to generate the characteristic lists of tree.io. I started out
from the templatetag used in the Identities module. They are pretty simple and almost the same, only
use a different template.
"""
from coffin import template
from treeio.core.rendering import render_to_string
from jinja2 import contextfunction, Markup
from django.template import RequestContext


register = template.Library()


@contextfunction
def achievements_user_list(context, users, skip_group=False):
    """
    Print a list of users.

    Arguments:
    context -- the current Context object, supplied by the decorator
    users -- a iterable collection of User objects
    skip_group -- letters to be skipped
    """
    request = context['request']

    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    return Markup(render_to_string('achievements/tags/user_list',
                               {'users': users, 'skip_group': skip_group},
                               context_instance=RequestContext(request),
                               response_format=response_format))

register.object(achievements_user_list)


@contextfunction
def achievements_achievements_list(context, achievements, skip_group=False):
    """
    Print a list of achievements.

    Arguments:
    context -- the current Context object, supplied by the decorator
    achievements -- a iterable collection of Achievement objects
    skip_group -- letters to be skipped
    """
    request = context['request']

    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    return Markup(render_to_string('achievements/tags/achievements_list',
                               {'achievements': achievements, 'skip_group': skip_group},
                               context_instance=RequestContext(request),
                               response_format=response_format))

register.object(achievements_achievements_list)


@contextfunction
def achievements_prototypes_list(context, prototypes, skip_group=False):
    """
    Print a list of prototypes.

    Arguments:
    context -- the current Context object, supplied by the decorator
    prototypes -- a iterable collection of Prototype objects
    skip_group -- letters to be skipped
    """
    request = context['request']

    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    return Markup(render_to_string('achievements/tags/prototypes_list',
                               {'prototypes': prototypes, 'skip_group': skip_group},
                               context_instance=RequestContext(request),
                               response_format=response_format))

register.object(achievements_prototypes_list)


@contextfunction
def icon_line(context, user=None, size=25):
    """
    Print a line with a certain amount off achievement-icons.

    Arguments:
    context -- the current Context object, supplied by the decorator
    user -- which user, defaults to the active account
    size -- how many icons should be displayed
    """
    request = context['request']
    if not user:
        user = request.user

    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    achievements = user.achievements.all()[:size]

    return Markup(render_to_string('achievements/tags/icon_line', {'achievements': achievements},
                                   context_instance=RequestContext(request),
                                   response_format=response_format))

register.object(icon_line)