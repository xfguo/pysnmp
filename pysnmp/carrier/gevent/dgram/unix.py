# 
# Copyright (C) 2012 Credo Semiconductor Inc.
# Author: Xiongfei GUO, <xfguo@credosemi.com>
#
# This work is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License Version 2 as published by the 
# Free Software Foundation.
#
# This work is distributed in the hope that it will be useful, but without
# any warranty; without even the implied warranty of merchantability or
# fitness for a particular purpose. See the GNU General Public License for 
# more details. You should have received a copy of the GNU General Public 
# License along with this program; if not, write to: Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#

import os
import random
try:
    from gevent.socket import AF_UNIX
except ImportError:
    AF_UNIX = None
from pysnmp.carrier.gevent.dgram.base import DgramGeventTransport

domainName = snmpLocalDomain = (1, 3, 6, 1, 2, 1, 100, 1, 13)

random.seed()

class UnixGeventTransport(DgramGeventTransport):
    sockFamily = AF_UNIX
    def openClientMode(self, iface=None):
        if iface is None:
            # UNIX domain sockets must be explicitly bound
            iface = ''
            while len(iface) < 8:
                iface += chr(random.randrange(65, 91))
                iface += chr(random.randrange(97, 123))
            iface = os.path.sep + 'tmp' + os.path.sep + 'pysnmp' + iface
        if os.path.exists(iface):
            os.remove(iface)
        DgramGeventTransport.openClientMode(self, iface)
        self.__iface = iface
        return self

    def openServerMode(self, iface):
        DgramGeventTransport.openServerMode(self, iface)
        self.__iface = iface
        return self

    def closeTransport(self):
        DgramGeventTransport.closeTransport(self)
        try:
            os.remove(self.__iface)
        except:
            pass

UnixTransport = UnixGeventTransport

# Compatibility stub
UnixDgramGeventTransport = UnixGeventTransport
