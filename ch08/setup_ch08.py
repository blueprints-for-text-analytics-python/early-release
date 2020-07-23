#!/usr/bin/python3

import sys, os

GIT_ROOT = 'https://github.com/blueprints-for-text-analytics-python/early-release'

# this is generic, maybe externalize?
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



DEBATES_FILENAME = os.path.join('data', 'un-general-debates', 'un-general-debates-blueprint.csv.gz')
DEBATES_FILE = universal_filename(DEBATES_FILENAME)

if ON_COLAB:
    # there are some generic files, maybe externalize?
    required_files = [
                  'settings.py',
                  DEBATES_FILENAME,
                  'ch08/colab_requirements.txt'
    ]
    print("Downloading required files ...")
    for file in required_files:
        cmd = ['wget', '-P', os.path.dirname(BASE_DIR+'/'+file), GIT_ROOT+'/'+file]
        print('!'+' '.join(cmd))
        os.system(cmd)


