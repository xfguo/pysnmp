from pysnmp.entity.rfc3413.oneliner import cmdgen

errorIndication, errorStatus, errorIndex, \
                 varBindTable = cmdgen.CommandGenerator().nextCmd(
    # SNMP v2
    cmdgen.CommunityData('test-agent', 'public'),
    # SNMP v3
#    cmdgen.UsmUserData('test-user', 'authkey1', 'privkey1'),
    cmdgen.UdpTransportTarget(('localhost', 161)),
    (1,3,6,1,2,1,1)
    )

if errorIndication:
    print errorIndication
else:
    if errorStatus:
        print '%s at %s\n' % (
            errorStatus.prettyOut(errorStatus), varBindTable[-1][errorIndex]
            )
    else:
        for varBindTableRow in varBindTable:
            for name, val in varBindTableRow:
                print '%s = %s' % (name, val.prettyOut(val))
