import requests
from re import sub

REVEAL_VERSION = '4.1.0'
REVEAL_URL = 'https://unpkg.com/reveal.js'
THEME = 'solarized'

r = requests.get(REVEAL_URL+'@'+REVEAL_VERSION+'/dist/theme/'+THEME+'.css', allow_redirects=True)

CSSCONTENT = r.content.decode('utf-8')

CSSCONTENT = sub(r'fdf6e3',r'2e3440',CSSCONTENT)
CSSCONTENT = sub(r'657b83',r'd8dee9',CSSCONTENT)
CSSCONTENT = sub(r'586e75',r'eceff4',CSSCONTENT)
CSSCONTENT = sub(r'268bd2',r'5e81ac',CSSCONTENT)
CSSCONTENT = sub(r'78b9e6',r'5e81ac',CSSCONTENT)
CSSCONTENT = sub(r'd33682',r'434c5e',CSSCONTENT)
CSSCONTENT = sub(r'fff',r'eceff4',CSSCONTENT)
CSSCONTENT = sub(r'\s*Impact\s*,\s*sans-serif',r' sans-serif',CSSCONTENT)
CSSCONTENT = sub(r'League Gothic',r'Nunito Sans',CSSCONTENT)
CSSCONTENT = sub(r'url(.*gothic.*)','url(https://fonts.googleapis.com/css?family=Nunito+Sans:600);',CSSCONTENT)
CSSCONTENT = sub(r'3.77em','2.55em',CSSCONTENT)
# CSSCONTENT

# @import url(https://fonts.googleapis.com/css?family=Nunito+Sans:600);

# CSSCONTENT = sub(r'')
  # --selection-background-color: #d33682;
  # --selection-color: #fff; }



OUTPUT = '../build/html/css/nord.css'

try:
    file_output = open(OUTPUT,'x')
except FileExistsError:
    file_output = open(OUTPUT,'w')


file_output.write(CSSCONTENT)

file_output.close()
