# -*- coding: utf-8 -*-
#
# PyNFe/run_tests.py
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

import doctest
import glob
import os
import sys

from getopt import gnu_getopt as getopt

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CUR_DIR)

if __name__ == '__main__':

    run_level = None
    
    optlist, args = getopt(sys.argv[1:], "l:", ['--level='])
    for opt, arg in optlist:
        if opt in ("-l", "--list"):
            run_level = arg.zfill(2)
    
    # determina a máscara dos nomes dos arquivos que serão
    # submetidos aos testes
    if run_level is None:
        # todos os arquivos de texto da pasta ``tests`` serão testados
        search_path = '%s/*.txt' % os.path.join(CUR_DIR, 'tests')
    else: 
        # apenas os arquivos que iniciam com o valor de ``run_level``
        # serão submetidos a testes (eg. ``04-servidor-soap.txt``)
        search_path = '%s/%s-*.txt' % (
                os.path.join(CUR_DIR, 'tests'), run_level)
    
    # obtém uma lista de todos os nomes de arquivos (sem o caminho)
    # que serão testados via ``doctest``
    test_files = [os.path.split(f)[-1] for f in glob.glob(search_path)]

    # executa os testes
    for fname in test_files:
        print 'Running "%s"...' % os.path.splitext(fname)[0]
        doctest.testfile(fname)

    print 'Finished!'

