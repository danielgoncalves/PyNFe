# -*- coding: utf-8 -*-
#
# PyNFe/pynfe/processamento/assinatura.py
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

import xmlsec, libxml2 # FIXME: verificar ambiguidade de dependencias: lxml e libxml2

from pynfe.utils import etree, StringIO, extrair_tag
from pynfe.utils.flags import NAMESPACE_NFE, NAMESPACE_SIG

class Assinatura(object):
    """Classe abstrata responsavel por definir os metodos e logica das classes
    de assinatura digital."""

    certificado = None
    senha = None

    def __init__(self, certificado, senha):
        self.certificado = certificado
        self.senha = senha

    def assinar_arquivo(self, caminho_arquivo):
        """Efetua a assinatura dos arquivos XML informados"""
        pass

    def assinar_xml(self, xml):
        """Efetua a assinatura numa string contendo XML valido."""
        pass

    def assinar_etree(self, raiz):
        u"""Efetua a assinatura numa instancia da biblioteca lxml.etree.
        
        Este metodo de assinatura será utilizado internamente pelos demais,
        sendo que eles convertem para uma instancia lxml.etree para somente
        depois efetivar a assinatura.
        
        TODO: Verificar o funcionamento da PyXMLSec antes de efetivar isso."""
        pass

    def assinar_objetos(self, objetos):
        """Efetua a assinatura em instancias do PyNFe"""
        pass

    def verificar_arquivo(self, caminho_arquivo):
        pass

    def verificar_xml(self, xml):
        pass

    def verificar_etree(self, raiz):
        pass

    def verificar_objetos(self, objetos):
        pass

class AssinaturaA1(Assinatura):
    """Classe abstrata responsavel por efetuar a assinatura do certificado
    digital no XML informado."""
    
    def assinar_arquivo(self, caminho_arquivo, salva=True):
        # Carrega o XML do arquivo
        raiz = etree.parse(caminho_arquivo)

        # Efetua a assinatura
        xml = self.assinar_etree(raiz, retorna_xml=True)

        # Grava XML assinado no arquivo
        if salva:
            fp = file(caminho_arquivo, 'w')
            fp.write(xml)
            fp.close()

        return xml

    def assinar_xml(self, xml):
        raiz = etree.parse(StringIO(xml))

        # Efetua a assinatura
        return self.assinar_etree(raiz, retorna_xml=True)

    def assinar_etree(self, raiz, retorna_xml=False):
        # Extrai a tag do elemento raiz
        tipo = extrair_tag(raiz.getroot())

        # doctype compatível com o tipo da tag raiz
        if tipo == u'NFe':
            doctype = u'<!DOCTYPE NFe [<!ATTLIST infNFe Id ID #IMPLIED>]>'
        elif tipo == u'inutNFe':
            doctype = u'<!DOCTYPE inutNFe [<!ATTLIST infInut Id ID #IMPLIED>]>'
        elif tipo == u'cancNFe':
            doctype = u'<!DOCTYPE cancNFe [<!ATTLIST infCanc Id ID #IMPLIED>]>'
        elif tipo == u'DPEC':
            doctype = u'<!DOCTYPE DPEC [<!ATTLIST infDPEC Id ID #IMPLIED>]>'

        # Tag de assinatura
        if raiz.getroot().find('Signature') is None:
            signature = etree.Element(
                    '{%s}Signature'%NAMESPACE_SIG,
                    URI=raiz.getroot().getchildren()[0].attrib['Id'],
                    nsmap={'sig': NAMESPACE_SIG},
                    )

            signed_info = etree.SubElement(signature, '{%s}SignedInfo'%NAMESPACE_SIG)
            etree.SubElement(signed_info, 'CanonicalizationMethod', Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315")
            etree.SubElement(signed_info, 'SignatureMethod', Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1")

            reference = etree.SubElement(signed_info, '{%s}Reference'%NAMESPACE_SIG, URI=raiz.getroot().getchildren()[0].attrib['Id'])
            transforms = etree.SubElement(reference, 'Transforms', URI=raiz.getroot().getchildren()[0].attrib['Id'])
            etree.SubElement(transforms, 'Transform', Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature")
            etree.SubElement(transforms, 'Transform', Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315")
            etree.SubElement(reference, '{%s}DigestMethod'%NAMESPACE_SIG, Algorithm="http://www.w3.org/2000/09/xmldsig#sha1")
            digest_value = etree.SubElement(reference, '{%s}DigestValue'%NAMESPACE_SIG)

            signature_value = etree.SubElement(signature, '{%s}SignatureValue'%NAMESPACE_SIG)

            key_info = etree.SubElement(signature, '{%s}KeyInfo'%NAMESPACE_SIG)
            x509_data = etree.SubElement(key_info, '{%s}X509Data'%NAMESPACE_SIG)
            x509_certificate = etree.SubElement(x509_data, '{%s}X509Certificate'%NAMESPACE_SIG)

            raiz.getroot().insert(0, signature)

        # Acrescenta a tag de doctype (como o lxml nao suporta alteracao do doctype,
        # converte para string para faze-lo)
        xml = etree.tostring(raiz, xml_declaration=True, encoding='utf-8')

        if xml.find('<!DOCTYPE ') == -1:
            pos = xml.find('>') + 1
            xml = xml[:pos] + doctype + xml[pos:]
            #raiz = etree.parse(StringIO(xml))

        doc_xml, ctxt, noh_assinatura, assinador = self._antes_de_assinar_ou_verificar(raiz)
        
        # Realiza a assinatura
        assinador.sign(noh_assinatura)
    
        # Coloca na instância Signature os valores calculados
        digest_value.text = ctxt.xpathEval(u'//sig:DigestValue')[0].content.replace(u'\n', u'')
        signature_value.text = ctxt.xpathEval(u'//sig:SignatureValue')[0].content.replace(u'\n', u'')
        
        # Provavelmente retornarão vários certificados, já que o xmlsec inclui a cadeia inteira
        certificados = ctxt.xpathEval(u'//sig:X509Data/sig:X509Certificate')
        x509_certificate.text = certificados[len(certificados)-1].content.replace(u'\n', u'')
    
        resultado = assinador.status == xmlsec.DSigStatusSucceeded

        # Gera o XML para retornar
        xml = doc_xml.serialize()

        # Limpa objetos da memoria e desativa funções criptográficas
        self._depois_de_assinar_ou_verificar(doc_xml, ctxt, assinador)

        if retorna_xml:
            return xml
        else:
            return etree.parse(StringIO(xml))

    def _ativar_funcoes_criptograficas(self):
        # FIXME: descobrir forma de evitar o uso do libxml2 neste processo

        # Ativa as funções de análise de arquivos XML FIXME
        libxml2.initParser()
        libxml2.substituteEntitiesDefault(1)
        
        # Ativa as funções da API de criptografia
        xmlsec.init()
        xmlsec.cryptoAppInit(None)
        xmlsec.cryptoInit()
    
    def _desativar_funcoes_criptograficas(self):
        ''' Desativa as funções criptográficas e de análise XML
        As funções devem ser chamadas aproximadamente na ordem inversa da ativação
        '''
        
        # Shutdown xmlsec-crypto library
        xmlsec.cryptoShutdown()
        
        # Shutdown crypto library
        xmlsec.cryptoAppShutdown()
        
        # Shutdown xmlsec library
        xmlsec.shutdown()
        
        # Shutdown LibXML2 FIXME: descobrir forma de evitar o uso do libxml2 neste processo
        libxml2.cleanupParser()

    def verificar_arquivo(self, caminho_arquivo):
        # Carrega o XML do arquivo
        raiz = etree.parse(caminho_arquivo)
        return self.verificar_etree(raiz)

    def verificar_xml(self, xml):
        raiz = etree.parse(StringIO(xml))
        return self.verificar_etree(raiz)

    def verificar_etree(self, raiz):
        doc_xml, ctxt, noh_assinatura, assinador = self._antes_de_assinar_ou_verificar(raiz)

        # Verifica a assinatura
        assinador.verify(noh_assinatura)
        resultado = assinador.status == xmlsec.DSigStatusSucceeded

        # Limpa objetos da memoria e desativa funções criptográficas
        self._depois_de_assinar_ou_verificar(doc_xml, ctxt, assinador)

        return resultado

    def _antes_de_assinar_ou_verificar(self, raiz):
        # Converte etree para string
        xml = etree.tostring(raiz, xml_declaration=True, encoding='utf-8')

        # Ativa funções criptográficas
        self._ativar_funcoes_criptograficas()

        # Colocamos o texto no avaliador XML FIXME: descobrir forma de evitar o uso do libxml2 neste processo
        doc_xml = libxml2.parseMemory(xml, len(xml))
    
        # Cria o contexto para manipulação do XML via sintaxe XPATH
        ctxt = doc_xml.xpathNewContext()
        ctxt.xpathRegisterNs(u'sig', NAMESPACE_SIG)
    
        # Separa o nó da assinatura
        noh_assinatura = ctxt.xpathEval(u'//*/sig:Signature')[0]
    
        # Buscamos a chave no arquivo do certificado
        chave = xmlsec.cryptoAppKeyLoad(
                filename=str(self.certificado.caminho_arquivo),
                format=xmlsec.KeyDataFormatPkcs12,
                pwd=str(self.senha),
                pwdCallback=None,
                pwdCallbackCtx=None,
                )
    
        # Cria a variável de chamada (callable) da função de assinatura
        assinador = xmlsec.DSigCtx()
    
        # Atribui a chave ao assinador
        assinador.signKey = chave

        return doc_xml, ctxt, noh_assinatura, assinador

    def _depois_de_assinar_ou_verificar(self, doc_xml, ctxt, assinador):
        # Libera a memória do assinador; isso é necessário, pois na verdade foi feita uma chamada
        # a uma função em C cujo código não é gerenciado pelo Python
        assinador.destroy()
        ctxt.xpathFreeContext()
        doc_xml.freeDoc()

        # E, por fim, desativa todas as funções ativadas anteriormente
        self._desativar_funcoes_criptograficas()
