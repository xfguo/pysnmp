#
# SNMP proxy example
#
# Relay SNMP messages between Managers and Agents using any combinations
# of SNMP protocol versions for both up and downstream packets.
#
# To query SNMPv3 Manager over SNMPv2c through this Proxy use:
# snmpget -v2c -c tgt-v3-1 localhost:1161 sysDescr.0
# or SNMPv2c Manager over SNMPv3:
# snmpget -v3 -u test-user -lauthPriv -A authkey1 -X privkey1 -n tgt-v2c-1 localhost:1161 sysDescr.0
# there are four combinations in total. ;)
#
from pysnmp.entity import engine, config
from pysnmp.entity.rfc3413 import cmdrsp, cmdgen, context
from pysnmp.proto.api import v2c
from pysnmp.carrier.asynsock.dgram import udp

# Create SNMP engine with autogenernated engineID and pre-bound
# to socket transport dispatcher
snmpEngine = engine.SnmpEngine()

# Setup UDP over IPv4 transport endpoints

# Agent will listen here
config.addSocketTransport(
    snmpEngine,
    udp.domainName + (1,),  # use transport domain's sub-name
    udp.UdpTransport().openServerMode(('127.0.0.1', 1161))
    )

# Manager will send packets there
config.addSocketTransport(
    snmpEngine,
    udp.domainName + (2,), # use transport domain's sub-name
    udp.UdpTransport().openClientMode()
    )

# SNMP credentials used by Manager

# v1/2 setup
config.addV1System(snmpEngine, 'dest-cmt', 'public')

# v3 setup
config.addV3User(
    snmpEngine, 'test-user',
    config.usmHMACMD5AuthProtocol, 'authkey1',
    config.usmDESPrivProtocol, 'privkey1'
#    config.usmAesCfb128Protocol, 'privkey1'
    )

# Transport targets used by Manager

# Target 1, SNMPv3 setup
config.addTargetParams(snmpEngine, 'v3-dest-1', 'test-user', 'authPriv')
config.addTargetAddr(
        snmpEngine, 'tgt-v3-1', config.snmpUDPDomain + (2,),
            ('127.0.0.1', 161), 'v3-dest-1'
            )
# This is to map community to context name in incoming messages
config.addV1System(snmpEngine, 'v2c-src-A', 'tgt-v3-1', contextName='tgt-v3-1')

# Target 1, SNMPv2c setup
config.addTargetParams(snmpEngine, 'v2c-dest-1', 'dest-cmt', 'noAuthNoPriv', 1)
config.addTargetAddr(
        snmpEngine, 'tgt-v2c-1', config.snmpUDPDomain + (2,),
            ('127.0.0.1', 161), 'v2c-dest-1'
            )
# This is to map community to context name in incoming messages
config.addV1System(snmpEngine, 'v2c-src-B', 'tgt-v2c-1', contextName='tgt-v2c-1')

# Default SNMP context
config.addContext(snmpEngine, '')
snmpContext = context.SnmpContext(snmpEngine)


class GetCommandProxy(cmdrsp.GetCommandResponder):
    acmID = 0  # void access control method
    cmdGen = cmdgen.GetCommandGenerator()
    
    def handleMgmtOperation(self, snmpEngine, stateReference, contextName,
                            PDU, acInfo):
        (acFun, acCtx) = acInfo
        varBinds = v2c.apiPDU.getVarBinds(PDU)
        try:
            # The trick here is to use contextName as SNMP Manager target name
            self.cmdGen.sendReq(
                snmpEngine, contextName, varBinds,
                self.handleResponse, (stateReference, varBinds)
                )
        except Exception:
            self.sendRsp(snmpEngine, stateReference,  5, 0,  varBinds)

    def handleResponse(self, sendRequestHandle, errorIndication,
                       errorStatus, errorIndex, varBinds, cbCtx):
        (stateReference, reqVarBinds) = cbCtx
        if errorIndication:
            errorStatus = 5
            varBinds = reqVarBinds
            
        self.sendRsp(
            snmpEngine, stateReference,  errorStatus, errorIndex, varBinds
            )
            
# Apps registration
GetCommandProxy(snmpEngine, snmpContext)

snmpEngine.transportDispatcher.jobStarted(1) # this job would never finish
snmpEngine.transportDispatcher.runDispatcher()
