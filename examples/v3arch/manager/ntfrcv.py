# Notification Receiver (TRAP/INFORM)
from pysnmp.entity import engine, config
from pysnmp.carrier.asynsock.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv
from pysnmp import debug

# Optionally enable stdout debugging
#debug.setLogger(debug.Debug('all'))

# Create SNMP engine with autogenernated engineID and pre-bound
# to socket transport dispatcher
snmpEngine = engine.SnmpEngine()

# Setup transport endpoint
config.addSocketTransport(
    snmpEngine,
    udp.domainName,
    udp.UdpSocketTransport().openServerMode(('127.0.0.1', 162))
    )

# v1/2 setup
config.addV1System(snmpEngine, 'test-agent', 'public')

# v3 setup
config.addV3User(
    snmpEngine, 'test-user',
    config.usmHMACMD5AuthProtocol, 'authkey1',
    config.usmDESPrivProtocol, 'privkey1'
#   '\x80\x00\x4f\xb8\x1c\x3d\xaf\xe6'   # ContextEngineID of
                                         # Notification Originator
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
snmpEngine.transportDispatcher.jobStarted(1) # this job would never finish
snmpEngine.transportDispatcher.runDispatcher()
