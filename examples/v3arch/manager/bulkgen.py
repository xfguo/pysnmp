# GETBULK Command Generator
from pysnmp.entity import engine, config
from pysnmp.entity.rfc3413 import cmdgen
from pysnmp.carrier.asynsock.dgram import udp

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
#config.addTargetParams(snmpEngine, 'myParams', 'test-user', 'authPriv')
config.addTargetParams(snmpEngine, 'myParams', 'test-agent', 'noAuthNoPriv', 1)

# Transport addresses
config.addTargetAddr(
    snmpEngine, 'myRouter', config.snmpUDPDomain,
    ('127.0.0.1', 161), 'myParams'    
    )

# Transport
config.addSocketTransport(
    snmpEngine,
    config.snmpUDPDomain,
    udp.UdpSocketTransport().openClientMode()
    )

def cbFun(sendRequesthandle, errorIndication, errorStatus, errorIndex,
          varBindTable, cbCtx):
    if errorIndication:
        print errorIndication
        return
    if errorStatus:
        print errorStatus.prettyPrint()
        return
    for varBindRow in varBindTable:
        for oid, val in varBindRow:
            if val is None:
                print oid.prettyPrint()
            else:
                print '%s = %s' % (oid.prettyPrint(), val.prettyPrint())
    for oid, val in varBindTable[-1]:
        if val is not None:
            break
    else:
        return # stop on end-of-table
    return 1 # continue walking

cmdgen.BulkCommandGenerator().sendReq(
    snmpEngine, 'myRouter', 0, 25, (((1,3,6,1,2,1,1), None),), cbFun
    )

snmpEngine.transportDispatcher.runDispatcher()
