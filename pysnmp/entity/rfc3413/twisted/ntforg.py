from twisted.internet import reactor, defer
from pysnmp.entity.rfc3413 import ntforg
from pyasn1.compat.octets import null

class NotificationOriginator(ntforg.NotificationOriginator):
    def sendNotification(
        self,
        snmpEngine,
        notificationTarget,
        notificationName,
        additionalVarBinds=None,
        contextName=null
        ):
        df = defer.Deferred()
        ntforg.NotificationOriginator.sendNotification(
            self,
            snmpEngine,
            notificationTarget,
            notificationName,
            additionalVarBinds,
            None,
            df,
            contextName=null
            )
        return df

    def _handleResponse(
        self,
        sendRequestHandle,
        errorIndication,
        cbFun,
        cbCtx):
        cbCtx.callback((sendRequestHandle, errorIndication))
