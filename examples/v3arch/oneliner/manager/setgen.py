# SET Command Generator
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902

cmdGen = cmdgen.CommandGenerator()

errorIndication, errorStatus, errorIndex, varBinds = cmdGen.setCmd(
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
    # Objects to set/modify and their new values (OID-value pairs):
    # MIB symbol: ((mib-name, mib-symbol), instance-id), new-value
    ((('SNMPv2-MIB', 'sysName'), 0), 'new name'),
    # OID in string form, rfc1902 class instance value
    ('1.3.6.1.2.1.1.5.0', rfc1902.OctetString('new name'))
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
