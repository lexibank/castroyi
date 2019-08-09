from __future__ import unicode_literals, print_function
from collections import OrderedDict, defaultdict

import attr
from clldutils.misc import slug
from clldutils.path import Path
from clldutils.text import split_text, strip_brackets
from pylexibank.dataset import NonSplittingDataset as BaseDataset
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
    SubGroup = attr.ib(default="Nesu")
    Family = attr.ib(default="Sino-Tibetan")


class Dataset(BaseDataset):
    id = 'castroyi'
    dir = Path(__file__).parent
    concept_class = HConcept
    language_class = HLanguage
    
    def cmd_download(self, **kw):
        pass

    def cmd_install(self, **kw):

        wl = Wordlist(self.dir.joinpath('raw', 'yi-wl.tsv').as_posix())
        langs = {} # need for checking later
        concepts = {}

        with self.cldf as ds:

            for concept in self.conceptlist.concepts.values():
                ds.add_concept(
                        ID=concept.id,
                        Name=concept.english,
                        Chinese_Gloss=concept.attributes['chinese'],
                        Concepticon_ID=concept.concepticon_id,
                        Concepticon_Gloss=concept.concepticon_gloss
                        )
                concepts[concept.english] = concept.id
            concepts['Daughter-in-law'] = concepts['daughter-in-law']
            langs = {k['Name']: k['ID'] for k in self.languages}
            ds.add_languages()
            ds.add_sources(*self.raw.read_bib())
            
            for idx in tqdm(wl, desc='cldfify'):
                 ds.add_segments(
                    Language_ID=langs[wl[idx, 'doculect']],
                    Parameter_ID=concepts[wl[idx, 'concept']],
                    Value=wl[idx, 'value'],
                    Form= wl[idx, 'form'],
                    Segments=wl[idx, 'tokens'],
                    Source=['Castro2010']
                    )



