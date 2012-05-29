"""
The only purpose of this file is to let tree.io know that this Module has
a widget and pass on a few very basic settings.
"""
WIDGETS = {'widget_achievement_stream': {'title': 'Newest Achievements',
                                      'size': "95%"}}


def get_widgets(request):
    """ tree.io seems to anticipate this function. It is copied from another module. """
    widgets = {}
    widgets.update(WIDGETS)
    return widgets
