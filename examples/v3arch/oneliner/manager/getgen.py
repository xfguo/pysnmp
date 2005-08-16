from pysnmp.entity.rfc3413.oneliner import cmdgen

errorIndication, errorStatus, \
                 errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(
    # SNMP v2
    cmdgen.CommunityData('test-agent', 'public'),
    # SNMP v3
#    cmdgen.UsmUserData('test-user', 'authkey1', 'privkey1'),
    cmdgen.UdpTransportTarget(('localhost', 161)),
    (1,3,6,1,2,1,1,1,0)
    )

if errorIndication:
    print errorIndication
else:
    if errorStatus:
        print '%s at %s\n' % (
            errorStatus.prettyOut(errorStatus), varBinds[errorIndex-1]
            )
    else:
        for name, val in varBindTableRow:
            print '%s = %s' % (name, val.prettyOut(val))
