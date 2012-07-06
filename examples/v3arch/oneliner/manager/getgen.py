# GET Command Generator
from pysnmp.entity.rfc3413.oneliner import cmdgen

errorIndication, errorStatus, \
                 errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(
    # SNMP v1
#    cmdgen.CommunityData('public', mpModel=0),
    # SNMP v2
    cmdgen.CommunityData('public'),
    # SNMP v3
#    cmdgen.UsmUserData('test-user', 'authkey1', 'privkey1'),
    # Transport options
    cmdgen.UdpTransportTarget(('localhost', 161)),
#    cmdgen.Udp6TransportTarget(('::1', 161)),
#    cmdgen.UnixTransportTarget('/tmp/snmp-agent'),
    # Plain OID
    (1,3,6,1,2,1,1,1,0),
    # ((mib-name, mib-symbol), instance-id)
    (('SNMPv2-MIB', 'sysObjectID'), 0)
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
