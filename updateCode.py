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
