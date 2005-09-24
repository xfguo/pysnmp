from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902

errorIndication, errorStatus, \
                 errorIndex, varBinds = cmdgen.CommandGenerator().setCmd(
    # SNMP v1
#    cmdgen.CommunityData('test-agent', 'public', 0),
    # SNMP v2
#    cmdgen.CommunityData('test-agent', 'public'),
    # SNMP v3
    cmdgen.UsmUserData('test-user', 'authkey1', 'privkey1'),
    cmdgen.UdpTransportTarget(('localhost', 161)),
    ((1,3,6,1,2,1,1,1,0), rfc1902.OctetString('Some system desc'))
    )

if errorIndication:
    print errorIndication
else:
    if errorStatus:
        print '%s at %s\n' % (
            errorStatus.prettyOut(errorStatus), varBinds[int(errorIndex)-1]
            )
    else:
        for name, val in varBinds:
            print '%s = %s' % (name, val.prettyOut(val))
