# Notification Receiver (TRAP/INFORM)
from twisted.internet import reactor
from pysnmp.entity import engine, config
from pysnmp.carrier.twisted import dispatch
from pysnmp.carrier.twisted.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv

# Create SNMP engine with autogenernated engineID and pre-bound
# to socket transport dispatcher
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

# Transport
config.addSocketTransport(
    snmpEngine,
    udp.domainName,
    udp.UdpTwistedTransport().openServerMode(('127.0.0.1', 162))
    )

# Callback function for receiving notifications
def cbFun(snmpEngine,
          stateReference,
          contextEngineId, contextName,
          varBinds,
          cbCtx):
    transportDomain, transportAddress = snmpEngine.msgAndPduDsp.getTransportInfo(stateReference)
    print 'Notification from %s, SNMP Engine \"%s\", Context \"%s\"' % (
        transportAddress, contextEngineId, contextName
        )
    for name, val in varBinds:
        print '%s = %s' % (name.prettyPrint(), val.prettyPrint())
        
# Apps registration
ntfrcv.NotificationReceiver(snmpEngine, cbFun)

reactor.run()
