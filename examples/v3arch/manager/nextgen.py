"""Command Generator Application (GETNEXT)"""
from pysnmp import setApiVersion
setApiVersion('v4')
from pysnmp.proto.rfc3412 import MsgAndPduDispatcher, AbstractApplication
from pysnmp.proto import omni

# PDU version to use
versionId = omni.protoVersionId1
ver = omni.protoVersions[versionId]

# SNMP table header
headVars = [ ver.ObjectName((1,3,6,1,2,1,1)) ]

class ManagerApplication(AbstractApplication):
    __pendingReqs = {}
    def sendReq(self, msgAndPduDsp, **kwargs):
        sendPduHandle = apply(msgAndPduDsp.sendPdu, (), kwargs)
        # Queue request information
        self.__pendingReqs[sendPduHandle] = (
            kwargs['transportDomain'],
            kwargs['transportAddress'],
            kwargs['PDU']
            )
            
    def processResponsePdu(self, msgAndPduDsp, **kwargs):
        # Take pending req off the queue
        transportDomain, transportAddress, reqPdu = self.__pendingReqs.get(
            kwargs['sendPduHandle']
            )
        del self.__pendingReqs[kwargs['sendPduHandle']]

        # Check for SNMP engine-level errors        
        if kwargs.has_key('statusInformation'):
            raise str(kwargs['statusInformation'])
        
        rspPdu = kwargs['PDU']

        # Check for PDU-level error
        errorStatus = rspPdu.omniGetErrorStatus()
        if 0 != errorStatus != 2:
            raise str(errorStatus)

        # Build SNMP table from response
        tableIndices = apply(
            reqPdu.omniGetTableIndices, [rspPdu] + headVars
            )

        # Report SNMP table
        varBindList = rspPdu.omniGetVarBindList()
        for rowIndices in tableIndices:
            for cellIdx in filter(lambda x: x!=-1, rowIndices):
                print varBindList[cellIdx].omniGetOidVal()

        # Remove completed SNMP table columns
        map(lambda idx, headVars=headVars: headVars.__delitem__(idx), \
            filter(lambda x: x==-1, tableIndices[-1]))
        if not headVars:
            msgAndPduDsp.transportDispatcher.doDispatchFlag = 0
            return

        # Generate request PDU for next row
        lastRow = map(lambda cellIdx, varBindList=varBindList:
                      varBindList[cellIdx].omniGetOidVal(),
                      filter(lambda x: x!=-1, tableIndices[-1]))
        apply(reqPdu.omniSetVarBindList,
              map(lambda (x, y): (x.get(), None), lastRow))
        
        reqPdu.omniGetRequestId().inc(1)

        # Submit next req to msgAndPduDsp
        self.sendReq(
            msgAndPduDsp,
            transportDomain=transportDomain,
            transportAddress=transportAddress,
            messageProcessingModel=kwargs['messageProcessingModel'],
            pduVersion=kwargs['pduVersion'],
            securityName=kwargs['securityName'],            
            PDU=reqPdu,
            expectResponse=self
            )                     
                     
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

pdu = ver.GetNextRequestPdu()
pdu.omniSetVarBindList((headVars[0].clone(), ver.Null()))

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
