#!/usr/bin/env python
#--

"""Extracteur d'informations à partir de publications.

Ce programme extrait des informations à partir de représentations
textuelles d'un ensemble de publications de papiers. Ces publications
sont de différentes catégories : conférence, journal, etc. (voir
publications.py). Le but est d'en avoir une présentation plus
structurée, pour pouvoir enregistrer ces informations en base de
données ou effectuer des traitements dessus.

Voir l'aide (extractor.py --help) pour les formats de sortie
possibles.
"""

import argparse
from itertools import chain
from corpus import PubsCorpus
from classifier import Classifier
from publications import ConferencePub, JournalPub, RevuePub
import pprinter

__author__ = "Anas Hilama, Moncef Baazet"

class Extractor(object):
    def __init__(self, classifier):
        self.classifier = classifier

    def pubs_data(self, input_gen):
        """Génére une représentation des données de chaque publication
        fournie par input_gen.
        """
        for kpub in self.classifier.get_classified(input_gen):
            yield self._get_extracted_data(kpub)
        
    def _get_extracted_data(self, kpub):
        pub_type, pub = kpub
        return pub_type(pub).extract()

        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename",
                        help="Chemin du (ou des) fichier(s) de publications",
                        nargs='*')
    parser.add_argument("-r", "--raw",
                        help="Affichage de la représentation interne des "
                        "résultats de l'extraction sur la sortie standard",
                        action="store_true")
    parser.add_argument("-o", "--output",
                        help="Sortie à utiliser pour les "
                        "résultats de l'extraction (stdout par défaut")
    parser.add_argument("-of", "--output-format",
                        help="Format des données écrites en sortie",
                        choices=["dict", "xml"],
                        default="dict")
    args = parser.parse_args()

    if args.filename:
        pubs_filens = args.filename
    else:
        pubs_filens = [input("Chemin du fichier contenant les publications: ")]

    pub_types = [ConferencePub, JournalPub, RevuePub]
    classifier = Classifier(pub_types)
    extractor = Extractor(classifier)

    pubs_gen = chain(*map(lambda f: PubsCorpus(f).get_pubs(),
                          pubs_filens))

    pp = pprinter.PrettyPrinter(args, extractor.pubs_data(pubs_gen))
    pp.print()
