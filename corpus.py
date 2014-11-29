#!/usr/bin/env python
#--

"""Lecture du corpus textuel constitué des publications.

On évite de tout lire en mémoire, la taille des fichiers
contenant les publications étant assez conséquente. On
utilise pour cela un générateur, qui nous permet de
travailler avec des listes paresseuses dont les éléments
ne sont calculés que lorsqu'on en a besoin.
"""

import re

__author__ = "Anas Hilama, Moncef Baazet"

class PubsCorpus(object):
    def __init__(self, file_name):
        """file_name est le chemin du fichier contenant les publications."""
        self.input_file = file_name
        
    def get_pubs(self):
        """Retourne les publications.

        Utilise une fonction génératrice pour éviter de garder
        le fichier en entier en mémoire."""
        try:
            with open(self.input_file) as f:
                for line in f:
                    yield line
        except (IOError, OSError):
            print("Impossible d'ouvrir le fichier de publications",
                  self.input_file)
