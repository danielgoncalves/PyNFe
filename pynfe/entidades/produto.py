# -*- coding: utf-8 -*-
#
# PyNFe/pynfe/entidades/produto.py
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
from pynfe.utils.flags import ICMS_TIPOS_TRIBUTACAO, ICMS_ORIGENS, ICMS_MODALIDADES

from decimal import Decimal

class Produto(Entidade):
    """XXX: E provavel que esta entidade sera descartada."""

    # Dados do Produto
    # - Descricao (obrigatorio)
    descricao = str()

    # - Codigo (obrigatorio) - nao pode ser alterado quando em edicao
    codigo = str()

    # - EAN
    ean = str()

    # - EAN Unid. Tributavel
    ean_unidade_tributavel = str()

    # - EX TIPI
    ex_tipi = str()

    # - Genero
    genero = str()

    # - NCM
    ncm = str()

    # - Unid. Com.
    unidade_comercial = str()

    # - Valor Unitario Com.
    valor_unitario_comercial = Decimal()

    # - Unid. Trib.
    unidade_tributavel = str()

    # - Qtd. Trib.
    quantidade_tributavel = Decimal()

    # - Valor Unitario Trib.
    valor_unitario_tributavel = Decimal()

    # Impostos
    # - ICMS (lista 1 para * / ManyToManyField)
    icms = None

    # - IPI
    #  - Classe de Enquadramento (cigarros e bebidas)
    ipi_classe_enquadramento = str()

    #  - Codigo de Enquadramento Legal
    ipi_codigo_enquadramento_legal = str()

    #  - CNPJ do Produtor
    ipi_cnpj_produtor = str()

    def __init__(self, *args, **kwargs):
        self.icms = []

        super(Produto, self).__init__(*args, **kwargs)

    def __str__(self):
        return ' '.join([self.codigo, self.descricao])

    def adicionar_icms(self, **kwargs):
        u"""Adiciona uma instancia de ICMS a lista de ICMS do produto"""
        self.icms.append(ProdutoICMS(**kwargs))

class ProdutoICMS(Entidade):
    #  - Tipo de Tributacao (seleciona de lista) - ICMS_TIPOS_TRIBUTACAO
    tipo_tributacao = str()

    #  - Origem (seleciona de lista) - ICMS_ORIGENS
    origem = str()

    #  - Modalidade de determinacao da Base de Calculo (seleciona de lista) - ICMS_MODALIDADES
    modalidade = str()

    #  - Aliquota ICMS
    aliquota = Decimal()

    #  - Percentual de reducao da Base de Calculo
    percentual_reducao = Decimal()

    #  - Modalidade de determinacao da Base de Calculo do ICMS ST (seleciona de lista) - ICMS_MODALIDADES
    st_modalidade = str()

    #  - Aliquota ICMS ST
    st_aliquota = Decimal()

    #  - Percentual de reducao do ICMS ST
    st_percentual_reducao = Decimal()

    #  - Percentual da margem de Valor Adicionado ICMS ST
    st_percentual_margem_valor_adicionado = Decimal()

