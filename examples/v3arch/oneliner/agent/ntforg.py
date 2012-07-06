# Notification Originator (TRAP/INFORM)
from pysnmp.entity.rfc3413.oneliner import ntforg
from pysnmp.proto import rfc1902

ntfOrg = ntforg.NotificationOriginator()

errorIndication = ntfOrg.sendNotification(
    # SNMP v1
#    ntforg.CommunityData('public', mpModel=0),
    # SNMP v2c
#   ntforg.CommunityData('public'),
    # SNMP v3:
    # auth MD5, privacy DES
    ntforg.UsmUserData('test-user', 'authkey1', 'privkey1'),
    # auth MD5, privacy NONE
#    ntforg.UsmUserData('test-user', 'authkey1'),
    # auth NONE, privacy NONE
#    ntforg.UsmUserData('test-user'),
    # auth SHA, privacy AES128
#    ntforg.UsmUserData('test-user', 'authkey1', 'privkey1',
#                       authProtocol=ntforg.usmHMACSHAAuthProtocol,
#                       privProtocol=ntforg.usmAesCfb128Protocol ),
    # Transport options:
    # IPv4/UDP
    ntforg.UdpTransportTarget(('localhost', 162)),
    # IPv6/UDP
#    ntforg.Udp6TransportTarget(('::1', 162)),
    # Local (UNIX) domain socket
#    ntforg.UnixTransportTarget('/tmp/snmp-agent'),
    # Trap type (TRAP | INFORM)
    'trap',
#    'inform',
    # Trap OID
    (('SNMPv2-MIB', 'coldStart'),),
    # Objects to include into TRAP message:
    # MIB symbol: ((mib-name, mib-symbol), instance-id), new-value
    ((('SNMPv2-MIB', 'sysName'), 0), 'new name'),
    # OID in string form, rfc1902 class instance value
    ('1.3.6.1.2.1.1.5.0', rfc1902.OctetString('new name'))
    )

if errorIndication:
    print('Notification not sent: %s' % errorIndication)
