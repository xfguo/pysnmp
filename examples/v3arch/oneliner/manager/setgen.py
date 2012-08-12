# Various SET Command Generator uses
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902

cmdGen = cmdgen.CommandGenerator()

# Send SNMP SET request
#     with SNMPv2c, community 'public'
#     over IPv4/UDP
#     to an Agent at localhost:161
#     setting SNMPv2-MIB::sysName.0 to new value (type taken from MIB)
errorIndication, errorStatus, errorIndex, varBinds = cmdGen.setCmd(
    cmdgen.CommunityData('public'),
    cmdgen.UdpTransportTarget(('localhost', 161)),
    (cmdgen.MibVariable('SNMPv2-MIB', 'sysName', 0), 'new system name')
)

# Check for errors and print out results
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


# Send SNMP SET request
#     with SNMPv1, community 'public'
#     over IPv4/UDP
#     to an Agent at localhost:161
#     setting two OIDs to new values (types explicitly specified)
errorIndication, errorStatus, errorIndex, varBinds = cmdGen.setCmd(
    cmdgen.CommunityData('public'),
    cmdgen.UdpTransportTarget(('localhost', 161)),
    ('1.3.6.1.2.1.1.2.0', rfc1902.ObjectName('1.3.6.1.4.1.20408.1.1')),
    ('1.3.6.1.2.1.1.2.0', '1.3.6.1.4.1.20408.1.1'),
    ('1.3.6.1.2.1.1.5.0', rfc1902.OctetString('new system name'))
)

# Check for errors and print out results
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


# Send SNMP SET request
#     with SNMPv3 with user 'usr-md5-des', MD5 auth and DES privacy protocols
#     over IPv4/UDP
#     to an Agent at localhost:161
#     setting SNMPv2-MIB::sysName.0 to new value (type taken from MIB)
#     perform response OIDs and values resolution at MIB
errorIndication, errorStatus, errorIndex, varBinds = cmdGen.setCmd(
    cmdgen.UsmUserData('usr-md5-des', 'authkey1', 'privkey1'),
    cmdgen.UdpTransportTarget(('localhost', 161)),
    (cmdgen.MibVariable('SNMPv2-MIB', 'sysName', 0), 'new system name'),
    lookupNames=True, lookupValues=True
)

# Check for errors and print out results
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
