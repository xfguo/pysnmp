from pysnmp.entity import engine, config
from pysnmp.entity.rfc3413 import cmdgen, error

snmpEngine = engine.SnmpEngine()

# v1/2 setup
# addV1System(snmpEngine, 'public')

# v3 setup
config.addV3User(snmpEngine, 'test-user', 'authkey1', 'md5', 'privkey1', 'des')

# Transport params
config.addTargetParams(snmpEngine, 'myParams', 'test-user', 'authPriv')

# Transport addresses
config.addTargetAddr(
    snmpEngine, 'myRouter', config.snmpUDPDomain,
    ('127.0.0.1', 1161), 'myParams'
    )

def cbFun(errorIndication, mibView, errorStatus, errorIndex, varBinds, cbCtx):
    raise error.ApplicationReturn(
        errorIndication=errorIndication,
        errorStatus=errorStatus,
        errorIndex=errorIndex,
        varBinds=varBinds
        )
    
cmdgen.SnmpSet().sendReq(
    snmpEngine, 'myRouter', ((('SNMPv2-MIB', 'sysDescr'), 'a Penguin'),), cbFun
    )

try:
    snmpEngine.msgAndPduDsp.transportDispatcher.runDispatcher()
except error.ApplicationReturn, applicationReturn:
    if applicationReturn['errorIndication']:
        print applicationReturn['errorIndication']
    elif applicationReturn['errorStatus']:
        print repr(applicationReturn['errorStatus'])
    else:
        for o, v in applicationReturn['varBinds']:
            print '%s = %s' % (o, v)
