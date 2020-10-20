import pathlib

appGlobals = {}

def init():
    global appGlobals
    appGlobals['app_root'] = pathlib.Path(__file__).parent.absolute()
    appGlobals['ml_models'] = {}