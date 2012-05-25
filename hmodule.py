"""
The purpose of this file is to let tree.io know a few variables, and most importantly, let's tree.io know that
this is a tree.io-module and not just any other app.
"""
PROPERTIES = {
              'title': 'Achievements',
              'details': 'The Awesomemeter of the Internet.',
              'url': '/achievements/',
              'system': False,
              'type': 'minor',
              }

URL_PATTERNS = [
                '^/achievements/',
                ]
