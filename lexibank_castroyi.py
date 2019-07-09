from __future__ import unicode_literals, print_function
from collections import OrderedDict, defaultdict

import attr
from clldutils.misc import slug
from clldutils.path import Path
from clldutils.text import split_text, strip_brackets
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank.dataset import Concept, Language

from lingpy import *
from tqdm import tqdm

@attr.s
class HConcept(Concept):
    Chinese_Gloss = attr.ib(default=None)

@attr.s
class HLanguage(Language):
    Latitude = attr.ib(default=None)
    Longitude = attr.ib(default=None)


class Dataset(BaseDataset):
    id = 'castroyi'
    dir = Path(__file__).parent
    concept_class = HConcept
    language_class = HLanguage
    
    def clean_form(self, item, form):
        return form.strip().replace(' ', '_')

    def cmd_download(self, **kw):
        pass

    def cmd_install(self, **kw):

        wl = Wordlist(self.dir.joinpath('raw', 'wordlist.tsv').as_posix())
        langs = {} # need for checking later
        concepts = {}

        with self.cldf as ds:

            for concept in self.concepts:
                ds.add_concept(
                        ID=concept['ID'],
                        Name=concept['ENGLISH'],
                        Chinese_Gloss=concept['CHINESE'],
                        Concepticon_ID=concept['CONCEPTICON_ID'],
                        Concepticon_Gloss=concept['CONCEPTICON_GLOSS']
                        )
                concepts[concept['ENGLISH']] = concept['ID']
            for language in self.languages:
                ds.add_language(
                        ID=language['ID'],
                        Glottocode=language['Glottolog'],
                        Name=language['Name'],
                        Latitude=language['Latitude'],
                        Longitude=language['Longitude']
                        )
                langs[language['Name']] = language['ID']

            ds.add_sources(*self.raw.read_bib())
            
            for idx in tqdm(wl, desc='cldfify'):
                 ds.add_lexemes(
                    Language_ID=langs[wl[idx, 'doculect']],
                    Parameter_ID=concepts[wl[idx, 'concept']],
                    Value=wl[idx, 'value'],
                    Form=wl[idx, 'form'],
                    Segments=wl[idx, 'tokens'],
                    Source=['Castro2010']
                    )



