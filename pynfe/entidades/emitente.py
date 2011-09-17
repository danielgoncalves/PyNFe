# -*- coding: utf-8 -*-
#
# PyNFe/pynfe/entidades/emitente.py
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
from pynfe.utils.flags import CODIGO_BRASIL

class Emitente(Entidade):
    # Dados do Emitente
    # - Nome/Razao Social (obrigatorio)
    razao_social = str()

    # - Nome Fantasia
    nome_fantasia = str()

    # - CNPJ (obrigatorio)
    cnpj = str()

    # - Inscricao Estadual (obrigatorio)
    inscricao_estadual = str()

    # - CNAE Fiscal
    cnae_fiscal = str()

    # - Inscricao Municipal
    inscricao_municipal = str()

    # - Inscricao Estadual (Subst. Tributario)
    inscricao_estadual_subst_tributaria = str()

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

    # - Pais (aceita somente Brasil)
    endereco_pais = CODIGO_BRASIL

    # - UF (obrigatorio)
    endereco_uf = str()

    # - Municipio (obrigatorio)
    endereco_municipio = str()

    # - Telefone
    endereco_telefone = str()

    # Logotipo
    logotipo = None

    def __str__(self):
        return self.cnpj

