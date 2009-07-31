# Command Responder
from pysnmp.entity import engine, config
from pysnmp.entity.rfc3413 import cmdrsp, context
from pysnmp.carrier.asynsock.dgram import udp
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
    udp.UdpTransport().openServerMode(('127.0.0.1', 161))
    )

# Create and put on-line my managed object
sysDescr, = snmpEngine.msgAndPduDsp.mibInstrumController.mibBuilder.importSymbols('SNMPv2-MIB', 'sysDescr')
MibScalarInstance, = snmpEngine.msgAndPduDsp.mibInstrumController.mibBuilder.importSymbols('SNMPv2-SMI', 'MibScalarInstance')
sysDescrInstance = MibScalarInstance(
    sysDescr.name, (0,), sysDescr.syntax.clone('Example Command Responder')
    )
snmpEngine.msgAndPduDsp.mibInstrumController.mibBuilder.exportSymbols('PYSNMP-EXAMPLE-MIB', sysDescrInstance)  # add anonymous Managed Object Instance

# v1/2 setup
config.addV1System(snmpEngine, 'test-agent', 'public')

# v3 setup
config.addV3User(
    snmpEngine, 'test-user',
    config.usmHMACMD5AuthProtocol, 'authkey1',
    config.usmDESPrivProtocol, 'privkey1'
#    config.usmAesCfb128Protocol, 'privkey1'
    )

# Install default Agent configuration
#config.setInitialVacmParameters(snmpEngine)
#
# Apply initial VACM configuration to this user
#config.addVacmGroup(snmpEngine, "initial", 3, "test-user")

# Alternatively, configure VACM from the scratch
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
