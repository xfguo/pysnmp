# GETNEXT Command Generator
from twisted.internet import reactor, defer
from pysnmp.entity import engine, config
from pysnmp.carrier.twisted import dispatch
from pysnmp.carrier.twisted.dgram import udp
from pysnmp.entity.rfc3413.twisted import cmdgen
from pyasn1.type import univ

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

def receiveResponse(cbCtx):
    (errorIndication, errorStatus, errorIndex, varBindTable) = cbCtx
    if errorIndication:
        print('Error: %s' % errorIndication)
        reactor.stop()
        return
    if errorStatus and errorStatus != 2:
        print('%s at %s' % (
            errorStatus.prettyPrint(),
            errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
            )
        )
        reactor.stop()
        return
    for varBindRow in varBindTable:
        for oid, val in varBindRow:
            print('%s = %s' % (oid.prettyPrint(), val.prettyPrint()))

    for o, v in varBindTable[-1]:
        if not isinstance(v, univ.Null):
            break
    else:
        reactor.stop()  # no more objects available
        return

    df = defer.Deferred()
    df.addCallback(receiveResponse)
    return df  # this is to indicate that we wish to continue walking

nextCmdGen = cmdgen.NextCommandGenerator()

df = nextCmdGen.sendReq(
    snmpEngine, 'myRouter', (((1,3,6,1,2,1,1), None),)
    )

df.addCallback(receiveResponse)

reactor.run()
