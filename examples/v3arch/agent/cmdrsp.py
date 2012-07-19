# Command Responder
from pysnmp.entity import engine, config
from pysnmp.entity.rfc3413 import cmdrsp, context
from pysnmp.carrier.asynsock.dgram import udp, udp6, unix
#from pysnmp import debug

## Optional debugging ('all' enables full debugging)
#debug.setLogger(debug.Debug('io', 'dsp', 'msgproc', 'secmod', 'app'))

# Create SNMP engine with autogenernated engineID and pre-bound
# to socket transport dispatcher
snmpEngine = engine.SnmpEngine()


#
# Transport setup
#

# UDP over IPv4
config.addSocketTransport(
    snmpEngine,
    udp.domainName,
    udp.UdpTransport().openServerMode(('127.0.0.1', 161))
)

# UDP over IPv6
config.addSocketTransport(
    snmpEngine,
    udp6.domainName,
    udp6.Udp6Transport().openServerMode(('::1', 161))
    )

# Local domain sockets
config.addSocketTransport(
    snmpEngine,
    unix.domainName,
    unix.UnixTransport().openServerMode('/tmp/snmp-agent')
    )

#
# SNMPv1/2c setup (if you need to handle SNMPv1/v2c messages)
#

# SecurityName <-> CommunityName mapping
config.addV1System(snmpEngine, 'my-area', 'public')

#
# SNMPv3/USM setup (if you need to handle SNMPv3 messages)
#

# user: usr-md5-des, auth: MD5, priv DES
config.addV3User(
    snmpEngine, 'usr-md5-des',
    config.usmHMACMD5AuthProtocol, 'authkey1',
    config.usmDESPrivProtocol, 'privkey1'
)

# user: usr-none-none, auth: NONE, priv NONE
config.addV3User(
    snmpEngine, 'usr-none-none'
)

# user: usr-md5-none, auth: MD5, priv NONE
config.addV3User(
    snmpEngine, 'usr-md5-none',
    config.usmHMACMD5AuthProtocol, 'authkey1'
)

# user: usr-sha-aes128, auth: SHA, priv AES
config.addV3User(
    snmpEngine, 'usr-sha-aes128',
    config.usmHMACSHAAuthProtocol, 'authkey1',
    config.usmAesCfb128Protocol, 'privkey1'
)

# user: usr-md5-aes256, auth: MD5, priv AES256
config.addV3User(
    snmpEngine, 'usr-md5-aes256',
    config.usmHMACMD5AuthProtocol, 'authkey1',
    config.usmAesCfb256Protocol, 'privkey1'
)

# user: usr-md5-aes192, auth: MD5, priv AES192
config.addV3User(
    snmpEngine, 'usr-md5-aes192',
    config.usmHMACMD5AuthProtocol, 'authkey1',
    config.usmAesCfb192Protocol, 'privkey1'
)

# user: usr-md5-3des, auth: MD5, priv 3DES
config.addV3User(
    snmpEngine, 'usr-md5-3des',
    config.usmHMACMD5AuthProtocol, 'authkey1',
    config.usm3DESEDEPrivProtocol, 'privkey1'
)

#
# Access control (VACM) setup
#

# Install default Agent configuration
# Install default Agent configuration
#config.setInitialVacmParameters(snmpEngine)
#
# Apply initial VACM configuration to this user
#config.addVacmGroup(snmpEngine, "initial", 3, "usr-md5-des")

# Alternatively, configure VACM from the scratch

# default context
config.addContext(snmpEngine, '')

# allow full MIB access for each user
config.addVacmUser(snmpEngine, 1, 'my-area', 'noAuthNoPriv', (1,3,6), (1,3,6)) 
config.addVacmUser(snmpEngine, 2, 'my-area', 'noAuthNoPriv', (1,3,6), (1,3,6)) 
config.addVacmUser(snmpEngine, 3, 'usr-md5-des', 'authPriv', (1,3,6), (1,3,6)) 
config.addVacmUser(snmpEngine, 3, 'usr-none-none', 'noAuthNoPriv', (1,3,6), (1,3,6)) 
config.addVacmUser(snmpEngine, 3, 'usr-md5-none', 'authNoPriv', (1,3,6), (1,3,6)) 
config.addVacmUser(snmpEngine, 3, 'usr-sha-aes128', 'authPriv', (1,3,6), (1,3,6)) 
config.addVacmUser(snmpEngine, 3, 'usr-md5-aes256', 'authPriv', (1,3,6), (1,3,6)) 
config.addVacmUser(snmpEngine, 3, 'usr-md5-aes192', 'authPriv', (1,3,6), (1,3,6)) 
config.addVacmUser(snmpEngine, 3, 'usr-md5-3des', 'authPriv', (1,3,6), (1,3,6)) 

#
# CommandResponder could serve multiple independent MIB trees
# selected by ContextName parameter. The default ContextName is
# an empty string, this is where SNMP engine's LCD also lives.
#
snmpContext = context.SnmpContext(snmpEngine)

#
# Add our own Managed Object to default MIB tree
#

# Get a reference to defautl MIB tree instrumentation
mibInstrumController = snmpContext.getMibInstrum('')

# Create and put on-line my managed object
sysDescr, = mibInstrumController.mibBuilder.importSymbols('SNMPv2-MIB', 'sysDescr')
MibScalarInstance, = mibInstrumController.mibBuilder.importSymbols('SNMPv2-SMI', 'MibScalarInstance')
sysDescrInstance = MibScalarInstance(
    sysDescr.name, (0,), sysDescr.syntax.clone('Example Command Responder')
)
mibInstrumController.mibBuilder.exportSymbols('PYSNMP-EXAMPLE-MIB', sysDescrInstance)  # add anonymous Managed Object Instance

# Register SNMP Applications at the SNMP engine
cmdrsp.GetCommandResponder(snmpEngine, snmpContext)
cmdrsp.SetCommandResponder(snmpEngine, snmpContext)
cmdrsp.NextCommandResponder(snmpEngine, snmpContext)
cmdrsp.BulkCommandResponder(snmpEngine, snmpContext)

snmpEngine.transportDispatcher.jobStarted(1) # this job would never finish

# Run I/O dispatcher which would receive queries and send responses
try:
    snmpEngine.transportDispatcher.runDispatcher()
except:
    snmpEngine.transportDispatcher.closeDispatcher()
    raise
