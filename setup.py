#!/usr/bin/env python

from distutils.core import setup

setup(name="pysnmp",
      version="3.1.2",
      description="Python SNMP Toolkit",
      author="Ilya Etingof",
      author_email="ilya@glas.net ",
      url="http://sourceforge.net/projects/pysnmp/",
      packages = [ 'pysnmp',
                   'pysnmp.asn1',
                   'pysnmp.asn1.ber',
                   'pysnmp.proto',
                   'pysnmp.mapping',
                   'pysnmp.mapping.udp',
                   'pysnmp.compat',
                   'pysnmp.compat.pysnmp1x',
                   'pysnmp.compat.pysnmp2x',
                   'pysnmp.compat.snmpy' ],
      license="BSD"
      )
