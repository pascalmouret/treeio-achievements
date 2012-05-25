"""
Since most of tree.io is based around forms, there are a few of them here. The MassForm's feature a save()
method which allows execution of whatever the user wanted by just running form.save()
Maybe a bit odd is the unused 'user' argument, but this is default in tree.io and to be sure it's saver to keep it in.
"""
from django import forms
from django.utils.translation import ugettext as _
from treeio.core.decorators import preprocess_form
from achievements.models import Prototype, Achievement

preprocess_form()


def _get_achievement_choices():
    """ Make a list of tuples with all available Achievements, so they can be used for ChoiceFields. """
    prts = Prototype.objects.filter(trash=False)
    ret = [('-', '-')]
    for prt in prts:
        choice = (prt.pk, prt.title)
        ret.append(choice)
    return ret


class MassActionUserForm(forms.Form):
    """ Mass action form for Users in Achievements"""

    award = forms.ChoiceField(label=_("Award selected"), choices=_get_achievement_choices(), required=False)
    instance = None

    def __init__(self, user, *args, **kwargs):
        """
        If the kwargs argument instance is given, set it. Then run the init of forms.Form. Also, make sure the
        fields are set.

        Arguments:
        user -- the current user (get it via request.user)
        instance -- the object the form is related to
        *args -- arguments to be passed on
        **kwargs -- keyword arguments to be passed on
        """
        if 'instance' in kwargs:
            self.instance = kwargs['instance']
            del kwargs['instance']

        super(MassActionUserForm, self).__init__(*args, **kwargs)

        self.fields['award'] = forms.ChoiceField(label=_("Award selected"), choices=_get_achievement_choices(),
                                                 required=False)

    def save(self, *args, **kwargs):
        """
        Create a new Achievement object according to the form.

        Arguments:
        *args -- catch all arguments
        **kwargs -- catch all keyword arguments
        """
        if self.instance:
            if self.is_valid():
                if self.cleaned_data['award'] and self.cleaned_data['award'] != '-':
                    p = Prototype.objects.get(pk=self.cleaned_data['award'])
                    a = Achievement(prototype=p, user=self.instance)
                    a.save()


class MassActionUserAchievementsForm(forms.Form):
    """ Mass action form for User-Achievements in Achievements"""

    revoke = forms.ChoiceField(label=_("With selected"), choices=[('-', '-'), ('revoke', _('Revoke'))], required=False)
    instance = None

    def __init__(self, user, *args, **kwargs):
        """
        If the kwargs argument instance is given, set it. Then run the init of forms.Form. Also, make sure the
        fields are set.

        Arguments:
        user -- the current user (get it via request.user)
        instance -- the object the form is related to
        *args -- arguments to be passed on
        **kwargs -- keyword arguments to be passed on
        """
        if 'instance' in kwargs:
            self.instance = kwargs['instance']
            del kwargs['instance']

        super(MassActionUserAchievementsForm, self).__init__(*args, **kwargs)

        self.fields['revoke'] = forms.ChoiceField(label=_("With selected"),
                                                  choices=[('-', '-'), ('revoke', _('Revoke'))],
                                                  required=False)

    def save(self, *args, **kwargs):
        """
        Delete the specified Achievement object,

        Arguments:
        *args -- catch all arguments
        **kwargs -- catch all keyword arguments
        """
        if self.instance:
            if self.is_valid():
                if self.cleaned_data['revoke'] and self.cleaned_data['revoke'] != '-':
                    self.instance.delete()


class MassActionAchievementsForm(forms.Form):
    """ Mass action form for Achievements """

    delete = forms.ChoiceField(label=_("With selected"), choices=(('', '-----'), ('delete', _('Delete Completely')),
                                                    ('trash', _('Move to Trash'))), required=False)
    instance = None

    def __init__(self, user, *args, **kwargs):
        """
        If the kwargs argument instance is given, set it. Then run the init of forms.Form. Also, make sure the
        fields are set.

        Arguments:
        user -- the current user (get it via request.user)
        instance -- the object the form is related to
        *args -- arguments to be passed on
        **kwargs -- keyword arguments to be passed on
        """
        if 'instance' in kwargs:
            self.instance = kwargs['instance']
            del kwargs['instance']

        super(MassActionAchievementsForm, self).__init__(*args, **kwargs)

        self.fields['delete'] = forms.ChoiceField(label=_("With selected"),
                                                  choices=(('', '-----'), ('delete', _('Delete Completely')),
                                                           ('trash', _('Move to Trash'))),
                                                  required=False)

    def save(self, *args, **kwargs):
        """
        Delete or trash the selected Prototype.

        Arguments:
        *args -- catch all arguments
        **kwargs -- catch all keyword arguments
        """
        if self.instance:
            if self.is_valid():
                if self.cleaned_data['delete']:
                    if self.cleaned_data['delete'] == 'delete':
                        self.instance.delete()
                    if self.cleaned_data['delete'] == 'trash':
                        self.instance.trash = True
                        self.instance.save()


class PrototypeForm(forms.ModelForm):
    """ Form for Prototypes """

    def __init__(self, user, *args, **kwargs):
        """
        Run the init of forms.Form and add a TextArea-Widget to the Text-Field.

        Arguments:
        user -- the current user (get it via request.user)
        instance -- the object the form is related to
        *args -- arguments to be passed on
        **kwargs -- keyword arguments to be passed on
        """
        super(PrototypeForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget = forms.Textarea(attrs={})

    class Meta:
        """ The model is Prototype and use all fields. """
        model = Prototype
        fields = ('title', 'text', 'badge', 'icon')


class AchievementForm(forms.ModelForm):
    """ Form for Achievements """

    def __init__(self, user, *args, **kwargs):
        """
        Run the init of forms.Form and add a TextArea-Widget to the Text-Field.

        Arguments:
        user -- the current user (get it via request.user)
        instance -- the object the form is related to
        *args -- arguments to be passed on
        **kwargs -- keyword arguments to be passed on
        """
        super(AchievementForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget = forms.Textarea(attrs={})

    class Meta:
        """ The model is Achievement and use all fields. """
        model = Achievement
        fields = ('user', 'prototype', 'text')
