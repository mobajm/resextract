#!/usr/bin/env python
#--

"""Classificateur de publications.

Classifie les publications reçues suivant le médium
d'apparition de celles-ci (voir publications.py pour
les types de publications gérés.
"""

import re

__author__ = "Anas Hilama, Moncef Baazet"

class Classifier(object):
    def __init__(self, pubs_types):
        """Construit un classificateur, qui est en fait un dictionnaire
        associant à chaque expression régulière le type de publication
        qu'elle reconnait."""
        self.classtor = {}
        for pty in pubs_types:
            for i, regexp in enumerate(pty.REGEXPS):
                self.classtor[regexp] = (pty, pty.REGEXPS_OPTS[i])

    def get_classified(self, input_gen):
        """Génére, pour chaque publication fournie par input_gen,
        une représentation de cette publication classifiée, suivant
        qu'elle représente une publication de conférence, de journal, etc."""
        for pub in input_gen:
            for regxp, (pub_type, regxp_opt) in self.classtor.items():
                if regxp_opt == -1:
                    res = re.search(regxp, pub)
                else:
                    res = re.search(regxp, pub, regxp_opt)
                    
                if res:
                    yield (pub_type, pub)
                    break
