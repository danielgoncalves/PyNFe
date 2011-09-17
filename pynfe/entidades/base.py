# -*- coding: utf-8 -*-
#
# PyNFe/pynfe/entidades/base.py
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

class Entidade(object):
    _fonte_dados = None

    def __init__(self, **kwargs):
        # Codigo para dinamizar a criacao de instancias de entidade,
        # aplicando os valores dos atributos na instanciacao
        for k, v in kwargs.items():
            setattr(self, k, v)

        # Adiciona o objeto à fonte de dados informada
        if not self._fonte_dados:
            from fonte_dados import _fonte_dados
            self._fonte_dados = _fonte_dados

        self._fonte_dados.adicionar_objeto(self)

    def __repr__(self):
        return '<%s %s>'%(self.__class__.__name__, str(self))

class Lote(object):
    pass

