# GET Command Generator
from pysnmp.entity.rfc3413.oneliner import cmdgen

cmdGen = cmdgen.CommandGenerator()

errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
    # SNMP v1
#    cmdgen.CommunityData('public', mpModel=0),
    # SNMP v2c
#    cmdgen.CommunityData('public'),
    # SNMP v3:
    # auth MD5, privacy DES
    cmdgen.UsmUserData('test-user', 'authkey1', 'privkey1'),
    # auth MD5, privacy NONE
#    cmdgen.UsmUserData('test-user', 'authkey1'),
    # auth NONE, privacy NONE
#    cmdgen.UsmUserData('test-user'),
    # auth SHA, privacy AES128
#    cmdgen.UsmUserData('test-user', 'authkey1', 'privkey1',
#                       authProtocol=cmdgen.usmHMACSHAAuthProtocol,
#                       privProtocol=cmdgen.usmAesCfb128Protocol ),
    # Transport options:
    # IPv4/UDP
    cmdgen.UdpTransportTarget(('localhost', 161)),
    # IPv6/UDP
#    cmdgen.Udp6TransportTarget(('::1', 161)),
    # Local (UNIX) domain socket
#    cmdgen.UnixTransportTarget('/tmp/snmp-agent'),
    # Objects to query (OID-value pairs):
    # OID in tuple form
    (1,3,6,1,2,1,1,1,0),
    # OID in string form
    '1.3.6.1.2.1.1.6.0',
    # MIB symbol: ((mib-name, mib-symbol), instance-id)
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
