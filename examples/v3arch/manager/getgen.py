"""Command Generator Application (GET)"""
from pysnmp.proto.rfc3412 import MsgAndPduDispatcher, AbstractApplication
from pysnmp.proto.api import alpha

# PDU version to use
ver = alpha.protoVersions[alpha.protoVersionId1]

class ManagerApplication(AbstractApplication):
    __pendingReqs = {}
    def sendReq(self, msgAndPduDsp, **kwargs):
        sendPduHandle = apply(msgAndPduDsp.sendPdu, (), kwargs)
        self.__pendingReqs[sendPduHandle] = kwargs['PDU']
            
    def processResponsePdu(self, msgAndPduDsp, **kwargs):
        reqPdu = self.__pendingReqs.get(kwargs['sendPduHandle'])
        del self.__pendingReqs[kwargs['sendPduHandle']]
        if kwargs.has_key('statusInformation'):
            raise str(kwargs['statusInformation'])
        rspPdu = kwargs['PDU']
        errorStatus = rspPdu.apiAlphaGetErrorStatus()
        if errorStatus:
            raise str(errorStatus)
        for varBind in rspPdu.apiAlphaGetVarBindList():
            oid, val = varBind.apiAlphaGetOidVal()
            print oid, val
        msgAndPduDsp.transportDispatcher.doDispatchFlag = 0

msgAndPduDsp = MsgAndPduDispatcher()

# Configure target SNMP agent at LCD
( snmpCommunityEntry, )  \
  =  msgAndPduDsp.mibInstrumController.mibBuilder.importSymbols(
    'SNMP-COMMUNITY-MIB', 'snmpCommunityEntry'
    )

msgAndPduDsp.mibInstrumController.writeVars(
    (snmpCommunityEntry.getInstNameByIndex(2, 'myAgentIdx'), 'public'),
    (snmpCommunityEntry.getInstNameByIndex(3, 'myAgentIdx'), 'myAgent')
    )

msgAndPduDsp.transportDispatcher.getTransport('udp').openClientMode()

pdu = ver.GetRequestPdu()
pdu.apiAlphaSetVarBindList(((1,3,6,1,2,1,1,2,0), ver.Null()))

app = ManagerApplication()
app.sendReq(
    msgAndPduDsp,
    transportDomain='udp', transportAddress=('127.0.0.1', 1161),
    securityName='myAgent',
    PDU=pdu,
    expectResponse=app
    )

msgAndPduDsp.runTransportDispatcher()

    
