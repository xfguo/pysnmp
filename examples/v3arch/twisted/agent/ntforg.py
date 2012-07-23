# Notification originator
from twisted.internet import reactor
from pysnmp.entity import engine, config
from pysnmp.carrier.twisted import dispatch
from pysnmp.carrier.twisted.dgram import udp
from pysnmp.entity.rfc3413 import context
from pysnmp.entity.rfc3413.twisted import ntforg
from pysnmp.proto.api import v2c
#from pysnmp import debug

## Optional debugging ('all' enables full debugging)
#debug.setLogger(debug.Debug('io', 'dsp', 'msgproc', 'secmod', 'app'))

# Send either Teap or Inform request
doInform = True

# Create SNMP engine instance
snmpEngine = engine.SnmpEngine()

# Set Twisted dispatcher
snmpEngine.registerTransportDispatcher(dispatch.TwistedDispatcher())

# SNMPv1/2c setup (if you use SNMPv1 or v2c)
#

## SecurityName <-> CommunityName mapping
config.addV1System(snmpEngine, 'my-area', 'public')

## Specify security settings per SecurityName (SNMPv1 - 0, SNMPv2c - 1)
#config.addTargetParams(snmpEngine, 'my-creds-1', 'my-area', 'noAuthNoPriv', 0)
config.addTargetParams(snmpEngine, 'my-creds-1', 'my-area', 'noAuthNoPriv', 1)

#
# SNMPv3/USM setup (choose any one if you use SNMPv3/USM)
#

# user: usr-md5-des, auth: MD5, priv DES
config.addV3User(
    snmpEngine, 'usr-md5-des',
    config.usmHMACMD5AuthProtocol, 'authkey1',
    config.usmDESPrivProtocol, 'privkey1'
)
config.addTargetParams(snmpEngine, 'my-creds-3', 'usr-md5-des', 'authPriv')

## user: usr-none-none, auth: NONE, priv NONE
#config.addV3User(
#    snmpEngine, 'usr-none-none'
#)
#config.addTargetParams(snmpEngine, 'my-creds', 'usr-none-none', 'noAuthNoPriv')

## user: usr-md5-none, auth: MD5, priv NONE
#config.addV3User(
#    snmpEngine, 'usr-md5-none',
#    config.usmHMACMD5AuthProtocol, 'authkey1'
#)
#config.addTargetParams(snmpEngine, 'my-creds', 'usr-md5-none', 'authNoPriv')

## user: usr-sha-aes128, auth: SHA, priv AES
#config.addV3User(
#    snmpEngine, 'usr-sha-aes128',
#    config.usmHMACSHAAuthProtocol, 'authkey1',
#    config.usmAesCfb128Protocol, 'privkey1'
#)
#config.addTargetParams(snmpEngine, 'my-creds', 'usr-sha-aes128', 'authPriv')

## user: usr-md5-aes256, auth: MD5, priv AES256
#config.addV3User(
#    snmpEngine, 'usr-md5-aes256',
#    config.usmHMACMD5AuthProtocol, 'authkey1',
#    config.usmAesCfb256Protocol, 'privkey1'
#)
#config.addTargetParams(snmpEngine, 'my-creds', 'usr-md5-aes256', 'authPriv')

## user: usr-md5-aes192, auth: MD5, priv AES192
#config.addV3User(
#    snmpEngine, 'usr-md5-aes192',
#    config.usmHMACMD5AuthProtocol, 'authkey1',
#    config.usmAesCfb192Protocol, 'privkey1'
#)
#config.addTargetParams(snmpEngine, 'my-creds', 'usr-md5-aes192', 'authPriv')

## user: usr-md5-3des, auth: MD5, priv 3DES
#config.addV3User(
#    snmpEngine, 'usr-md5-3des',
#    config.usmHMACMD5AuthProtocol, 'authkey1',
#    config.usm3DESEDEPrivProtocol, 'privkey1'
#)
#config.addTargetParams(snmpEngine, 'my-creds', 'usr-md5-3des', 'authPriv')

#
# Setup transport endpoint and bind it with security settings yielding
# a target name. Since Notifications could be sent to multiple Managers
# at once, more than one target entry may be configured (and tagged).
#

# UDP/IPv4
config.addSocketTransport(
    snmpEngine,
    udp.domainName,
    udp.UdpTwistedTransport().openClientMode()
)
config.addTargetAddr(
    snmpEngine, 'my-nms-1',
    udp.domainName, ('127.0.0.1', 162),
    'my-creds-1',
    tagList='all-my-managers'
)

#
# Specify what kind of notification should be sent (TRAP or INFORM)
# to what targets (chosen by tag) and with what credentials.
#
config.addNotificationTarget(
    snmpEngine, 'my-notification', 'my-creds', 'all-my-managers', doInform and 'inform' or 'trap'
)

#
# Notifications carry potentially confidential information from
# the Agent. Therefore access control is to be setup allowing
# NotificationOriginator access to certain portions of Agent MIB.
#
config.addContext(snmpEngine, '')
# SNMPv1
config.addVacmUser(snmpEngine, 1, 'my-area', 'noAuthNoPriv', (), (), (1,3,6))
# SNMPv2c
config.addVacmUser(snmpEngine, 2, 'my-area', 'noAuthNoPriv', (), (), (1,3,6))
# SNMPv3
config.addVacmUser(snmpEngine, 3, 'usr-md5-des', 'authPriv', (), (), (1,3,6)) 
config.addVacmUser(snmpEngine, 3, 'usr-md5-none', 'authPriv', (), (), (1,3,6)) 
config.addVacmUser(snmpEngine, 3, 'usr-none-none', 'authPriv', (), (), (1,3,6)) 
config.addVacmUser(snmpEngine, 3, 'usr-md5-aes192', 'authPriv', (), (),(1,3,6)) 
config.addVacmUser(snmpEngine, 3, 'usr-md5-aes256', 'authPriv', (), (),(1,3,6)) 
config.addVacmUser(snmpEngine, 3, 'usr-sha-aes128', 'authPriv', (), (),(1,3,6)) 
config.addVacmUser(snmpEngine, 3, 'usr-md5-3des', 'authPriv', (), (),(1,3,6)) 

# SNMP context
snmpContext = context.SnmpContext(snmpEngine)

#
# Twisted API follows
#

# Error/confirmation reciever
def receiveResponse(cbCtx):
    (sendRequestHandle, errorIndication) = cbCtx
    print('Notification %s, status - %s' % (sendRequestHandle, errorIndication and errorIndication or 'delivered'))
    reactor.stop()
    
df = ntforg.NotificationOriginator(snmpContext).sendNotification(
     snmpEngine,
     # Notification targets
     'my-notification',
     # Trap OID (SNMPv2-MIB::coldStart)
     (1,3,6,1,6,3,1,1,5,1),
     # ((oid, value), ... )
     ( ((1,3,6,1,2,1,1,1), v2c.OctetString('Example Notificator')),
       ((1,3,6,1,2,1,1,5), v2c.OctetString('Notificator Example')) ),
)

if doInform:
    df.addCallback(receiveResponse)
    reactor.run()
