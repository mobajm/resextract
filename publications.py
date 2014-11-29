#!/usr/bin/env python
#--

"""Types de publications gérées par l'extraction.

Chaque type de publication représente un médium de publication
particulier, et possède des informations le caractérisant.

L'extraction de ces informations est faite en appelant la
méthode extract du type de publication adéquat.

Les variables de classe REGEXPS et REGEXPS_OPTS sont utilisées
par l'extracteur (voir extractor.py) pour reconnaitre un type de
publication et savoir quelles options passer au moteur de regexps
lors de la reconnaissance, respectivement. Une option '-1' dans
REGEXP_OPTS indique d'utiliser les options par défaut du moteur.
"""

import re

__author__ = "Anas Hilama, Moncef Baazet"

class Publication(object):
    # Reconnait un sigle
    REGX_SIGLE = r'\(.*?([A-Z]+).*?\)'
    # Reconnait un mois en français ou anglais
    REGX_MONTHS = r'janvier|january|f[eé]vrier|february|mars|march' \
                  + r'|april|avril|mai|may|june|juin|juillet|july' \
                  + r'|aout|august|septemb(?:er|re)|octob(?:er|re)' \
                  + r'|novemb(?:er|re)|d[eé]cemb(?:re|er)'

    def __init__(self, pub):
        self.pub = pub
        self.data = {}

    def extract(self):
        """Extraction des données attachées à la publication self.pub.

        Chaque type de publication descendant de cette classe surcharge
        cette méthode pour extraire des informations qui lui sont
        particulières. Les informations d'ordre général (que l'on retrouve
        pour tout type de publication) sont extraites ici.
        """
        self._extract_authors()
        self._extract_title()
        self._extract_date()

    def _extract_authors(self):
        # Remplacement des 'et', 'and' et ';' séparants quelques noms d'auteurs
        # par des virgules. Facilite le traitement suivant.
        self.pub = re.sub(r"([A-Z]\.[\w ]*?)(?:et|;|and)\s+([A-Z])", r"\1, \2",
                          self.pub)
        self.data['authors'] = re.findall(r"\b([A-Z](?:-[A-Z])?\.[\w\s]+)\b",
                                          self.pub)
        
    def _extract_title(self):
        res = re.search(r"(?:[A-Z](?:-[A-Z])?\.[\w\s]+[,.]\s*)+(.*?)[,;.]",
                        self.pub)
        if res:
            self.data['title'] = res.group(1)

    def _extract_sigle(self, from_where):
        sigle = re.search(Publication.REGX_SIGLE, self.data[from_where])
        if sigle:
            self.data['sigle'] = sigle.group(1)
            self.data[from_where] = re.sub(r'\(.*?[A-Z]+.*?\)', '',
                                             self.data[from_where]).strip()

    def _extract_date(self):
        date = re.search(r'\d{1,4}(?:-\d{1,2})?\s(?:'
                         + Publication.REGX_MONTHS
                         + r')?\s\d{1,4}(?:-\d{1,2})?',
                         self.pub, re.I)
        if not date:
            date = re.search(r'(?:' + Publication.REGX_MONTHS
                             + ')?[\s/(]\d{4}', self.pub, re.I)
        if date:
            self.data['date'] = re.sub(r'[^\w\d\s-]', '', date.group(0).strip())

                                            
class ConferencePub(Publication):
    REGEXPS = [r".*?\s+conf[eé]rence.*?"]
    REGEXPS_OPTS = [re.I] # Ignorer la casse

    def extract(self):
        super(ConferencePub, self).extract()
        self.data['type'] = "Conference"
        self._extract_conf_title()

        return self.data

    def _extract_conf_title(self):
        res = re.search(r"(?:International)?\sconf[eé]rence.*?[,.]",
                        self.pub, re.I)
        if res:
            self.data['conf_title'] = res.group(0).strip()
            self._extract_sigle('conf_title')

class JournalPub(Publication):
    REGEXPS = [r".*\s+journal.*?", r".*[(\s]IJ[A-Z]+.*"]
    REGEXPS_OPTS = [re.I, -1]

    def extract(self):
        super(JournalPub, self).extract()
        self.data['type'] = "Journal"
        self._extract_journal_title()
        self._extract_vol_issue()
        self._extract_pages()

        return self.data

    def _extract_journal_title(self):
        res = re.search(r'(?:(?:[A-Z](?:-[A-Z])?\.[\w\s]+[,.]\s*)+.*?[,;.])'
                        + r'(.*?journal.*?)[.,;]',
                        self.pub, re.I)
        if res:
            self.data['journal_title'] = res.group(1).strip()
            self._extract_sigle('journal_title')

    def _extract_vol_issue(self):
        vol = re.search(r'vol(?:ume)?\.?\s*(\d+)', self.pub, re.I)
        issue = re.search(r'issue\.?\s*(\d+)', self.pub, re.I)
        if vol:
            self.data['volume'] = vol.group(1)
        if issue:
            self.data['issue'] = issue.group(1)

    def _extract_pages(self):
        res = re.search(r'pp?\.?\s*(\d+(?:[^\d]+\d+))', self.pub, re.I)
        if res:
            self.data['pages'] = res.group(1).strip()

class RevuePub(Publication):
    # Regexps définissants une publication de revue
    REGEXPS = [r"\s+revue", r"\s+ISSN"]
    REGEXPS_OPTS = [re.I, -1]

    def extract(self):
        super(RevuePub, self).extract()
        self.data['type'] = "Revue"
        self._extract_revue_title()
        self._extract_issn()
        self._extract_num()
        self._extract_vol()
        self._extract_pages()
        
        return self.data

    def _extract_revue_title(self):
        res = re.search(r'(?:(?:[A-Z](?:-[A-Z])?\.[\w\s]+[,.]\s*)+.*?[,;.])'
                        + r'(.*?revue.*?)[.,;]',
                        self.pub, re.I)
        if res:
            self.data['revue_title'] = res.group(1).strip()
            self._extract_sigle('revue_title')

    def _extract_issn(self):
        res = re.search(r'ISSN[^\d]*(\d{4}-\d{4})', self.pub, re.I)
        if res:
            self.data['issn'] = res.group(1)

    def _extract_num(self):
        res = re.search(r'N°?(?:um[eé]ro)?[^\d]+(\d+)', self.pub, re.I)
        if res:
            self.data['num'] = res.group(1)

    def _extract_vol(self):
        vol = re.search(r'vol(?:ume)?\.?\s*(\d+)', self.pub, re.I)
        if vol:
            self.data['volume'] = vol.group(1)

    def _extract_pages(self):
        res = re.search(r'pp?\.?\s*(\d+(?:[^\d]+\d+))', self.pub, re.I)
        if res:
            self.data['pages'] = res.group(1).strip()
