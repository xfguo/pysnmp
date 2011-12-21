# GETNEXT Command Generator
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902

# ( ( authData, transportTarget, varNames ), ... )
targets = (
    # 1-st target (SNMPv2c -- can't handle v1&v2c with equal communities)
    ( cmdgen.CommunityData('public'),  # , mpModel=0),
      cmdgen.UdpTransportTarget(('localhost', 161)),
      (rfc1902.ObjectName((1,3,6,1,2,1)), rfc1902.ObjectName((1,3,6,1,3,1)))),
    # 2-nd target (SNMPv2c)
    ( cmdgen.CommunityData('public'),
      cmdgen.UdpTransportTarget(('localhost', 161)),
      (rfc1902.ObjectName((1,3,6,1,4,1)),) ),
    # 3-nd target (SNMPv3)
    ( cmdgen.UsmUserData('test-user', 'authkey1', 'privkey1'),
      cmdgen.UdpTransportTarget(('localhost', 161)),
      (rfc1902.ObjectName((1,3,6,1,5,1)),) )
    # N-th target
    # ...
    )

def cbFun(sendRequestHandle, errorIndication, errorStatus, errorIndex,
          varBindTable, cbCtx):
    (varBindHead, authData, transportTarget) = cbCtx
    print('%s via %s' % (authData, transportTarget))
    if errorIndication:
        print(errorIndication)
        return 1
    if errorStatus:
        print('%s at %s' % (
            errorStatus.prettyPrint(),
            errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
            )
        )
        return 1
    varBindTableRow = varBindTable[-1]
    for idx in range(len(varBindTableRow)):
        name, val = varBindTableRow[idx]
        if val is not None and varBindHead[idx] <= name:
            # still in table
            break
    else:
        print('went out of table at %s' % (name, ))
        return
    
    for varBindRow in varBindTable:
        for oid, val in varBindRow:
            if val is None:
                print(oid.prettyPrint())
            else:
                print('%s = %s' % (oid.prettyPrint(), val.prettyPrint()))

    return 1 # continue table retrieval

cmdGen  = cmdgen.AsynCommandGenerator()

for authData, transportTarget, varNames in targets:
    cmdGen.nextCmd(
        authData, transportTarget, varNames,
        # User-space callback function and its context
        (cbFun, (varNames, authData, transportTarget))
        )

cmdGen.snmpEngine.transportDispatcher.runDispatcher()
