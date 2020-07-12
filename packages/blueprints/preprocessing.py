import re
import html

# tags like <tab>
RE_TAG = re.compile(r'<[^<>]*>')
# markdown URLs, like [Some text](https://....)
RE_MD_URL = re.compile('\[([^\[\]]*)\]\([^\(\)]*\)')
# text or code in brackets like [0]
RE_BRACKET = re.compile('\[[^\[\]]*\]')
# standalone sequences of specials, matches &# but not #cool
RE_SPECIAL = re.compile(r'(?:^|\s)[&#<>{}\[\]+|\\:-]{1,}(?:\s|$)')
# standalone sequences of hyphens like --- or ==
RE_HYPHEN_SEQ = re.compile(r'(?:^|\s)[\-=\+]{2,}(?:\s|$)')
# sequences of white spaces
RE_MULTI_SPACE = re.compile('\s+')

def clean(text):
    # convert html escapes like &amp; to characters.
    text = html.unescape(text)
    text = RE_TAG.sub(' ', text)
    text = RE_MD_URL.sub(r'\1', text)
    text = RE_BRACKET.sub(' ', text)
    text = RE_SPECIAL.sub(' ', text)
    text = RE_HYPHEN_SEQ.sub(' ', text)
    text = RE_MULTI_SPACE.sub(' ', text)
    return text.strip()
    
    

import spacy    
from IPython.core.display import display, HTML
from tabulate import tabulate

def display_nlp(doc, include_punct=False):
    """Print tokens with attributes for spaCy doc."""
    rows = []
    for token in doc:
        if not token.is_punct or include_punct:
            row = (token.text, token.lemma_, 
                   token.pos_, token.tag_, token.dep_,
                   token.is_punct, token.is_alpha, token.is_stop,
                   token.ent_type_, token.ent_iob_)
            rows.append(row)

    # generate HTML formatted table for display in Jupyter
    headers = ['text', 'lemma_', 'pos_', 'tag_', 'dep_', 
               'is_punct', 'is_alpha', 'is_stop', 'ent_type', 'ent_iob'] 
    display(HTML(tabulate(rows, headers=headers, tablefmt='html')))
