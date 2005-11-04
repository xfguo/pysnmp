# SET Command Generator with MIB resolution
import string
from pysnmp.entity.rfc3413.oneliner import cmdgen

cmdGen = cmdgen.CommandGenerator()

# Lookup Managed Object name & value at MIB
oid, suffix = cmdgen.mibvar.mibNameToOid(
    cmdGen.mibViewController,
    (('SNMPv2-MIB', 'sysDescr'), 0)
    )
val = cmdgen.mibvar.cloneFromMibValue(
    cmdGen.mibViewController,
    'SNMPv2-MIB', 'sysDescr', 'Some system desc'
    )

errorIndication, errorStatus, errorIndex, \
                 varBinds = cmdGen.setCmd(
    # SNMP v1
#    cmdgen.CommunityData('test-agent', 'public', 0),
    # SNMP v2
#    cmdgen.CommunityData('test-agent', 'public'),
    # SNMP v3
    cmdgen.UsmUserData('test-user', 'authkey1', 'privkey1'),
    # Transport
    cmdgen.UdpTransportTarget(('localhost', 161)),
    # Request variable(s)
    (oid + suffix, val)
    )

if errorIndication:
    print errorIndication
else:
    if errorStatus:
        print '%s at %s\n' % (
            errorStatus.prettyPrint(), varBinds[int(errorIndex)-1]
            )
    else:
        for oid, val in varBinds:
            (symName, modName), indices = cmdgen.mibvar.oidToMibName(
                cmdGen.mibViewController, oid
                )
            val = cmdgen.mibvar.cloneFromMibValue(
                cmdGen.mibViewController, modName, symName, val
                )
            print '%s::%s.%s = %s' % (
                modName, symName,
                string.join(map(lambda v: v.prettyPrint(), indices), '.'),
                val.prettyPrint()
                )
