from pysnmp.entity.rfc3413.oneliner import cmdgen

errorIndication, errorStatus, errorIndex, \
                 varBinds, varBindTable = cmdgen.CmdGen().bulkCmd(
    # SNMP v2
#    cmdgen.CommunityData('test-agent', 'public'),
    # SNMP v3
    cmdgen.UsmUserData('test-user', 'authkey1', 'privkey1'),
    cmdgen.UdpTransportTarget(('localhost', 161)),
    0, 25,
    (1,3,6,1,2,1,1)
    )

if errorIndication:
    print errorIndication
else:
    if errorStatus:
        print '%s at %s\n' % (errorStatus, varBinds[errorIndex-1])
    else:
        for varBindTableRow in varBindTable:
            for varBind in varBindTableRow:
                print '%s = %s' % varBind
