# Notification Receiver (TRAP/INFORM)
from pysnmp.entity import engine, config
from pysnmp.carrier.asynsock.dgram import udp, udp6, unix
from pysnmp.entity.rfc3413 import ntfrcv
#from pysnmp import debug

# Optionally enable stdout debugging
#debug.setLogger(debug.Debug('all'))

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
    udp.UdpTransport().openServerMode(('127.0.0.1', 162))
)

# UDP over IPv6
config.addSocketTransport(
    snmpEngine,
    udp6.domainName,
    udp6.Udp6Transport().openServerMode(('::1', 162))
    )

# Local domain sockets
config.addSocketTransport(
    snmpEngine,
    unix.domainName,
    unix.UnixTransport().openServerMode('/tmp/snmp-manager')
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

# Callback function for receiving notifications
def cbFun(snmpEngine,
          stateReference,
          contextEngineId, contextName,
          varBinds,
          cbCtx):
    transportDomain, transportAddress = snmpEngine.msgAndPduDsp.getTransportInfo(stateReference)
    print('Notification from %s, SNMP Engine "%s", Context "%s"' % (
        transportAddress, contextEngineId.prettyPrint(),
        contextName.prettyPrint()
        )
    )
    for name, val in varBinds:
        print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))

# Apps registration
ntfrcv.NotificationReceiver(snmpEngine, cbFun)

snmpEngine.transportDispatcher.jobStarted(1) # this job would never finish

# Run I/O dispatcher which would receive queries and send confirmations
try:
    snmpEngine.transportDispatcher.runDispatcher()
except:
    snmpEngine.transportDispatcher.closeDispatcher()
    raise
