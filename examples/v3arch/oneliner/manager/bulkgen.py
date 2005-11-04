# GETBULK Command Generator
from pysnmp.entity.rfc3413.oneliner import cmdgen

errorIndication, errorStatus, errorIndex, \
                 varBindTable = cmdgen.CommandGenerator().bulkCmd(
    # SNMP v1
#    cmdgen.CommunityData('test-agent', 'public', 0),
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
        print '%s at %s\n' % (
            errorStatus.prettyPrint(),
            varBindTable[-1][int(errorIndex)-1]
            )
    else:
        for varBindTableRow in varBindTable:
            for name, val in varBindTableRow:
                print '%s = %s' % (name.prettyPrint(), val.prettyPrint())
