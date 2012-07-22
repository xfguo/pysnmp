#
# SNMP proxy example
#
# Act as a local SNMPv1/v2c Agent, relay messages to distant SNMPv3 Manager.
#
from socket import gethostbyname
from pysnmp.carrier.asynsock.dgram import udp, udp6
from pysnmp.entity import engine, config
from pysnmp.entity.rfc3413 import cmdrsp, cmdgen, context
from pysnmp.proto.api import v2c
from pysnmp import error
#from pysnmp import debug

# Basic configuration
remoteTransportDomain = udp.domainName
remoteTransportAddress = gethostbyname('test.net-snmp.org'), 161
remoteV3User = 'MD5User'
remoteV3AuthKey = 'The Net-SNMP Demo Password'

# Optional debugging ('all' enables full debugging)
#debug.setLogger(debug.Debug('io', 'dsp', 'msgproc', 'secmod', 'app'))

# Create SNMP engine with autogenernated engineID and pre-bound
# to socket transport dispatcher
snmpEngine = engine.SnmpEngine()

#
# Transport setup
#

# Agent section

# UDP over IPv4
config.addSocketTransport(
    snmpEngine,
    udp.domainName + (1,),
    udp.UdpTransport().openServerMode(('127.0.0.1', 161))
)

# UDP over IPv6
config.addSocketTransport(
    snmpEngine,
    udp6.domainName + (1,),
    udp6.Udp6Transport().openServerMode(('::1', 161))
    )

# Manager section

# UDP over IPv4
config.addSocketTransport(
    snmpEngine,
    udp.domainName,
    udp.UdpTransport().openClientMode()
)

#
# SNMPv1/2c setup (Agent role)
#

# SecurityName <-> CommunityName mapping
config.addV1System(snmpEngine, 'my-area', 'public')

#
# SNMPv3/USM setup (Manager role)
#

# user: usr-md5-none, auth: MD5, priv NONE
config.addV3User(
    snmpEngine, remoteV3User,
    config.usmHMACMD5AuthProtocol, remoteV3AuthKey
)

#
# Transport target used by Manager
#

config.addTargetParams(
    snmpEngine, 'distant-agent', 'MD5User', 'authNoPriv'
)
config.addTargetAddr(
        snmpEngine, 'net-snmp-agent', 
        remoteTransportDomain, remoteTransportAddress,
        'distant-agent', retryCount=0
)

# Default SNMP context
config.addContext(snmpEngine, '')

class CommandResponder(cmdrsp.CommandResponderBase):
    cmdGenMap = { v2c.GetRequestPDU.tagSet: cmdgen.GetCommandGenerator(),
                  v2c.SetRequestPDU.tagSet: cmdgen.SetCommandGenerator(),
                  v2c.GetNextRequestPDU.tagSet: cmdgen.NextCommandGeneratorSingleRun(),
                  v2c.GetBulkRequestPDU.tagSet: cmdgen.BulkCommandGeneratorSingleRun() }
    pduTypes = cmdGenMap.keys()  # This app will handle these PDUs

    def handleMgmtOperation(self, snmpEngine, stateReference, contextName,
                            PDU, acInfo):
        (acFun, acCtx) = acInfo
        varBinds = v2c.apiPDU.getVarBinds(PDU)
        try:
            if PDU.tagSet == v2c.GetBulkRequestPDU.tagSet:
                self.cmdGenMap[PDU.tagSet].sendReq(
                    snmpEngine, 'net-snmp-agent', 
                    v2c.apiBulkPDU.getNonRepeaters(PDU),
                    v2c.apiBulkPDU.getMaxRepetitions(PDU),
                    varBinds,
                    self.handleResponse, stateReference
                )
            elif PDU.tagSet in self.cmdGenMap:
                self.cmdGenMap[PDU.tagSet].sendReq(
                    snmpEngine, 'net-snmp-agent', varBinds,
                    self.handleResponse, stateReference
                )
        except error.PySnmpError:
            self.sendRsp(snmpEngine, stateReference,  5, 0,  varBinds)

    def handleResponse(self, sendRequestHandle, errorIndication, 
                       errorStatus, errorIndex, varBinds, cbCtx):
        if errorIndication:
            errorStatus = 5
            errorIndex = 0
            varBinds = ()

        stateReference = cbCtx

        self.sendRsp(
            snmpEngine, stateReference,  errorStatus, errorIndex, varBinds
        )

# Command Responder app registration
CommandResponder(snmpEngine, context.SnmpContext(snmpEngine))

snmpEngine.transportDispatcher.jobStarted(1) # this job would never finish

# Run I/O dispatcher which would receive queries and send responses
try:
    snmpEngine.transportDispatcher.runDispatcher()
except:
    snmpEngine.transportDispatcher.closeDispatcher()
    raise
