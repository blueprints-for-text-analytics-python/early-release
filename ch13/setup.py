#!/usr/bin/python3

import sys, os

GIT_ROOT = 'https://github.com/blueprints-for-text-analytics-python/early-release/raw/master'

ON_COLAB = 'google.colab' in sys.modules
if ON_COLAB:
    BASE_DIR = "/content"
    print("You are working on Google Colab.")
    print(f'Files will be downloaded to "{BASE_DIR}".')
else:
    BASE_DIR = ".."
    print("You are working on a local system.")
    print(f'Files will be searched relative to "{BASE_DIR}".')

def universal_filename(f):
    return os.path.join(BASE_DIR, f)

if ON_COLAB:
    required_files = [
                  'settings.py',
                  'ch13/colab_requirements.txt'
    ]
    print("Downloading required files ...")
    for file in required_files:
        cmd = ' '.join(['wget', '-P', os.path.dirname(BASE_DIR+'/'+file), GIT_ROOT+'/'+file])
        print('!'+cmd)
        os.system(cmd)
