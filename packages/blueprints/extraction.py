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
            if doc._.has('coref_clusters'): # neuralcoref attributes
                row['in_coref'] = t._.in_coref
                row['main_coref'] = t._.coref_clusters[0].main.text if t._.in_coref else None
            if t._.has('referent'): # fuzzy_name_coref attribute
                row['referent'] = t._.referent.text if t._.referent is not None else None
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
