#!D:\js_workspace\covid-estimator\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'impact==0.5.9','console_scripts','impact'
__requires__ = 'impact==0.5.9'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('impact==0.5.9', 'console_scripts', 'impact')()
    )
