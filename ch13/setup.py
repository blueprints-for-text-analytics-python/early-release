#!/usr/bin/python3

import sys, os

GIT_ROOT = 'https://github.com/blueprints-for-text-analytics-python/early-release/raw/master'

ON_COLAB = 'google.colab' in sys.modules
if ON_COLAB:
    DIR = "/content"
    print("You are working on Google Colab.")
    print(f'Files will be downloaded to "{BASE_DIR}".')
else:
    DIR = ".."
    print("You are working on a local system.")
    print(f'Files will be searched relative to "{BASE_DIR}".')

def universal_filename(f):
    return os.path.join(DIR, f)

if ON_COLAB:
    required_files = [
                  'settings.py',
                  'packages/blueprints/__init__.py',
                  'packages/blueprints/preparation.py',
                  'packages/blueprints/extraction.py',
                  'ch13/colab_requirements.txt'
                  
    ]
    print("Downloading required files ...")
    for file in required_files:
        cmd = ' '.join(['wget', '-P', os.path.dirname(DIR+'/'+file), GIT_ROOT+'/'+file])
        print('!'+cmd)
        if os.system(cmd) != 0:
            stdout, stderr = subprocess.Popen(cmd, stdout=PIPE, stderr=PIPE).communicate()
            print(stderr.decode())

if ON_COLAB:
    print("\nAdditional setup ...")
    setup_cmds = ['pip install -r ch13/colab_requirements.txt',
                  'python -m spacy download en',
                  'python -m spacy download en_core_web_lg',
                  'git clone https://github.com/huggingface/neuralcoref.git',
                  'cd neuralcoref;sed "/spacy/d" requirements.txt > requirements.txt',
                  'cd neuralcoref;pip install -r requirements.txt;pip install -e .'
                 ]

    for cmd in setup_cmds:
        print('!'+cmd)
        if os.system(cmd) != 0:
            print('  --> ERROR')
