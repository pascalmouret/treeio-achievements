"""
Here are the functions which actually prepare the data and render the pages.
Most of the functions here are very similar since tree.io is, more or less, following
the CRUD (Create, Retrieve, Update, Delete) pattern.
The only thing special are the MassForms, which are quite common in tree.io and I only
adapted the code to fit my purposes.
Also: The forms.py file is in many ways more important since all forms are defined there.
"""
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from treeio.core.models import User
from treeio.core.rendering import render_to_response
from treeio.core.decorators import treeio_login_required, handle_response_format
from achievements.forms import MassActionUserForm, MassActionUserAchievementsForm, MassActionAchievementsForm, \
                               PrototypeForm, AchievementForm
from achievements.models import Prototype, Achievement


def _get_default_context(request, type):
    """
    This function generates a context with a prepared massform.

    Arguments:
    request -- a Django Request object
    type -- the type of MassForm you want
    """
    context = {}
    massform = type(request.user.get_profile())
    context.update({'massform': massform})
    return context


def _process_mass_form(f):
    """
    This decorator checks if and which mass-form type is received and reacts in a proper fashion. (read: saves)
    By excluding this, the views themselfes get a bit less crowded. And it is the way it is in every other module
    as well.

    Arguments:
    f -- the function that is decorated
    """

    def wrap(request, *args, **kwargs):
        """
        Checks first which MassForm we are dealing with, then check if the user has the necessary permission.
        If that all checks out, execute the save() action.

        Arguments:
        request -- the Django-request
        *args -- catch args to pass them on afterwards
        **kwargs -- catch kwargs to pass them on afterwards
        """
        user = request.user.get_profile()
        # check for massform and check permission
        if 'massform' in request.POST and request.user.get_profile().is_admin(module_name='achievements'):
            for key in request.POST:
                if 'mass-user' in key:
                    try:
                        user = User.objects.get(pk=request.POST[key])
                        form = MassActionUserForm(request.user.get_profile(), request.POST, instance=user)
                        if form.is_valid():
                            form.save()
                    except Exception:
                        pass
                if 'mass-achievement' in key:
                    try:
                        prototype = Prototype.objects.get(pk=request.POST[key])
                        form = MassActionAchievementsForm(request.user.get_profile(), request.POST, instance=prototype)
                        if form.is_valid():
                            form.save()
                    except Exception:
                        pass
                if 'mass-userachievement' in key:
                    try:
                        achievement = Achievement.objects.get(pk=request.POST[key])
                        form = MassActionUserAchievementsForm(request.user.get_profile(),
                                                              request.POST, instance=achievement)
                        if form.is_valid():
                            form.save()
                    except Exception:
                        pass
        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


@handle_response_format
@treeio_login_required
@_process_mass_form
def index(request, response_format='html'):
    """
    This view displays a list of user, with their achievements (icons). Has a MassForm.

    Arguments:
    request -- a Django Request object
    response_format -- defines which format the response should be
    """
    users = User.objects.all()

    context = _get_default_context(request, MassActionUserForm)
    context.update({'users': users})

    return render_to_response('achievements/index', context, context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
@_process_mass_form
def user(request, user_id, response_format='html'):
    """
    This just displays one user and his achievements. Has a MassForm.

    Arguments:
    request -- a Django Request object
    user_id -- the id of the requested User object
    response_format -- defines which format the response should be
    """
    user = User.objects.get(pk=user_id)
    achievements = Achievement.objects.filter(user=user)

    context = _get_default_context(request, MassActionUserAchievementsForm)
    context.update({'u': user, 'achievements': achievements})

    return render_to_response('achievements/user', context, context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
@_process_mass_form
def prototypes(request, response_format='html'):
    """
    Gives an overview over all available Achievements, with the description. Has a MassForm.

    Arguments:
    request -- a Django Request object
    response_format -- defines which format the response should be
    """
    prototypes = Prototype.objects.filter(trash=False)

    context = _get_default_context(request, MassActionAchievementsForm)
    context.update({'protos': prototypes})

    return render_to_response('achievements/prototypes', context, context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
def prototype_add(request, response_format='html'):
    """
    This delivers a view to create a new Prototype.

    Arguments:
    request -- a Django Request object
    response_format -- defines which format the response should be
    """
    if request.POST:
        if not 'cancel' in request.POST:
            form = PrototypeForm(request.user.get_profile(), request.POST, files=request.FILES)
            if form.is_valid():
                prototype = form.save()  # TODO: saver
                return HttpResponseRedirect(reverse('achievements_prototype_detail', args=[prototype.id]))
        else:
            return HttpResponseRedirect(reverse('achievements_prototypes'))
    else:
        form = PrototypeForm(request.user)

    return render_to_response('achievements/prototype_form', {'form': form},
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def prototype_edit(request, prototype_id, response_format='html'):
    """
    Opens a form to edit a Prototype.

    Arguments:
    request -- a Django Request object
    prototype_id -- the id of the requested Prototype object
    response_format -- defines which format the response should be
    """
    prototype = get_object_or_404(Prototype, pk=prototype_id)
    if not request.user.get_profile().has_permission(prototype, mode='w'):
        return HttpResponseRedirect(reverse('achievements_prototype_detail', args=[prototype.id]))

    if request.POST:
        if not 'cancel' in request.POST:
            form = PrototypeForm(request.user.get_profile(), request.POST, files=request.FILES, instance=prototype)
            if form.is_valid():
                prototype = form.save()
                return HttpResponseRedirect(reverse('achievements_prototype_detail', args=[prototype.id]))
        else:
            return HttpResponseRedirect(reverse('achievements_prototypes'))
    else:
        form = PrototypeForm(request.user, instance=prototype)

    return render_to_response('achievements/prototype_form', {'form': form},
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def prototype_detail(request, prototype_id, response_format='html'):
    """
    Opens a simple overview for one Prototype.

    Arguments:
    request -- a Django Request object
    prototype_id -- the id of the requested Prototype object
    response_format -- defines which format the response should be
    """
    prototype = get_object_or_404(Prototype, pk=prototype_id)
    return render_to_response('achievements/prototype_detail', {'prototype': prototype},
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def prototype_delete(request, prototype_id, response_format='html'):
    """
    Simply deletes a Prototype and redirects to the list. If the permissions are alright, of course.

    Arguments:
    request -- a Django Request object
    prototype_id -- the id of the requested Prototype object
    response_format -- defines which format the response should be
    """
    prototype = get_object_or_404(Prototype, pk=prototype_id)
    if request.user.get_profile().has_permission(Prototype, mode='w'):
        prototype.delete()
    else:
        return HttpResponseRedirect(reverse('achievements_prototype_detail', args=[prototype.id]))
    return HttpResponseRedirect(reverse('achievements_prototypes'))


@handle_response_format
@treeio_login_required
def achievement_add(request, response_format='html'):
    """
    Opens an empty form for a new Achievement.

    Arguments:
    request -- a Django Request object
    response_format -- defines which format the response should be
    """
    if request.POST:
        if not 'cancel' in request.POST:
            form = AchievementForm(request.user.get_profile(), request.POST, files=request.FILES)
            if form.is_valid():
                achievement = form.save()  # TODO: saver
                return HttpResponseRedirect(reverse('achievements_achievement_detail', args=[achievement.id]))
        else:
            return HttpResponseRedirect(reverse('achievements'))
    else:
        form = AchievementForm(request.user)

    return render_to_response('achievements/achievement_form', {'form': form},
                               context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def achievement_edit(request, achievement_id, response_format='html'):
    """
    Opens a form to edit a specific Achievement.

    Arguments:
    request -- a Django Request object
    achievement_id -- the id of the requested Achievement object
    response_format -- defines which format the response should be
    """
    achievement = get_object_or_404(Achievement, pk=achievement_id)
    if request.POST:
        if not 'cancel' in request.POST:
            form = AchievementForm(request.user.get_profile(), request.POST, files=request.FILES, instance=achievement)
            if form.is_valid():
                achievement = form.save()  # TODO: saver
                return HttpResponseRedirect(reverse('achievements_achievement_detail', args=[achievement.id]))
        else:
            return HttpResponseRedirect(reverse('achievements'))
    else:
        form = AchievementForm(request.user, instance=achievement)

    return render_to_response('achievements/achievement_form', {'form': form},
                               context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def achievement_detail(request, achievement_id, response_format='html'):
    """
    Opens a simple overview for one Achievement.

    Arguments:
    request -- a Django Request object
    achievement_id -- the id of the requested Achievement object
    response_format -- defines which format the response should be
    """
    achievement = get_object_or_404(Achievement, pk=achievement_id)
    return render_to_response('achievements/achievement_detail', {'achievement': achievement},
                               context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def achievement_delete(request, achievement_id, response_format='html'):
    """
    Simply deletes a Achievement and redirects to the list. If the permissions are alright, of course.

    Arguments:
    request -- a Django Request object
    achievement_id -- the id of the requested Achievement object
    response_format -- defines which format the response should be
    """
    achievement = get_object_or_404(Achievement, pk=achievement_id)
    if request.user.get_profile().has_permission(Prototype, mode='w'):
        achievement.delete()
    else:
        return HttpResponseRedirect(reverse('achievements_achievement_detail', args=[achievement.id]))
    return HttpResponseRedirect(reverse('achievements'))


@handle_response_format
@treeio_login_required
def widget_achievement_stream(request, response_format='html'):
    """
    Gets the last three Achievements and gives them to the widget template. This will be rendered as the Widget.

    Arguments:
    request -- a Django Request object
    response_format -- defines which format the response should be
    """
    achievements = Achievement.objects.all()[:3]
    return render_to_response('achievements/widgets/newest', {'achievements': achievements},
                               context_instance=RequestContext(request), response_format=response_format)
