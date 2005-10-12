from pysnmp.entity.rfc3413.oneliner import ntforg
from pysnmp.proto.api import v2c

errorIndication = ntforg.NotificationOriginator().sendNotification(
    # SNMP v1
#    ntforg.CommunityData('test-manager', 'public', 0),
    # SNMP v2
#   ntforg.CommunityData('test-manager', 'public'),
    # SNMP v3
    ntforg.UsmUserData('test-user', 'authkey1', 'privkey1'),
    ntforg.UdpTransportTarget(('localhost', 162)),
    'trap',
    ('SNMPv2-MIB', 'coldStart'),
    (((1,3,6,1,2,1,1,3,0), v2c.TimeTicks(44100)),)
    )

if errorIndication:
    print errorIndication

# XXX
# informs require cbFun?
# responses do not come back for informs
