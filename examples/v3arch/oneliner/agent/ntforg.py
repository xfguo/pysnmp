from pysnmp.entity.rfc3413.oneliner import ntforg
from pysnmp.proto.api import v2c

errorIndication = ntforg.NotificationOriginator().sendNotification(
    # SNMP v1
    ntforg.CommunityData('test-manager', 'public', 0),
    # SNMP v2
#    ntforg.CommunityData('test-manager', 'public'),
    # SNMP v3
#    ntforg.UsmUserData('test-manager', 'authkey1', 'privkey1'),
    ntforg.UdpTransportTarget(('localhost', 1162)),
    ('SNMPv2-MIB', 'coldStart')#, ((1,3,6,1,2,1,1,3,0), v2c.Integer(32))
    )

if errorIndication:
    print errorIndication
