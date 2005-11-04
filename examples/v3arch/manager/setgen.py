# SET Command Generator
from pysnmp.entity import engine, config
from pysnmp.carrier.asynsock.dgram import udp
from pysnmp.entity.rfc3413 import cmdgen
from pysnmp.proto import rfc1902

snmpEngine = engine.SnmpEngine()

# v1/2 setup
config.addV1System(snmpEngine, 'test-agent', 'public')

# v3 setup
config.addV3User(
    snmpEngine, 'test-user',
    config.usmHMACMD5AuthProtocol, 'authkey1',
    config.usmDESPrivProtocol, 'privkey1'
    )

# Transport params
config.addTargetParams(snmpEngine, 'myParams', 'test-user', 'authPriv')
#config.addTargetParams(snmpEngine, 'myParams', 'test-agent', 'noAuthNoPriv', 0)

# Transport addresses
config.addTargetAddr(
    snmpEngine, 'myRouter', config.snmpUDPDomain,
    ('127.0.0.1', 161), 'myParams'
    )

# Setup transport endpoint
config.addSocketTransport(
    snmpEngine,
    udp.domainName,
    udp.UdpSocketTransport().openClientMode()
    )

def cbFun(sendRequestHandle, errorIndication, errorStatus, errorIndex,
          varBinds, cbCtx):
    cbCtx['errorIndication'] = errorIndication
    cbCtx['errorStatus'] = errorStatus
    cbCtx['errorIndex'] = errorIndex
    cbCtx['varBinds'] = varBinds

cbCtx = {}

cmdgen.SetCommandGenerator().sendReq(
    snmpEngine, 'myRouter',
    (((1,3,6,1,2,1,1,1,0), rfc1902.OctetString('Grinch')),), cbFun, cbCtx
    )

snmpEngine.transportDispatcher.runDispatcher()
if cbCtx['errorIndication']:
    print cbCtx['errorIndication']
elif cbCtx['errorStatus']:
    print '%s at %s' % (
        cbCtx['errorStatus'].prettyPrint(),
        cbCtx['varBinds'][int(cbCtx['errorIndex'])-1]
        )
else:
    for o, v in cbCtx['varBinds']:
        print '%s = %s' % (o.prettyPrint(), v.prettyPrint())
