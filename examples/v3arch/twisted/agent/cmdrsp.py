# Command Responder over Twisted transport
from pysnmp.entity import engine, config
from pysnmp.entity.rfc3413 import cmdrsp, context
from pysnmp.carrier.twisted.dgram import udp
from pysnmp.carrier.twisted import dispatch

# Create SNMP engine with autogenernated engineID and pre-bound
# to socket transport dispatcher
snmpEngine = engine.SnmpEngine()

# Setup non-default transport dispatcher
snmpEngine.registerTransportDispatcher(dispatch.TwistedDispatcher())

# Setup UDP over IPv4 transport endpoint
config.addSocketTransport(
    snmpEngine,
    udp.domainName,
    udp.UdpTransport().openServerMode(('127.0.0.1', 161))
    )

# v1/2 setup
config.addV1System(snmpEngine, 'test-agent', 'public')

# v3 setup
config.addV3User(
    snmpEngine, 'test-user',
    config.usmHMACMD5AuthProtocol, 'authkey1',
    config.usmDESPrivProtocol, 'privkey1'
#    config.usmAesCfb128Protocol, 'privkey1'
    )

# Configure VACM from the scratch
config.addContext(snmpEngine, '')
config.addVacmUser(snmpEngine, 1, 'test-agent', 'noAuthNoPriv',
                   (1,3,6), (1,3,6)) # v1
config.addVacmUser(snmpEngine, 2, 'test-agent', 'noAuthNoPriv',
                   (1,3,6), (1,3,6)) # v2c
config.addVacmUser(snmpEngine, 3, 'test-user', 'authPriv',
                   (1,3,6), (1,3,6)) # v3

# SNMP context
snmpContext = context.SnmpContext(snmpEngine)

# Apps registration
cmdrsp.GetCommandResponder(snmpEngine, snmpContext)
cmdrsp.SetCommandResponder(snmpEngine, snmpContext)
cmdrsp.NextCommandResponder(snmpEngine, snmpContext)
cmdrsp.BulkCommandResponder(snmpEngine, snmpContext)
snmpEngine.transportDispatcher.jobStarted(1) # this job would never finish
snmpEngine.transportDispatcher.runDispatcher()
