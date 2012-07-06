# SET Command Generator with MIB resolution
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.entity.rfc3413 import mibvar

cmdGen = cmdgen.CommandGenerator()

errorIndication, errorStatus, errorIndex, varBinds = cmdGen.setCmd(
    # SNMP v1
#    cmdgen.CommunityData('public', mpModel=0),
    # SNMP v2
#    cmdgen.CommunityData('public'),
    # SNMP v3
    cmdgen.UsmUserData('test-user', 'authkey1', 'privkey1'),
    # Transport options
    cmdgen.UdpTransportTarget(('localhost', 161)),
#    cmdgen.Udp6TransportTarget(('::1', 161)),
#    cmdgen.UnixTransportTarget('/tmp/snmp-agent'),
    # Request variable(s)
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
