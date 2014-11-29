#!/usr/bin/env python
#--

"""Ecrit les données en sortie dans un format adéquat.

Le format de sortie et la destination dépendent des
informations passées sur la ligne de commande. Les formats
de sortie supportés pour l'instant sont:
    - dict: Dictionnaire python transformé en chaine de
            caractères et enregistré sans modifications.
    - xml: Les données sont enregistrées sous forme d'arbre
           xml.
"""

import pprint

__author__ = "Anas Hilama, Moncef Baazet"

class PrettyPrinter(object):
    def __init__(self, cmdline_args, data_gen):
        self.args = cmdline_args
        self.data = data_gen
        self.pp = pprint.PrettyPrinter()

    def print(self):
        if self.args.raw:
            self._write_raw_data()
        else:
            if self.args.output_format == "dict":
                self._write_raw_data()
            elif self.args.output_format == "xml":
                self._write_xml()
            else:
                raise ValueError("Format de sortie {} non reconnu.".format(
                    self.args.output_format))

    def _write_raw_data(self):
        if not self.args.output:
            for d in self.data:
                self.pp.pprint(d)
        else:
            try:
                with open(self.args.output, 'w') as f:
                    for d in self.data:
                        f.write(self.pp.pformat(d))
            except (OSError, IOError):
                print("Impossible d'ouvrir le fichier {} en écriture.".format(
                    self.args.output))

    def _write_xml(self):
        """Ecrit la représentation xml des données dans self.args.output.

        On évite d'accumuler la représentation xml dans une variable pour
        l'écrite d'un coup à la fin, la consommation mémoire en souffrirait
        autrement, les documents de publications étants assez conséquents.
        """
        if not self.args.output:
            print(self._get_xml_header())
            for d in self.data:
                print(self._get_xml_from(d))
            print(self._get_xml_footer())
        else:
            try:
                with open(self.args.output, 'w') as f:
                    f.write(self._get_xml_header())
                    for d in self.data:
                        f.write(self._get_xml_from(d))
                    f.write(self._get_xml_footer())
            except (OSError, IOError):
                print("Impossible d'ouvrir le fichier {} en écriture.".format(
                    self.args.output))

    def _get_xml_from_2(self, d):
        pub = ET.Element("publication")
        pub.set("type", d["type"])
        for k, v in d.items():
            if k == "authors":
                authors_node = ET.SubElement(pub, k)
                for auth in v:
                    auth_node = ET.SubElement(authors_node, "author")
                    auth_node.text = auth
            elif k != "type":
                prop = ET.SubElement(pub, k)
                prop.text = v

        return ET.tostring(pub, encoding="unicode")

    def _get_xml_from(self, d):
        xml = "    <publication type=\"" + d["type"] + "\">\n"
        for k, v in d.items():
            if k == "authors":
                xml += "        <authors>\n"
                for auth in v:
                    xml += "            <author>" + auth + "</author>\n"
                xml += "        </authors>\n"
            elif k != "type":
                xml += "        <" + k + ">" + v + "</" + k + ">\n"
        xml += "    </publication>\n"
        return xml

    def _get_xml_header(self):
        xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml += '<publications>\n'
        return xml

    def _get_xml_footer(self):
        return '</publications>'
