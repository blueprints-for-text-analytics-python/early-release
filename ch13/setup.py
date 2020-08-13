#!/usr/bin/python3

import sys, os, subprocess
from subprocess import PIPE

GIT_ROOT = 'https://github.com/blueprints-for-text-analytics-python/early-release/raw/master'

ON_COLAB = 'google.colab' in sys.modules
if ON_COLAB:
    DIR = "/content"
    print("You are working on Google Colab.")
    print(f'Files will be downloaded to "{DIR}".')
else:
    DIR = ".."
    print("You are working on a local system.")
    print(f'Files will be searched relative to "{DIR}".')

def universal_filename(f):
    return os.path.join(DIR, f)

if ON_COLAB:
    required_files = [
                  'settings.py',
                  'packages/blueprints/__init__.py',
                  'packages/blueprints/preparation.py',
                  'packages/blueprints/knowledge.py',
                  'ch13/colab_requirements.txt'
                  
    ]
    print("Downloading required files ...")
    for file in required_files:
        cmd = ' '.join(['wget', '-P', os.path.dirname(DIR+'/'+file), GIT_ROOT+'/'+file])
        print('!'+cmd)
        if os.system(cmd) != 0:
            print('  --> ERROR')
        # stdout, stderr = subprocess.Popen(cmd, stdout=PIPE, stderr=PIPE).communicate()
        # print(stderr.decode())

if ON_COLAB:
    print("\nAdditional setup ... (may take a few minutes)")
    setup_cmds = ['mkdir figures',
                  'pip install -r ch13/colab_requirements.txt',
                  'python -m spacy download en',
                  # 'python -m spacy download en_core_web_lg',
                  'git clone https://github.com/huggingface/neuralcoref.git',
                  'cd neuralcoref;sed "/spacy/d" requirements.txt > requirements.txt',
                  'cd neuralcoref;pip install -r requirements.txt;pip install -e .'
                 ]

    for cmd in setup_cmds:
        print('!'+cmd)
        if os.system(cmd) != 0:
            print('  --> ERROR')

sys.path.append(DIR + '/packages')
sys.path.append('neuralcoref')
