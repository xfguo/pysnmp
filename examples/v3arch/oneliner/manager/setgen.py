# SET Command Generator
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902

errorIndication, errorStatus, \
                 errorIndex, varBinds = cmdgen.CommandGenerator().setCmd(
    # SNMP v1
#    cmdgen.CommunityData('public', mpModel=0),
    # SNMP v2
#    cmdgen.CommunityData('public'),
    # SNMP v3
    cmdgen.UsmUserData('test-user', 'authkey1', 'privkey1'),
    cmdgen.UdpTransportTarget(('localhost', 161)),
    # MIB symbol name, plain string value
    ((('SNMPv2-MIB', 'sysName'), 0), 'new name'),
    # Plain OID name, rfc1902 class instance value
    ((1,3,6,1,2,1,1,5,0), rfc1902.OctetString('new name'))
    )

if errorIndication:
    print(errorIndication)
else:
    if errorStatus:
        print('%s at %s' % (
            errorStatus.prettyPrint(),
            errorIndex and varBinds[int(errorIndex)-1] or '?'
            )
        )
    else:
        for name, val in varBinds:
            print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))
