# GETNEXT Command Generator
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902

# ( ( authData, transportTarget, varNames ), ... )
targets = (
    # 1-st target (SNMPv1)
    ( cmdgen.CommunityData('test-agent', 'public'),
      cmdgen.UdpTransportTarget(('localhost', 161)),
      (rfc1902.ObjectName((1,3,6,1,2,1)), rfc1902.ObjectName((1,3,6,1,3,1)))),
    # 2-nd target (SNMPv2c)
    ( cmdgen.CommunityData('test-agent', 'public', 1),
      cmdgen.UdpTransportTarget(('localhost', 161)),
      (rfc1902.ObjectName((1,3,6,1,4,1)),) ),
    # 3-nd target (SNMPv3)
    ( cmdgen.UsmUserData('test-user', 'authkey1', 'privkey1'),
      cmdgen.UdpTransportTarget(('localhost', 161)),
      (rfc1902.ObjectName((1,3,6,1,5,1)),) )
    # N-th target
    # ...
    )

def cbFun(
    sendRequestHandle, errorIndication, errorStatus, errorIndex,
    varBindTable, (varBindHead, authData, transportTarget)
    ):
    print '%s via %s' % (authData, transportTarget)
    if errorIndication:
        print 'SNMP engine error', errorIndication
        return 1
    if errorStatus:
        print 'SNMP error %s at %s' % (errorStatus, errorIndex)
        return 1
    varBindTableRow = varBindTable[-1]
    for idx in range(len(varBindTableRow)):
        name, val = varBindTableRow[idx]
        if val is not None and varBindHead[idx].isPrefixOf(name):
            # still in table
            break
    else:
        print 'went out of table at %s' % (name, )
        return
    
    for varBindRow in varBindTable:
        for oid, val in varBindRow:
            if val is None:
                print oid.prettyPrint()
            else:
                print '%s = %s' % (oid.prettyPrint(), val.prettyPrint())

    return 1 # continue table retrieval

cmdGen  = cmdgen.CommandGenerator()

for authData, transportTarget, varNames in targets:
    cmdGen.asyncNextCmd(
        authData, transportTarget, varNames,
        # User-space callback function and its context
        (cbFun, (varNames, authData, transportTarget))
        )

cmdGen.snmpEngine.transportDispatcher.runDispatcher()
