"""Command Generator Application (GET)"""
from pysnmp import setApiVersion
setApiVersion('v4')
from pysnmp.proto.rfc3412 import MsgAndPduDispatcher, AbstractApplication
from pysnmp.proto import omni

# PDU version to use
versionId = omni.protoVersionId1
ver = omni.protoVersions[versionId]

class ManagerApplication(AbstractApplication):
    __pendingReqs = {}
    def sendReq(self, msgAndPduDsp, **kwargs):
        sendPduHandle = apply(msgAndPduDsp.sendPdu, (), kwargs)
        # Queue request information
        self.__pendingReqs[sendPduHandle] = kwargs['PDU']
            
    def processResponsePdu(self, msgAndPduDsp, **kwargs):
        # Take pending req off the queue        
        reqPdu = self.__pendingReqs.get(kwargs['sendPduHandle'])
        del self.__pendingReqs[kwargs['sendPduHandle']]

        # Check for SNMP engine-level errors
        if kwargs.has_key('statusInformation'):
            raise str(kwargs['statusInformation'])
        
        rspPdu = kwargs['PDU']

        # Check for PDU-level errors
        errorStatus = rspPdu.omniGetErrorStatus()
        if errorStatus:
            raise str(errorStatus)

        # Report response values
        for varBind in rspPdu.omniGetVarBindList():
            oid, val = varBind.omniGetOidVal()
            print oid, val
        msgAndPduDsp.transportDispatcher.doDispatchFlag = 0

msgAndPduDsp = MsgAndPduDispatcher()

# UDP is default transport, initialize client mode
msgAndPduDsp.transportDispatcher.getTransport('udp').openClientMode()

# Configure target SNMP agent at LCD
( snmpCommunityEntry, )  \
  =  msgAndPduDsp.mibInstrumController.mibBuilder.importSymbols(
    'SNMP-COMMUNITY-MIB', 'snmpCommunityEntry'
    )
msgAndPduDsp.mibInstrumController.writeVars(
    (snmpCommunityEntry.getInstNameByIndex(2, 'myAgentIdx'), 'public'),
    (snmpCommunityEntry.getInstNameByIndex(3, 'myAgentIdx'), 'myAgent')
    )

pdu = ver.GetRequestPdu()
pdu.omniSetVarBindList(((1,3,6,1,2,1,1,1), ver.Null()))

app = ManagerApplication()
app.sendReq(
    msgAndPduDsp,
    transportDomain='udp', transportAddress=('127.0.0.1', 1161),
    messageProcessingModel=versionId,
    pduVersion=versionId,
    securityName='myAgent',
    PDU=pdu,
    expectResponse=app
    )

msgAndPduDsp.transportDispatcher.runDispatcher()

    
