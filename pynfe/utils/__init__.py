# -*- coding: utf-8 -*-
#
# PyNFe/pynfe/utils/__init__.py
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

import os

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

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

import flags

from geraldo.utils import memoize

@memoize
def so_numeros(texto):
    """Retorna o texto informado mas somente os numeros"""
    return ''.join(filter(lambda c: ord(c) in range(48,58), texto))

@memoize
def obter_pais_por_codigo(codigo):
    # TODO
    if codigo == '1058':
        return 'Brasil'

CAMINHO_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
CAMINHO_MUNICIPIOS = os.path.join(CAMINHO_DATA, 'MunIBGE')

@memoize
def carregar_arquivo_municipios(uf):
    caminho_arquivo = os.path.join(
            CAMINHO_MUNICIPIOS,
            'MunIBGE-UF%s.txt'%flags.CODIGOS_ESTADOS[uf.upper()],
            )

    # Carrega o conteudo do arquivo
    fp = file(caminho_arquivo)
    linhas = list(fp.readlines())
    fp.close()

    return dict([(linha[:7], linha[7:].strip()) for linha in linhas])

@memoize
def obter_municipio_por_codigo(codigo, uf):
    # TODO: fazer UF ser opcional
    municipios = carregar_arquivo_municipios(uf)

    return municipios[codigo]

@memoize
def extrair_tag(root):
    return root.tag.split('}')[-1]

