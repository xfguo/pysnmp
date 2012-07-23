# GETNEXT Command Generator
from twisted.internet import reactor, defer
from pysnmp.entity import engine, config
from pysnmp.carrier.twisted import dispatch
from pysnmp.carrier.twisted.dgram import udp
from pysnmp.entity.rfc3413.twisted import cmdgen
from pyasn1.type import univ
#from pysnmp import debug

## Optional debugging ('all' enables full debugging)
#debug.setLogger(debug.Debug('io', 'dsp', 'msgproc', 'secmod', 'app'))

# Create SNMP engine instance
snmpEngine = engine.SnmpEngine()

# Set Twisted dispatcher
snmpEngine.registerTransportDispatcher(dispatch.TwistedDispatcher())

#
# SNMPv1/2c setup (if you use SNMPv1 or v2c)
#

## SecurityName <-> CommunityName mapping
config.addV1System(snmpEngine, 'my-area', 'public')

## Specify security settings per SecurityName (SNMPv1 - 0, SNMPv2c - 1)
config.addTargetParams(snmpEngine, 'my-creds', 'my-area', 'noAuthNoPriv', 0)
#config.addTargetParams(snmpEngine, 'my-creds', 'my-area', 'noAuthNoPriv', 1)

#
# SNMPv3/USM setup (choose any one if you use SNMPv3/USM)
#

# user: usr-md5-des, auth: MD5, priv DES
#config.addV3User(
#    snmpEngine, 'usr-md5-des',
#    config.usmHMACMD5AuthProtocol, 'authkey1',
#    config.usmDESPrivProtocol, 'privkey1'
#)
#config.addTargetParams(snmpEngine, 'my-creds', 'usr-md5-des', 'authPriv')

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
# a target name (choose one entry depending of the transport needed).
#

# UDP/IPv4
config.addSocketTransport(
    snmpEngine,
    udp.domainName,
    udp.UdpTwistedTransport().openClientMode()
)
config.addTargetAddr(
    snmpEngine, 'my-router',
    udp.domainName, ('127.0.0.1', 161),
    'my-creds'
)

# Twisted API follows

# Error/response reciever
def receiveResponse(cbCtx):
    (errorIndication, errorStatus, errorIndex, varBindTable) = cbCtx
    if errorIndication:
        print('Error: %s' % errorIndication)
        reactor.stop()
        return
    # SNMPv1 response may contain noSuchName error *and* SNMPv2c exception,
    # so we ignore noSuchName error here
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

df = cmdgen.NextCommandGenerator().sendReq(
     snmpEngine,
    'my-router',
    ( ((1,3,6,1,2,1,1), None),
      ((1,3,6,1,4,1,1), None), )
)

df.addCallback(receiveResponse)

reactor.run()
