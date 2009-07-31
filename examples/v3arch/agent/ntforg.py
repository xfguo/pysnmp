# Notification originator
from pysnmp.entity import engine, config
from pysnmp.carrier.asynsock.dgram import udp
from pysnmp.entity.rfc3413 import ntforg, context
from pysnmp.proto.api import v2c

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
#config.addTargetParams(snmpEngine, 'myParams', 'test-agent', 'noAuthNoPriv', 0)

# Transport addresses
config.addTargetAddr(
    snmpEngine, 'myNMS', config.snmpUDPDomain,
    ('127.0.0.1', 162), 'myParams', tagList='myManagementStations'
    )

# Notification targets
config.addNotificationTarget(
#    snmpEngine, 'myNotifyName', 'myParams', 'myManagementStations', 'trap'
    snmpEngine, 'myNotifyName', 'myParams', 'myManagementStations', 'inform'
    )

# Setup transport endpoint
config.addSocketTransport(
    snmpEngine,
    udp.domainName,
    udp.UdpSocketTransport().openClientMode()
    )

# Agent-side VACM setup
config.addContext(snmpEngine, '')
config.addVacmUser(snmpEngine, 1, 'test-agent', 'noAuthNoPriv',
                   (), (), (1,3,6)) # v1
config.addVacmUser(snmpEngine, 2, 'test-agent', 'noAuthNoPriv',
                   (), (), (1,3,6)) # v2c
config.addVacmUser(snmpEngine, 3, 'test-user', 'authPriv',
                   (), (), (1,3,6)) # v3

# SNMP context
snmpContext = context.SnmpContext(snmpEngine)

def cbFun(sendRequestHandle, errorIndication, cbCtx):
    if errorIndication:
        print errorIndication
        
ntforg.NotificationOriginator(snmpContext).sendNotification(
    snmpEngine,
    # Notification targets
    'myNotifyName',
    # Trap OID (SNMPv2-MIB::coldStart)
    (1,3,6,1,6,3,1,1,5,1),
    # ((oid, value), ... )
    (((1,3,6,1,2,1,1,5), v2c.OctetString('Example Notificator')),),
    cbFun
    )

snmpEngine.transportDispatcher.runDispatcher()
