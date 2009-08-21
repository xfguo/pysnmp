# Notification Originator (TRAP/INFORM)
from pysnmp.entity.rfc3413.oneliner import ntforg
from pysnmp.proto import rfc1902

ntforg.NotificationOriginator().sendNotification(
    # SNMP v1
#    ntforg.CommunityData('test-manager', 'public', 0),
    # SNMP v2
#   ntforg.CommunityData('test-manager', 'public'),
    # SNMP v3
    ntforg.UsmUserData('test-user', 'authkey1', 'privkey1'),
    ntforg.UdpTransportTarget(('localhost', 162)),
    # Trap type
#    'trap',
    'inform',
    # Trap OID
    (('SNMPv2-MIB', 'coldStart'),),
    # MIB symbol name, plain string value
    ((('SNMPv2-MIB', 'sysName'), 0), 'new name'),
    # Plain OID name, rfc1902 class instance value
    ((1,3,6,1,2,1,1,5,0), rfc1902.OctetString('new name'))
    )
