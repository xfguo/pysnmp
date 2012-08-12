# Various uses of GET Command Generator uses
from pysnmp.entity.rfc3413.oneliner import cmdgen

cmdGen = cmdgen.CommandGenerator()

# Send SNMP GET request
#     with SNMPv2c, community 'public'
#     over IPv4/UDP
#     to an Agent at localhost:161
#     for two OIDs in string form 
errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
    cmdgen.CommunityData('public'),
    cmdgen.UdpTransportTarget(('localhost', 161)),
    '1.3.6.1.2.1.1.1.0',
    '1.3.6.1.2.1.1.6.0'
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


# Send SNMP GET request
#     with SNMPv1, community 'public'
#     over IPv4/UDP
#     to an Agent at localhost:161
#     for two instances of SNMPv2-MIB::sysDescr.0 MIB object,
#     one in label and another in MIB symbol form
errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
    cmdgen.CommunityData('public', mpModel=0),
    cmdgen.UdpTransportTarget(('localhost', 161)),
    cmdgen.MibVariable('iso.org.dod.internet.mgmt.mib-2.system.sysDescr.0'),
    cmdgen.MibVariable('SNMPv2-MIB', 'sysDescr', 0)
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


# Send SNMP GET request
#     with SNMPv3 with user 'usr-md5-des', MD5 auth and DES privacy protocols
#     over IPv6/UDP
#     to an Agent at [::1]:161
#     for three OIDs: one passed as a MibVariable object while others are
#     in string form
errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
    cmdgen.UsmUserData('usr-md5-des', 'authkey1', 'privkey1'),
    cmdgen.Udp6TransportTarget(('::1', 161)),
    cmdgen.MibVariable('1.3.6.1.2.1.1.1.0'),
    '1.3.6.1.2.1.1.2.0',
    '1.3.6.1.2.1.1.3.0'
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


# Send SNMP GET request
#     with SNMPv3, user 'usr-md5-none', MD5 authentication, no privacy
#     over IPv4/UDP
#     to an Agent at localhost:161
#     for IP-MIB::ipAdEntAddr.127.0.0.1 MIB object
errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
    cmdgen.UsmUserData('usr-md5-none', 'authkey1'),
    cmdgen.UdpTransportTarget(('localhost', 161)),
    cmdgen.MibVariable('IP-MIB', 'ipAdEntAddr', '127.0.0.1')
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


# Send SNMP GET request
#     with SNMPv3, user 'usr-none-none', no authentication, no privacy
#     over IPv4/UDP
#     to an Agent at localhost:161
#     for IP-MIB::ipAdEntAddr.127.0.0.1 MIB object
#     perform response OIDs and values resolution at MIB

errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
    cmdgen.UsmUserData('usr-none-none'),
    cmdgen.UdpTransportTarget(('localhost', 161)),
    cmdgen.MibVariable('IP-MIB', 'ipAdEntAddr', '127.0.0.1'),
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


# Send SNMP GET request
#     with SNMPv3, user 'usr-sha-aes128', SHA auth, AES128 privacy
#     over IPv4/UDP
#     to an Agent at /tmp/snmp-agent
#     for TCP-MIB::tcpConnLocalAddress."0.0.0.0".22."0.0.0.0".0 MIB object
errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
    cmdgen.UsmUserData('usr-sha-aes128', 'authkey1', 'privkey1',
                       authProtocol=cmdgen.usmHMACSHAAuthProtocol,
                       privProtocol=cmdgen.usmAesCfb128Protocol ),
    cmdgen.UdpTransportTarget(('localhost', 161)),
    cmdgen.MibVariable('TCP-MIB', 'tcpConnLocalAddress', '0.0.0.0', 22, '0.0.0.0', 0)
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

