"""Command Responder Application (GET PDU)"""
from pysnmp.entity import engine, config
from pysnmp.carrier.asynsock.dgram import udp
from pysnmp.entity.rfc3413 import cmdrsp, error

# Create SNMP engine with autogenernated engineID and pre-bound
# to socket transport dispatcher
snmpEngine = engine.SnmpEngine()

# XXX transport registration and routing should be different
# for client & server modes

# Setup transport endpoint
config.addSocketTransport(
    snmpEngine,
    udp.domainName,
    udp.UdpSocketTransport().openServerMode(('127.0.0.1', 1161))
    )

# Create and put on-line my managed object
MibVariable, = snmpEngine.msgAndPduDsp.mibInstrumController.mibBuilder.importSymbols('SNMPv2-SMI', 'MibVariable')
OctetString, = snmpEngine.msgAndPduDsp.mibInstrumController.mibBuilder.importSymbols('ASN1', 'OctetString')
myMibVariable = MibVariable(
    (1,3,6,1,4,1,20408,2,1), OctetString('hello, NMS!')
    ).setMaxAccess("readwrite")
snmpEngine.msgAndPduDsp.mibInstrumController.mibBuilder.exportSymbols('PYSNMP-EXAMPLE-MIB', myMibVariable=myMibVariable)  # creating MIB

# v1/2 setup
# addV1System(snmpEngine, 'public')

# v3 setup
#config.addV3User(snmpEngine, 'test-user', 'authkey1', 'md5', 'privkey1', 'des')
config.addV3User(snmpEngine, 'test-user', 'authKey1', 'md5', 'privKey1','des',
                 '\x1d\xcfY\xe8eS\xb3\xaf\xa5\xd3/\xd5\xd6\x1b\xf0\xcf',
                 '\xecZ\xb5^\x93\xe1\xd8\\\xb6\x84m\x0f#\xe8E\xe0')
    
# VACM setup
config.addContext(snmpEngine, '')
#config.addRoUser(snmpEngine, 'test-user', 1, (1,3,6,1,2,1))
#config.addRoUser(snmpEngine, 'test-user', 2, (1,3,6,1,2,1))
config.addRoUser(snmpEngine, 'test-user', 'authPriv', (1,3,6))
config.addRoUser(snmpEngine, 'test-user', 'authNoPriv', (1,3,6))
config.addRoUser(snmpEngine, 'test-user', 'noAuthNoPriv', (1,3,6))
#config.addRoUser(snmpEngine, 'test-user', 1, (1,3,6,1,2,1,2,2,1,1))
#config.addRoUser(snmpEngine, 'test-user', 3, (1,3,6,1,2,1))

getApp = cmdrsp.GetRsp(snmpEngine)
getApp = cmdrsp.GetNextRsp(snmpEngine)
getApp = cmdrsp.GetBulkRsp(snmpEngine)

snmpEngine.transportDispatcher.runDispatcher()
