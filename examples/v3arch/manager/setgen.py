from pysnmp.entity import engine, config
from pysnmp.carrier.asynsock.dgram import udp
from pysnmp.entity.rfc3413 import cmdgen, error
from pysnmp.proto import rfc1902

snmpEngine = engine.SnmpEngine()

# Setup transport endpoint
config.addSocketTransport(
    snmpEngine,
    udp.domainName,
    udp.UdpSocketTransport().openClientMode()
    )

# v1/2 setup
# addV1System(snmpEngine, 'public')

# v3 setup
config.addV3User(snmpEngine, 'test-user', 'authkey1', 'md5', 'privkey1', 'des')

# Transport params
config.addTargetParams(snmpEngine, 'myParams', 'test-user', 'authPriv')

# Transport addresses
config.addTargetAddr(
    snmpEngine, 'myRouter', config.snmpUDPDomain,
    ('127.0.0.1', 161), 'myParams'
    )

def cbFun(sendRequestHandle, errorIndication, errorStatus, errorIndex,
          varBinds, cbCtx):
    raise error.ApplicationReturn(
        errorIndication=errorIndication,
        errorStatus=errorStatus,
        errorIndex=errorIndex,
        varBinds=varBinds
        )
    
cmdgen.SetCmdGen().sendReq(
    snmpEngine, 'myRouter',
    (((1,3,6,1,2,1,1,1,0), rfc1902.OctetString('Grinch')),), cbFun
    )

try:
    snmpEngine.transportDispatcher.runDispatcher()
except error.ApplicationReturn, applicationReturn:
    if applicationReturn['errorIndication']:
        print applicationReturn['errorIndication']
    elif applicationReturn['errorStatus']:
        print '%s at %s' % (
            repr(applicationReturn['errorStatus']),
            applicationReturn['varBinds'][int(applicationReturn['errorIndex'])-1]
            )
    else:
        for o, v in applicationReturn['varBinds']:
            print '%s = %s' % (o, v)
