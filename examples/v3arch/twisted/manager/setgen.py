# SET Command Generator
from twisted.internet import reactor, defer
from pysnmp.entity import engine, config
from pysnmp.carrier.twisted import dispatch
from pysnmp.carrier.twisted.dgram import udp
from pysnmp.entity.rfc3413.twisted import cmdgen
from pysnmp.proto import rfc1902

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
    snmpEngine, 'myRouter', config.snmpUDPDomain,
    ('127.0.0.1', 161), 'myParams'
    )

# Transport
config.addSocketTransport(
    snmpEngine,
    udp.domainName,
    udp.UdpTwistedTransport().openClientMode()
    )

# Twisted API follows

def receiveResponse((errorIndication, errorStatus, errorIndex, varBinds)):
    if errorIndication or errorStatus:
        print 'Error: ', errorIndication, errorStatus.prettyPrint(), errorIndex
        reactor.stop()
        return
    for oid, val in varBinds:
        if val is None:
            print oid.prettyPrint()
        else:
            print '%s = %s' % (oid.prettyPrint(), val.prettyPrint())
    reactor.stop()

getCmdGen = cmdgen.SetCommandGenerator()

df = getCmdGen.sendReq(
    snmpEngine, 'myRouter',
    (((1,3,6,1,2,1,1,1,0), rfc1902.OctetString('Grinch')),)
    )

df.addCallback(receiveResponse)

reactor.run()
