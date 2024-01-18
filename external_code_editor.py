# Anki Addon
# Copy code(Ctrl+C) from reviewer/previewer to source HTML file created in collection.media/output_path in config.
# Edit source HTML file in external editor(like VSCode).
# Update and run directly in Anki reviewer/previewer by reloading(Ctrl+S).
# Author: Venkata Ramana P
# <github.com/itsmepvr>
# Date: 13-02-20
# Modified: 29-08-20 Updated for Anki-2.1.30
# Modified: 17-09-21 Updated to work in preview
# Modified: 14-08-23 Updated for Anki-2.1.65
# -*- mode: python ; coding: utf-8 -*-

import os
from pathlib import Path
import subprocess
import platform
import time

from anki.hooks import addHook
from aqt import mw
from aqt.gui_hooks import browser_will_show, webview_will_show_context_menu
from aqt.qt import *
from aqt.utils import tooltip
from anki import version as anki_version

browser = None
# config
config = mw.addonManager.getConfig(__name__)


# file name -> note_name.html
def file_name(in_previewer):
    if config['output_path']:
        output_path = config['output_path']
    else:
        output_path = os.path.join(
            mw.pm.base, mw.pm.name, 'collection.media', f'{mw.pm.name}.html')
    return output_path


# get notetype -> review/preview
def model(in_previewer):
    if in_previewer:
        card = browser._previewer.card()
    else:
        card = mw.reviewer.card

    note = mw.col.get_note(card.nid)
    return mw.col.models.get(note.mid)


# get state -> review/preview
def state(in_previewer):
    if in_previewer:
        state = browser._previewer._state
    else:
        state = mw.reviewer.state
    return state


# Copy code from card in reviewer to file created in output path
def copyCode(in_previewer=False):
    source_code = ''
    for i in model(in_previewer)['tmpls']:
        _state = state(in_previewer)
        if _state == 'question':
            source_code = i['qfmt']
        elif _state == 'answer':
            source_code = i['afmt']
        break

    with open(file_name(in_previewer), 'w+', encoding='utf-8') as htmlFile:
        htmlFile.write(source_code)

    tooltip('Copying current note code..')


# Update Notetype code with code from src html file
def updateCode(in_previewer=False):
    fname = file_name(in_previewer)
    if not os.path.isfile(fname):
        tooltip('File not found. Copy code first to creat a file to update')
        return

    tooltip('Updating current note code..')
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

    try:
        mw.col.models.update_dict(_model)
    except:
        mw.col.models.save(_model)

    if in_previewer:
        browser._previewer._last_state = None
        browser._previewer.render_card()
    else:
        _state = state(in_previewer)
        if _state == 'question':
            mw.moveToState('review')
        elif _state == 'answer':
            mw.moveToState('review')
            mw.reviewer._showAnswer()


# open the saved file in vscode, If not vscode open in default editor
def open_file():
    file_path = file_name(False)
    if not os.path.isfile(file_path):
        tooltip('File not found. Please copy code first to create file')
        return
    try:
        if not config['editor']:
            tooltip('Opening file in VSCode..')
            # Try opening the file in VSCode
            subprocess.run(["code", file_path])
            print(f"File '{file_path}' opened in VSCode.")
        else:
            tooltip('Opening file in VSCode..')
            # Try opening the file in VSCode
            subprocess.run([config['editor'], file_path])
            print(f"File '{file_path}' opened in {config['editor']}.")
    except FileNotFoundError:
        try:
            # If VSCode is not found, try opening the file with the default editor
            if platform.system() == "Darwin":
                subprocess.run(["open", file_path])
            elif platform.system() == "Windows":
                subprocess.run(["start", file_path], shell=True)
            else:
                subprocess.run(["xdg-open", file_path])

            print(f"File '{file_path}' opened with the default editor.")
        except Exception as e:
            print(f"An error occurred: {e}")
            tooltip(f'Error: Could not open file. {e}')


# Adding Copy Code button on menubar in Anki browser
action2 = QAction("Copy Code", mw)
action2.triggered.connect(copyCode)
action2.setShortcut("Ctrl+c")
mw.testmenu = action2
mw.form.menubar.addAction(mw.testmenu)

# Adding Update Code button on menubar in Anki browser
action1 = QAction("Update Code", mw)
action1.triggered.connect(updateCode)
action1.setShortcut("Ctrl+s")
mw.testmenu = action1
mw.form.menubar.addAction(mw.testmenu)


# Adding Update Code button on menubar in Anki browser
action3 = QAction("Open File", mw)
action3.triggered.connect(open_file)
action3.setShortcut("Ctrl+o")
mw.testmenu = action3
mw.form.menubar.addAction(mw.testmenu)


# show contect menu only in review
def checkState(*args):
    if mw.state == 'review':
        action1.setVisible(True)
        action2.setVisible(True)
        action3.setVisible(True)
    else:
        action1.setVisible(False)
        action2.setVisible(False)
        action3.setVisible(False)


addHook('beforeStateChange', checkState)


# context menu for preview
def add_context_menu_actions(webview, menu: QMenu):
    if webview.title != 'previewer':
        return

    action = QAction("Copy Code", menu)
    menu._foo_action = action
    action.triggered.connect(lambda: copyCode(in_previewer=True))
    menu.addAction(action)

    action = QAction("Update Code", menu)
    menu._foo_action = action
    action.triggered.connect(lambda: updateCode(in_previewer=True))
    menu.addAction(action)


webview_will_show_context_menu.append(add_context_menu_actions)


def set_browser_variable(_browser):
    global browser
    browser = _browser


browser_will_show.append(set_browser_variable)
