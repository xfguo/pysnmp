# Various GETNEXT Command Generator uses
from pysnmp.entity.rfc3413.oneliner import cmdgen

cmdGen = cmdgen.CommandGenerator()

# Send a series of SNMP GETNEXT requests
#     with SNMPv2c, community 'public'
#     over IPv4/UDP
#     to an Agent at localhost:161
#     for two OIDs in string form
#     stop when response OIDs leave the scopes of initial OIDs
errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.nextCmd(
    cmdgen.CommunityData('public'),
    cmdgen.UdpTransportTarget(('localhost', 161)),
    '1.3.6.1.2.1.2.2.1.2',
    '1.3.6.1.2.1.2.2.1.3',
)

if errorIndication:
    print(errorIndication)
else:
    if errorStatus:
        print('%s at %s' % (
            errorStatus.prettyPrint(),
            errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
            )
        )
    else:
        for varBindTableRow in varBindTable:
            for name, val in varBindTableRow:
                print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))


# Send a series of SNMP GETNEXT requests
#     with SNMPv1, community 'public'
#     over IPv4/UDP
#     to an Agent at localhost:161
#     for some columns of the IF-MIB::ifEntry table
#     stop when response OIDs leave the scopes of initial OIDs
# make sure IF-MIB.py is in search path
errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.nextCmd(
    cmdgen.CommunityData('public', mpModel=0),
    cmdgen.UdpTransportTarget(('localhost', 161)),
    cmdgen.MibVariable('IF-MIB', 'ifDescr'),
    cmdgen.MibVariable('IF-MIB', 'ifType'),
    cmdgen.MibVariable('IF-MIB', 'ifMtu'),
    cmdgen.MibVariable('IF-MIB', 'ifSpeed'),
    cmdgen.MibVariable('IF-MIB', 'ifPhysAddress')
)

if errorIndication:
    print(errorIndication)
else:
    if errorStatus:
        print('%s at %s' % (
            errorStatus.prettyPrint(),
            errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
            )
        )
    else:
        for varBindTableRow in varBindTable:
            for name, val in varBindTableRow:
                print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))


# Send a series of SNMP GETNEXT requests
#     with SNMPv3 with user 'usr-md5-des', MD5 auth and DES privacy protocols
#     over IPv6/UDP
#     to an Agent at [::1]:161
#     for all columns of the IF-MIB::ifEntry table
#     stop when response OIDs leave the scopes of the table
#     perform response OIDs and values resolution at MIB
# make sure IF-MIB.py is in search path
errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.nextCmd(
    cmdgen.UsmUserData('usr-md5-des', 'authkey1', 'privkey1'),
    cmdgen.Udp6TransportTarget(('::1', 161)),
    cmdgen.MibVariable('IF-MIB', 'ifEntry'),
    lookupNames=True, lookupValues=True
)

if errorIndication:
    print(errorIndication)
else:
    if errorStatus:
        print('%s at %s' % (
            errorStatus.prettyPrint(),
            errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
            )
        )
    else:
        for varBindTableRow in varBindTable:
            for name, val in varBindTableRow:
                print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))


# Send a series of SNMP GETNEXT requests
#     with SNMPv3, user 'usr-md5-none', MD5 authentication, no privacy
#     over IPv4/UDP
#     to an Agent at localhost:161
#     for all OIDs in IF-MIB
#     stop when response OIDs leave the scopes of the table
#     perform response values resolution at MIB
# make sure IF-MIB.py is in search path

errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.nextCmd(
    cmdgen.UsmUserData('usr-md5-none', 'authkey1'),
    cmdgen.UdpTransportTarget(('localhost', 161)),
    cmdgen.MibVariable('IF-MIB', ''),
    lookupValues=True
)

if errorIndication:
    print(errorIndication)
else:
    if errorStatus:
        print('%s at %s' % (
            errorStatus.prettyPrint(),
            errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
            )
        )
    else:
        for varBindTableRow in varBindTable:
            for name, val in varBindTableRow:
                print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))


# Send a series of SNMP GETNEXT requests
#     with SNMPv3, user 'usr-sha-aes128', SHA auth, AES128 privacy
#     over Local Domain Sockets
#     to an Agent at localhost:161
#     for all OIDs past IF-MIB
#     run till end-of-mib condition is reported by Agent OR maxRows == 100
#     ignoring non-increasing OIDs whenever reported by Agent
# make sure IF-MIB.py is search path

errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.nextCmd(
    cmdgen.UsmUserData('usr-sha-aes128', 'authkey1', 'privkey1',
                       authProtocol=cmdgen.usmHMACSHAAuthProtocol,
                       privProtocol=cmdgen.usmAesCfb128Protocol),
    cmdgen.UdpTransportTarget(('localhost', 161)),
    cmdgen.MibVariable('IF-MIB', ''),
    lexicographicMode=True, maxRows=100,
    ignoreNonIncreasingOid=True
)

if errorIndication:
    print(errorIndication)
else:
    if errorStatus:
        print('%s at %s' % (
            errorStatus.prettyPrint(),
            errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
            )
        )
    else:
        for varBindTableRow in varBindTable:
            for name, val in varBindTableRow:
                print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))

