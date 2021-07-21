from pathlib import Path

import attr
from clldutils.misc import slug
import lingpy
import pylexibank


@attr.s
class CustomConcept(pylexibank.Concept):
    Chinese_Gloss = attr.ib(default=None)


@attr.s
class CustomLanguage(pylexibank.Language):
    SubGroup = attr.ib(default="Nesu")
    Family = attr.ib(default="Sino-Tibetan")


class Dataset(pylexibank.Dataset):
    id = "castroyi"
    dir = Path(__file__).parent
    concept_class = CustomConcept
    language_class = CustomLanguage

    def cmd_makecldf(self, args):

        wl = lingpy.Wordlist(self.raw_dir.joinpath("yi-wl.tsv").as_posix())
        args.writer.add_sources()

        languages = args.writer.add_languages(lookup_factory="Name")

        concepts = {}
        for concept in self.conceptlists[0].concepts.values():
            idx = concept.id.split("-")[-1] + "_" + slug(concept.english)
            args.writer.add_concept(
                ID=idx,
                Name=concept.english,
                Concepticon_ID=concept.concepticon_id,
                Concepticon_Gloss=concept.concepticon_gloss,
                Chinese_Gloss=concept.attributes["chinese"],
            )
            concepts[concept.english] = idx
        concepts["Daughter-in-law"] = concepts["daughter-in-law"]

        for idx in pylexibank.progressbar(wl, desc="cldfify", total=len(wl)):
            args.writer.add_form_with_segments(
                Language_ID=languages[wl[idx, "doculect"]],
                Parameter_ID=concepts[wl[idx, "concept"]],
                Value=wl[idx, "value"],
                Form=wl[idx, "form"],
                Segments=wl[idx, "tokens"],
                Source=["Castro2010"],
            )
