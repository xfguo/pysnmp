# GETNEXT Command Generator
from twisted.internet import reactor, defer
from pysnmp.entity import engine, config
from pysnmp.carrier.twisted import dispatch
from pysnmp.carrier.twisted.dgram import udp
from pysnmp.entity.rfc3413.twisted import cmdgen

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

def receiveResponse(
    (errorIndication, errorStatus, errorIndex, varBindTable),
    nextCmdGen, snmpEngine):
    if errorIndication or errorStatus:
        print 'Error: ', errorIndication, errorStatus.prettyPrint(), errorIndex
        reactor.stop()
        return
    for varBindRow in varBindTable:
        for oid, val in varBindRow:
            if val is None:
                print oid.prettyPrint()
            else:
                print '%s = %s' % (oid.prettyPrint(), val.prettyPrint())
    for oid, val in varBindTable[-1]:
        if val is not None:
            df = nextCmdGen.sendReq(
                snmpEngine, 'myRouter', varBindTable[-1]
                )
            df.addCallback(receiveResponse, nextCmdGen, snmpEngine)
            return
    else:
        reactor.stop()

nextCmdGen = cmdgen.NextCommandGenerator()

df = nextCmdGen.sendReq(
    snmpEngine, 'myRouter', (((1,3,6,1,2,1,1), None),)
    )

df.addCallback(receiveResponse, nextCmdGen, snmpEngine)

reactor.run()
