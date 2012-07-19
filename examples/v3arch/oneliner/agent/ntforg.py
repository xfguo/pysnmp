# Various uses of the Notification Originator (TRAP/INFORM)
from pysnmp.entity.rfc3413.oneliner import ntforg
from pysnmp.proto import rfc1902

ntfOrg = ntforg.NotificationOriginator()

# Using
#     SNMPv2c
#     over IPv4/UDP
#     send TRAP notification
#     with TRAP ID 'coldStart' specified as a MIB symbol
#     include managed object information specified as a MIB symbol
errorIndication = ntfOrg.sendNotification(
    ntforg.CommunityData('public'),
    ntforg.UdpTransportTarget(('localhost', 162)),
    'trap',
    (('SNMPv2-MIB', 'coldStart'),),
    # MIB symbol: ((mib-name, mib-symbol), instance-id), new-value
    ((('SNMPv2-MIB', 'sysName'), 0), 'new name')
    )

if errorIndication:
    print('Notification not sent: %s' % errorIndication)

# Using
#     SNMPv1
#     over IPv4/UDP
#     send TRAP notification
#     with Generic Trap #6 (enterpriseSpecific) and Specific Trap 432
#     with Uptime value 12345
#     with Agent Address '127.0.0.1'
#     with Enterprise OID 1.3.6.1.4.1.20408.4.1.1.2
#     include managed object information '1.3.6.1.2.1.1.1.0' = 'my system'
errorIndication = ntfOrg.sendNotification(
    ntforg.CommunityData('public', mpModel=0),
    ntforg.UdpTransportTarget(('localhost', 162)),
    'trap',
    '1.3.6.1.4.1.20408.4.1.1.2.0.432',
    ('1.3.6.1.2.1.1.3.0', 12345),
    ('1.3.6.1.6.3.18.1.3.0', '127.0.0.1'),
    ('1.3.6.1.6.3.1.1.4.3.0', '1.3.6.1.4.1.20408.4.1.1.2'),
    ('1.3.6.1.2.1.1.1.0', rfc1902.OctetString('my system'))
    )

if errorIndication:
    print('Notification not sent: %s' % errorIndication)

# Using
#     SNMPv1
#     over IPv4/UDP
#     send TRAP notification
#     with Generic Trap #1 (warmStart) and Specific Trap 0
#     with default Uptime
#     with default Agent Address
#     with Enterprise OID 1.3.6.1.4.1.20408.4.1.1.2
#     include managed object information '1.3.6.1.2.1.1.1.0' = 'my system'
errorIndication = ntfOrg.sendNotification(
    ntforg.CommunityData('public', mpModel=0),
    ntforg.UdpTransportTarget(('localhost', 162)),
    'trap',
    '1.3.6.1.6.3.1.1.5.2',
    ('1.3.6.1.6.3.1.1.4.3.0', '1.3.6.1.4.1.20408.4.1.1.2'),
    ('1.3.6.1.2.1.1.1.0', rfc1902.OctetString('my system'))
    )

if errorIndication:
    print('Notification not sent: %s' % errorIndication)

# Using
#     SNMPv3 user 'usr-md5-des', auth: MD5, priv 3DES
#     over IPv4/UDP
#     send INFORM notification
#     with TRAP ID 'warmStart' specified as a string OID
#     include managed object information 1.3.6.1.2.1.1.5.0 = 'system name'
errorIndication = ntfOrg.sendNotification(
    ntforg.UsmUserData('usr-md5-des', 'authkey1', 'privkey1'),
    ntforg.UdpTransportTarget(('localhost', 162)),
    'inform',
    '1.3.6.1.6.3.1.1.5.2',
    ('1.3.6.1.2.1.1.5.0', rfc1902.OctetString('system name'))
    )

if errorIndication:
    print('Notification not sent: %s' % errorIndication)

# Using
#     SNMPv3 user 'usr-sha-aes', auth: SHA, priv: AES128
#     over IPv6/UDP
#     send TRAP notification
#     with TRAP ID 'authenticationFailure' specified as a MIB symbol
#     include managed object information 1.3.6.1.2.1.1.1.0 = 'my system'
#     include managed object information 1.3.6.1.2.1.1.3.0 = 567
errorIndication = ntfOrg.sendNotification(
    ntforg.UsmUserData('usr-sha-aes', 'authkey1', 'privkey1',
                       authProtocol=ntforg.usmHMACSHAAuthProtocol,
                       privProtocol=ntforg.usmAesCfb128Protocol),
    ntforg.Udp6TransportTarget(('::1', 162)),
    'trap',
    (('SNMPv2-MIB', 'authenticationFailure'),),
    ('1.3.6.1.2.1.1.1.0', rfc1902.OctetString('my system')),
    ('1.3.6.1.2.1.1.3.0', rfc1902.TimeTicks(567))
    )

if errorIndication:
    print('Notification not sent: %s' % errorIndication)


# Using
#     SNMPv3 user 'usr-none-none', no auth, no priv
#     over Local Domain Socket /tmp/snmp-manager
#     send TRAP notification
#     with TRAP ID 'authenticationFailure' specified as a MIB symbol
#     include managed object information 1.3.6.1.2.1.1.2.0 = 1.3.6.1.2.1.1.1
errorIndication = ntfOrg.sendNotification(
    ntforg.UsmUserData('test-user'),
    ntforg.UnixTransportTarget('/tmp/snmp-manager'),
    'trap',
    (('SNMPv2-MIB', 'authenticationFailure'),),
    ('1.3.6.1.2.1.1.2.0', rfc1902.ObjectName('1.3.6.1.2.1.1.1'))
    )

if errorIndication:
    print('Notification not sent: %s' % errorIndication)

