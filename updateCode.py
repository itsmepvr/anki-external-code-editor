# Anki Addon 
# Addon to enable developer options for users
# Copy code(Ctrl+C) from reviewer to source HTML file created in collection.media.
# Edit source HTML file in external editor(like VSCode).
# Run directly in Anki review browser by reloading(Ctrl+S).
# just like normal browser(Chrome)
# Author: Venkata Ramana P
# <pvrreddy155@gmail.com> 
# <github.com/itsmepvr>
# Date: 13-02-20
# Modified: 29-08-20 Updated for Anki-2.1.30
# -*- mode: python ; coding: utf-8 -*-

import aqt
from aqt import mw
from PyQt5 import *
from PyQt5 import QtCore
from anki import cards
from aqt.qt import *
from anki.hooks import wrap, addHook
from aqt.reviewer import Reviewer

# Copy code from Notetype in reviewer to src file created in collection.media        
def copyCode():
    ankifolder = mw.pm.base
    profilename = mw.pm.name
    curPath = os.path.join(ankifolder, profilename)
    curPath = os.path.join(curPath, 'collection.media/'+profilename+'.html')
    # Anki html file predefined in Anki addons
    fname = curPath
    source_code = ''
    cardId = mw.reviewer.card
    noteId = mw.col.getNote(cardId.nid)
    noteId = mw.col.models.get(noteId.mid)
    for i in noteId['tmpls']:
        if mw.reviewer.state == 'question':
            source_code = i['qfmt'] 
        elif mw.reviewer.state == 'answer':
            source_code = i['afmt']
    htmlFile = open(fname, 'w+', encoding='utf-8')
    htmlFile.write(source_code)
    htmlFile.close()
    mw.col.reset() 
        
# Update Notetype code with code from src html file        
def updateCode():
    ankifolder = mw.pm.base
    profilename = mw.pm.name
    curPath = os.path.join(ankifolder, profilename)
    curPath = os.path.join(curPath, 'collection.media/'+profilename+'.html')
    # Anki html file predefined in Anki addons
    fname = curPath
    if not os.path.isfile(fname):
        h = open(fname, 'w+')
        h.close()
    # Current path => /usr/python/bin
    htmlFile = open(fname, 'r', encoding='utf-8')
    source_code = htmlFile.read()
    cardId = mw.reviewer.card
    nid = mw.col.getNote(cardId.nid)
    mid = mw.col.models.get(nid.mid)
    for i in mid['tmpls']:
        if mw.reviewer.state == 'question':
            i['qfmt'] = source_code
        elif mw.reviewer.state == 'answer':
            i['afmt'] = source_code 
    mw.col.models.save(mid)  
    if mw.reviewer.state == 'question':                        
        mw.col.reset()
        mw.moveToState('overview')
        mw.moveToState('review')
    elif mw.reviewer.state == 'answer':
        mw.col.reset()
        mw.moveToState('overview')
        mw.moveToState('review')
        mw.reviewer._showAnswer()

# Adding Reload button on menubar in Anki browser
action2 = QAction("Copy Code", mw)
action2.triggered.connect(copyCode)
action2.setShortcut("Ctrl+c")
mw.testmenu = action2
mw.form.menubar.addAction(mw.testmenu)

# Adding Reload button on menubar in Anki browser
action1 = QAction("Update Note", mw)
action1.triggered.connect(updateCode)
action1.setShortcut("Ctrl+s")
mw.testmenu = action1
mw.form.menubar.addAction(mw.testmenu)

def checkState(*args):
  if mw.state == 'review':
    action1.setVisible(True)
    action2.setVisible(True)
  else:
    action1.setVisible(False)
    action2.setVisible(False)  

addHook('beforeStateChange', checkState)  
# Anki Addon
# Addon to enable developer options for users
# Copy code(Ctrl+C) from reviewer to source HTML file created in collection.media.
# Edit source HTML file in external editor(like VSCode).
# Run directly in Anki review browser by reloading(Ctrl+S).
# just like normal browser(Chrome)
# Author: Venkata Ramana P
# <pvrreddy155@gmail.com>
# <github.com/itsmepvr>
# Date: 13-02-20
# Modified: 29-08-20 Updated for Anki-2.1.30
# -*- mode: python ; coding: utf-8 -*-

import os
from pathlib import Path

from anki.hooks import addHook
from aqt import mw
from aqt.gui_hooks import browser_will_show, webview_will_show_context_menu
from aqt.qt import *
from PyQt5 import *

browser = None


def file_name(in_previewer):
    ankifolder = mw.pm.base
    profilename = mw.pm.name
    return Path(ankifolder) / profilename / 'collection.media' / f'{model(in_previewer)["name"]}.html'


def model(in_previewer):
    if in_previewer:
        card = browser._previewer.card()
    else:
        card = mw.reviewer.card

    note = mw.col.getNote(card.nid)
    return mw.col.models.get(note.mid)


def state(in_previewer):
    if in_previewer:
        state = browser._previewer._state
    else:
        state = mw.reviewer.state
    return state


def copyCode(in_previewer=False):
    # Copy code from Notetype in reviewer to src file created in collection.media

    source_code = ''
    for i in model(in_previewer)['tmpls']:
        _state = state(in_previewer)
        if _state == 'question':
            source_code = i['qfmt']
        elif _state == 'answer':
            source_code = i['afmt']

    with open(file_name(in_previewer), 'w+', encoding='utf-8') as htmlFile:
        htmlFile.write(source_code)

    mw.col.reset()


def updateCode(in_previewer=False):
    # Update Notetype code with code from src html file

    fname = file_name(in_previewer)
    if not os.path.isfile(fname):
        h = open(fname, 'w+')
        h.close()

    # Current path => /usr/python/bin
    with open(fname, 'r', encoding='utf-8') as htmlFile:
        source_code = htmlFile.read()

    _model = model(in_previewer)
    for i in _model['tmpls']:
        _state = state(in_previewer)
        if _state == 'question':
            i['qfmt'] = source_code
        elif _state == 'answer':
            i['afmt'] = source_code

    mw.col.models.save(_model)
    mw.col.reset()

    if in_previewer:
        browser._previewer._last_state = None
        browser._previewer.render_card()
    else:
        _state = state(in_previewer)
        if _state == 'question':
            mw.moveToState('overview')
            mw.moveToState('review')
        elif _state == 'answer':
            mw.col.reset()
            mw.moveToState('overview')
            mw.moveToState('review')
            mw.reviewer._showAnswer()


# Adding Reload button on menubar in Anki browser
action2 = QAction("Copy Code", mw)
action2.triggered.connect(copyCode)
action2.setShortcut("Ctrl+c")
mw.testmenu = action2
mw.form.menubar.addAction(mw.testmenu)

# Adding Reload button on menubar in Anki browser
action1 = QAction("Update Note", mw)
action1.triggered.connect(updateCode)
action1.setShortcut("Ctrl+s")
mw.testmenu = action1
mw.form.menubar.addAction(mw.testmenu)


def checkState(*args):
    if mw.state == 'review':
        action1.setVisible(True)
        action2.setVisible(True)
    else:
        action1.setVisible(False)
        action2.setVisible(False)


addHook('beforeStateChange', checkState)


def add_context_menu_actions(webview, menu: QMenu):
    if webview.title != 'previewer':
        return

    action = QAction("Get code", menu)
    menu._foo_action = action
    action.triggered.connect(lambda: copyCode(in_previewer=True))
    menu.addAction(action)

    action = QAction("Update code", menu)
    menu._foo_action = action
    action.triggered.connect(lambda: updateCode(in_previewer=True))
    menu.addAction(action)


webview_will_show_context_menu.append(add_context_menu_actions)


def set_browser_variable(_browser):
    global browser
    browser = _browser


browser_will_show.append(set_browser_variable)

