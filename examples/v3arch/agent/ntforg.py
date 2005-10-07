from pysnmp.entity import engine, config
from pysnmp.carrier.asynsock.dgram import udp
from pysnmp.entity.rfc3413 import ntforg

snmpEngine = engine.SnmpEngine()

# v1/2 setup
config.addV1System(snmpEngine, 'test-agent', 'public')

# v3 setup
config.addV3User(
    snmpEngine, 'test-user',
    config.usmHMACMD5AuthProtocol, 'authkey1',
    config.usmDESPrivProtocol, 'privkey1'
    )

# Transport params
config.addTargetParams(snmpEngine, 'myParams', 'test-user', 'authPriv')
#config.addTargetParams(snmpEngine, 'myParams', 'test-agent', 'noAuthNoPriv', 1)

# Transport addresses
config.addTargetAddr(
    snmpEngine, 'myNMS', config.snmpUDPDomain,
    ('127.0.0.1', 162), 'myParams', tagList='myManagementStations'
    )

# Notification targets
config.addNotificationTarget(
    snmpEngine, 'myNotifyName', 'myParams', 'myManagementStations'
    )

# Setup transport endpoint
config.addSocketTransport(
    snmpEngine,
    udp.domainName,
    udp.UdpSocketTransport().openClientMode()
    )

def cbFun(sendRequestHandle, errorIndication, errorStatus, errorIndex,
          varBinds, cbCtx):
    return
    
ntforg.NotificationOriginator().sendNotification(
    snmpEngine, 'myNotifyName', (1,3,6),(), '', cbFun # XXX coldStart
    )

snmpEngine.transportDispatcher.runDispatcher()
