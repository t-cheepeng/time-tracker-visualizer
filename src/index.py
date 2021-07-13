# =============== MONKEY PATCHING FOR PYINSTALLR ==================
# Due to pyinstaller not including in flask-compress dist. during builds
# there is a need to monkey patch in the dist.
# PyInstaller provides a sys._MEIPASS attribute to find out where bundled resources exist
# We use the existence of the attribute to find if the application running is frozen
# and provide a secondary function to discover the flask-compress dist. alongside the
# pkg_resources API during runtime. If the dist. to be retrieved is flask-compress, supply it,
# otherwise, we fall back on the original pkg_resources API for discovery.
# Code section below should have no effect on dev servers since _MEIPASS does not exist on dev

import sys
import os
import pkg_resources
from collections import namedtuple

# Application is packaged
IS_FROZEN = hasattr(sys, '_MEIPASS')

# Original pkg_resources API
_true_get_distribution = pkg_resources.get_distribution
_Dist = namedtuple('_Dist', ['version'])

# Secondary function for flask-compress
def _get_distribution(dist):
    if IS_FROZEN and dist == 'flask-compress':
        return _Dist('1.9.0')
    else:
        return _true_get_distribution(dist)

pkg_resources.get_distribution = _get_distribution


# =============== END MONKEY PATCHING FOR PYINSTALLR ==================


import dash_bootstrap_components as dbc
import dash_html_components as html

from app import app
from components import Instructions, Upload, Store

app.layout = dbc.Container([
        Store.layout,
        html.H1(children='Time Tracker Visualizer'),
        html.Hr(),

        Instructions.layout,
        Upload.layout,

        html.Div(id='output-data-upload'),
    ])

if __name__ == '__main__':
    env = os.getenv('TRACKER_ENV', 'PROD')
    if env == 'DEV':
        app.run_server(debug=True)
    else:
        # Frozen app must have debug=False.
        # See https://stackoverflow.com/questions/56758159/attributeerror-frozenimporter-object-has-no-attribute-filename
        app.run_server(debug=False)
