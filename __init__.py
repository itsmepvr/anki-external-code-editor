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

# Call main function
from . import external_code_editor
