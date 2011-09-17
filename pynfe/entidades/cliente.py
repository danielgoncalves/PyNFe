# -*- coding: utf-8 -*-
#
# PyNFe/pynfe/entidades/cliente.py
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

from base import Entidade
from pynfe.utils.flags import TIPOS_DOCUMENTO, CODIGO_BRASIL

class Cliente(Entidade):
    # Dados do Cliente
    # - Nome/Razão Social (obrigatorio)
    razao_social = str()

    # - Tipo de Documento (obrigatorio) - default CNPJ - TIPOS_DOCUMENTO
    tipo_documento = 'CNPJ'

    # - Numero do Documento (obrigatorio)
    numero_documento = str()

    # - Inscricao Estadual
    inscricao_estadual = str()

    # - Inscricao SUFRAMA
    inscricao_suframa = str()

    # - Isento do ICMS (Sim/Nao)
    isento_icms = False

    # Endereco
    # - Logradouro (obrigatorio)
    endereco_logradouro = str()

    # - Numero (obrigatorio)
    endereco_numero = str()

    # - Complemento
    endereco_complemento = str()

    # - Bairro (obrigatorio)
    endereco_bairro = str()

    # - CEP
    endereco_cep = str()

    # - Pais (seleciona de lista)
    endereco_pais = CODIGO_BRASIL

    # - UF (obrigatorio)
    endereco_uf = str()

    # - Municipio (obrigatorio)
    endereco_municipio = str()

    # - Telefone
    endereco_telefone = str()

    def __str__(self):
        return ' '.join([self.tipo_documento, self.numero_documento])

