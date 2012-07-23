# Command Responder over Twisted transport
from pysnmp.entity import engine, config
from pysnmp.entity.rfc3413 import cmdrsp, context
from pysnmp.carrier.twisted.dgram import udp
from pysnmp.carrier.twisted import dispatch
#from pysnmp import debug

## Optional debugging ('all' enables full debugging)
#debug.setLogger(debug.Debug('io', 'dsp', 'msgproc', 'secmod', 'app'))

# Create SNMP engine with autogenernated engineID and pre-bound
# to socket transport dispatcher
snmpEngine = engine.SnmpEngine()

# Setup non-default transport dispatcher
snmpEngine.registerTransportDispatcher(dispatch.TwistedDispatcher())
#
# Transport setup
#

# UDP over IPv4
config.addSocketTransport(
    snmpEngine,
    udp.domainName,
    udp.UdpTwistedTransport().openServerMode(('127.0.0.1', 161))
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

# Configure VACM from the scratch

# default context
config.addContext(snmpEngine, '')

# allow full MIB access for each user
config.addVacmUser(snmpEngine, 1, 'my-area', 'noAuthNoPriv', (1,3,6), (1,3,6)) 
config.addVacmUser(snmpEngine, 2, 'my-area', 'noAuthNoPriv', (1,3,6), (1,3,6)) 
config.addVacmUser(snmpEngine, 3, 'usr-md5-des', 'authPriv', (1,3,6), (1,3,6)) 

#
# CommandResponder could serve multiple independent MIB trees
# selected by ContextName parameter. The default ContextName is
# an empty string, this is where SNMP engine's LCD also lives.
#
snmpContext = context.SnmpContext(snmpEngine)

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
