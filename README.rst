===================
treeio-achievements
===================

treeio-achievements is a module for Tree.io (http://tree.io) that allows you to
distribute Achievements among the users.
It is completely integrated and even comes with a widget to dispay the last
three Achievements that were given out.

Installation
============

Sadly, the installation is pretty complex. This assumes you already have
Tree.io running.

 1. run ``pip install treeio-achievements``
 #. add ``achievements`` to your ``INSTALLED_APPS``
 #. add the following line to your urls.py: 
 	``(r'^achievements/', include('achievements.urls')),``
 #. run ``python manage.py migrate achievements``
	
And that should do the trick.

Have fun!

Author: Pascal Mouret