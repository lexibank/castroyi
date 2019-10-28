



from pathlib import Path
from pylexibank.dataset import Dataset as BaseDataset 
from pylexibank import Concept, Language
from pylexibank.util import pb

from collections import OrderedDict, defaultdict

from lingpy import *
from clldutils.misc import slug
import attr

@attr.s
class CustomConcept(Concept):
    Chinese_Gloss = attr.ib(default=None)

@attr.s
class CustomLanguage(Language):
    Latitude = attr.ib(default=None)
    Longitude = attr.ib(default=None)
    SubGroup = attr.ib(default="Nesu")
    Family = attr.ib(default="Sino-Tibetan")


class Dataset(BaseDataset):
    id = 'castroyi'
    dir = Path(__file__).parent
    concept_class = CustomConcept
    language_class = CustomLanguage

    def cmd_makecldf(self, args):

        wl = Wordlist(self.raw_dir.joinpath('yi-wl.tsv').as_posix())
        args.writer.add_sources()
        language_lookup = args.writer.add_languages(
                lookup_factory='Name')
        concept_lookup = {}
        for concept in self.conceptlist.concepts.values():
            idx = concept.id.split('-')[-1]+'_'+slug(concept.english)
            args.writer.add_concept(
                    ID=idx,
                    Name=concept.english,
                    Concepticon_ID=concept.concepticon_id,
                    Concepticon_Gloss=concept.concepticon_gloss,
                    Chinese_Gloss = concept.attributes['chinese']
                    )
            concept_lookup[concept.english] = idx
        concept_lookup['Daughter-in-law'] = concept_lookup['daughter-in-law']
        
        for idx in pb(wl, desc='cldfify', total=len(wl)):
             args.writer.add_form_with_segments(
                Language_ID=language_lookup[wl[idx, 'doculect']],
                Parameter_ID=concept_lookup[wl[idx, 'concept']],
                Value=wl[idx, 'value'],
                Form= wl[idx, 'form'],
                Segments=wl[idx, 'tokens'],
                Source=['Castro2010']
                )



