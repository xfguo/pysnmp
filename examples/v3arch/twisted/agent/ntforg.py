# Notification originator
from twisted.internet import reactor
from pysnmp.entity import engine, config
from pysnmp.carrier.twisted import dispatch
from pysnmp.carrier.twisted.dgram import udp
from pysnmp.entity.rfc3413 import context
from pysnmp.entity.rfc3413.twisted import ntforg
from pysnmp.proto.api import v2c

# Send either Teap or Inform request
doInform = 1

snmpEngine = engine.SnmpEngine()

# Set Twisted dispatcher
snmpEngine.registerTransportDispatcher(dispatch.TwistedDispatcher())

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
if doInform:
    config.addNotificationTarget(
        snmpEngine, 'myNotifyName', 'myParams','myManagementStations','inform'
    )
else:
    config.addNotificationTarget(    
        snmpEngine, 'myNotifyName', 'myParams', 'myManagementStations', 'trap'
        )

# Transport
config.addSocketTransport(
    snmpEngine,
    udp.domainName,
    udp.UdpTwistedTransport().openClientMode()
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

# Twisted API follows

def receiveResponse((sendRequestHandle, errorIndication)):
    if errorIndication:
        print 'Error: ', errorIndication
    reactor.stop()
    
ntfOrg = ntforg.NotificationOriginator(snmpContext)

df = ntfOrg.sendNotification(
    snmpEngine,
    # Notification targets
    'myNotifyName',
    # Trap OID (SNMPv2-MIB::coldStart)
    (1,3,6,1,6,3,1,1,5,1),
    # ((oid, value), ... )
    (((1,3,6,1,2,1,1,5), v2c.OctetString('Example Notificator')),)
    )

if doInform:
    df.addCallback(receiveResponse)
    reactor.run()
