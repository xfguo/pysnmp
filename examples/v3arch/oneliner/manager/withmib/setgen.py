# SET Command Generator with MIB resolution
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.entity.rfc3413 import mibvar

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
    # Object(s) to set/modify and their new values (OID-value pairs):
    # MIB symbol: ((mib-name, mib-symbol), instance-id), new-value
    ((('SNMPv2-MIB', 'sysDescr'), 0), 'new name')
    )

if errorIndication:
    print(errorIndication)
else:
    if errorStatus:
        print('%s at %s' % (
            errorStatus.prettyPrint(), varBinds[int(errorIndex)-1]
            )
        )
    else:
        for oid, val in varBinds:
            (symName, modName), indices = mibvar.oidToMibName(
                cmdGen.mibViewController, oid
                )
            val = mibvar.cloneFromMibValue(
                cmdGen.mibViewController, modName, symName, val
                )
            print('%s::%s.%s = %s' % (
                modName, symName,
                '.'.join([ v.prettyPrint() for v in indices]),
                val.prettyPrint()
                )
            )
