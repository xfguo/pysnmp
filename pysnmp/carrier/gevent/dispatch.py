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

from pysnmp.carrier.base import AbstractTransportDispatcher

class GeventDispatcher(AbstractTransportDispatcher):
    def __init__(self):
        self.timeout = 0.5
        AbstractTransportDispatcher.__init__(self)
        self.transport = None

    def registerTransport(self, tDomain, t):
        AbstractTransportDispatcher.registerTransport(self, tDomain, t)
        self.transport = t

    def unregisterTransport(self, tDomain):
        AbstractTransportDispatcher.unregisterTransport(self, tDomain)
        self.transport = None

    def runDispatcher(self, timeout=0.0):
        # FIXME: we only support one transport, we should listen all of the transport in each coroutine, 
        #        and commuicate with gevent.queue
        while self.jobsArePending():
            self.transport.loop(timeout and timeout or self.timeout, self.handleTimerTick, self.jobsArePending)
            
