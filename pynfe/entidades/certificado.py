# -*- coding: utf-8 -*-
#
# PyNFe/pynfe/entidades/certificado.py
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

from base import Entidade

from OpenSSL import crypto

class Certificado(Entidade):
    u"""Classe abstrata responsavel por definir o modelo padrao para as demais
    classes de certificados digitais.
    
    Caso va implementar um novo formato de certificado, crie uma classe que
    herde desta."""

    def __new__(cls, *args, **kwargs):
        if cls == Certificado:
            raise Exception('Esta classe nao pode ser instanciada diretamente!')
        else:
            return super(Certificado, cls).__new__(cls, *args, **kwargs)

class CertificadoA1(Certificado):
    u"""Implementa a entidade do certificado eCNPJ A1, suportado pelo OpenSSL,
    e amplamente utilizado."""

    caminho_arquivo = None
    conteudo_x509 = None
    pasta_temporaria = '/tmp/'
    arquivo_chave = 'key.pem'
    arquivo_cert = 'cert.pem'

    def __init__(self, caminho_arquivo=None, conteudo_x509=None):
        self.caminho_arquivo = caminho_arquivo or self.caminho_arquivo
        self.conteudo_x509 = conteudo_x509 or self.conteudo_x509
    
    def separar_arquivo(self, senha, caminho_chave=None, caminho_cert=None):
        u"""Separa o arquivo de certificado em dois: de chave e de certificado,
        em arquivos temporários separados"""
        
        caminho_chave = caminho_chave or os.path.join(self.pasta_temporaria, self.arquivo_chave)
        caminho_cert = caminho_cert or os.path.join(self.pasta_temporaria, self.arquivo_cert)

        # Lendo o arquivo pfx no formato pkcs12 como binario
        pkcs12 = crypto.load_pkcs12(file(self.caminho_arquivo, 'rb').read(), senha)

        # Retorna a string decodificado da chave privada
        key_str = crypto.dump_privatekey(crypto.FILETYPE_PEM, pkcs12.get_privatekey())

        # Retorna a string decodificado do certificado
        cert_str = crypto.dump_certificate(crypto.FILETYPE_PEM, pkcs12.get_certificate())

        # Gravando a string no dicso
        file(caminho_cert, 'wb').write(cert_str)

        # Gravando a string no dicso
        file(caminho_chave, 'wb').write(key_str)

        return caminho_chave, caminho_cert

