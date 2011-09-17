# -*- coding: utf-8 -*-
#
# PyNFe/pynfe/processamento/validacao.py
#
# Projeto PyNFe
# Copyright (C) 2010 Marinho Brandão et al
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
#

from os import path

try:
    from lxml import etree
except ImportError:
    try:
        # Python 2.5 - cElementTree
        import xml.etree.cElementTree as etree
    except ImportError:
        try:
            # Python 2.5 - ElementTree
            import xml.etree.ElementTree as etree
        except ImportError:
            try:
                # Instalacao normal do cElementTree
                import cElementTree as etree
            except ImportError:
                try:
                    # Instalacao normal do ElementTree
                    import elementtree.ElementTree as etree
                except ImportError:
                    raise Exception('Falhou ao importar lxml/ElementTree')

XSD_FOLDER = "pynfe/data/XSDs/"

XSD_NFE="nfe_v1.10.xsd"
XSD_NFE_PROCESSADA="procNFe_v1.10.xsd"
XSD_PD_CANCELAR_NFE="procCancNFe_v1.07.xsd"
XSD_PD_INUTILIZAR_NFE="procInutNFe_v1.07.xsd"

def get_xsd(xsd_file):
    """Retorna o caminho absoluto para um arquivo xsd.
    Argumentos:
        xsd_file - nome do arquivo xsd (utilizar nomes definidos em validacao.py)
    """
    return path.abspath(path.join(XSD_FOLDER, xsd_file))

class Validacao(object):
    '''Valida documentos xml a partir do xsd informado.'''
    
    def __init__(self):
        self.clear_cache()
    
    def clear_cache(self):
        self.MEM_CACHE = {}
    
    def validar_xml(self, xml_path, xsd_file, use_assert=False):
        '''Valida um arquivo xml.
        Argumentos:
            xml_path - caminho para arquivo xml
            xsd_file - caminho para o arquivo xsd
            use_assert - levantar exceção caso documento não valide?
        '''
        return self.validar_etree(etree.parse(xml_path), xsd_file, use_assert)
    
    def validar_etree(self, xml_doc, xsd_file, use_assert=False):
        '''Valida um documento lxml diretamente.
        Argumentos:
            xml_doc - documento etree
            xsd_file - caminho para o arquivo xsd
            use_assert - levantar exceção caso documento não valide?
        '''
        xsd_filepath = get_xsd(xsd_file)
        
        try:
            # checa se o schema ja existe no cache
            xsd_schema = self.MEM_CACHE[xsd_filepath]
        except:
            # lê xsd e atualiza cache
            xsd_doc = etree.parse(xsd_filepath)
            xsd_schema = etree.XMLSchema(xsd_doc)
            self.MEM_CACHE[xsd_file] = xsd_schema
        return use_assert and xsd_schema.assertValid(xml_doc) \
               or xsd_schema.validate(xml_doc)
