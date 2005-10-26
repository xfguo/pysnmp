"""Notification Receiver Application (TRAP/INFORM PDU)"""
from pysnmp.entity import engine, config
from pysnmp.carrier.asynsock.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv

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
#    '80004fb81c3dafe69'   # ContextEngineID of Notification Originator
    )
    
# Callback function for receiving notifications
def cbFun(snmpEngine,
          contextEngineId, contextName,
          varBinds,
          cbCtx):
    print 'Notification from SNMP Engine \"%s\", Context \"%s\"' % (
        contextEngineId, contextName
        )
    for name, val in varBinds:
        print '%s = %s' % (name.prettyPrint(), val.prettyPrint())

# Apps registration
ntfrcv.NotificationReceiver(snmpEngine, cbFun)
snmpEngine.transportDispatcher.jobStarted(1) # this job would never finish
snmpEngine.transportDispatcher.runDispatcher()
