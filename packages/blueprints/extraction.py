import pandas as pd
import spacy
from spacy.tokens import Span
import stanza
from spacy_stanza import StanzaLanguage


def display_ner(doc, include_punct=False):
    """Generate data frame for visualization of spaCy doc with custom attributes."""

    rows = []
    for i, t in enumerate(doc):
        if not t.is_punct or include_punct:
            row = {'token': i, 
                   'text': t.text, 'lemma': t.lemma_, 
                   'pos': t.pos_, 'dep': t.dep_, 'ent_type': t.ent_type_}
            if t.has_extension('in_coref') and t._.in_coref: # neuralcoref attributes
                row['in_coref'] = t._.in_coref
                row['main_coref'] = t._.coref_clusters[0].main.text
            if t.has_extension('ref_n'): # name_coref attribute
                row['ref_n'] = t._.ref_n
                row['ref_t'] = t._.ref_t
            if t.has_extension('ref_ent'): # ref_n/ref_t
                row['ref_ent'] = t._.ref_ent
            rows.append(row)
    
    df = pd.DataFrame(rows).set_index('token')
    df.index.name = None
    
    return df


def norm_entities(doc):
    """Normalize entities by dropping the determiner"""
    ents = []
    for ent in doc.ents:
        if ent[0].lemma_ in ['the', 'a', 'an']: # first token is article
            ent = Span(doc, ent.start + 1, ent.end, label=ent.label)
        ents.append(ent)
    doc.ents = ents
    return doc


def spacy_load(lang, use_stanza=False):
    """Instantiate spacy resp. stanza pipeline and add
    'normalize_entities' and 'merge_entities'"""

    if use_stanza:
        if lang=='en':
            snlp = stanza.Pipeline(lang, processors={'tokenize': 'spacy'})
        else:
            snlp = stanza.Pipeline(lang)
        nlp = StanzaLanguage(snlp) 
    else:
        nlp = spacy.load(lang)
        
    nlp.add_pipe(norm_entities)
    nlp.add_pipe(nlp.create_pipe("merge_entities"))

    return nlp


def print_dep_tree(doc, skip_punct=True):
    """Utility function to pretty print the dependency tree."""
    
    def print_recursive(root, indent, skip_punct):
        if not root.dep_ == 'punct' or not skip_punct:
            print(" "*indent + f"{root} [{root.pos_}, {root.dep_}]")
        for left in root.lefts:
            print_recursive(left, indent=indent+4, skip_punct=skip_punct)
        for right in root.rights:
            print_recursive(right, indent=indent+4, skip_punct=skip_punct)

    for sent in doc.sents: # iterate over all sentences in a doc
        print_recursive(sent.root, indent=0, skip_punct=skip_punct) 
