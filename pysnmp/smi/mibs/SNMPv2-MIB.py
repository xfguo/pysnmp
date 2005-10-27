from pyasn1.type import constraint, namedval

( Integer, ObjectIdentifier ) = mibBuilder.importSymbols('ASN1', 'Integer', 'ObjectIdentifier')
( ModuleCompliance, NotificationGroup, ObjectGroup, ) = mibBuilder.importSymbols("SNMPv2-CONF", "ModuleCompliance", "NotificationGroup", "ObjectGroup")
( ModuleIdentity, ObjectIdentity, MibIdentifier, MibScalar, MibTable, MibTableRow, MibTableColumn, NotificationType, TimeTicks, Counter32, snmpModules, mib_2 ) = mibBuilder.importSymbols('SNMPv2-SMI', 'ModuleIdentity', 'ObjectIdentity','MibIdentifier', 'MibScalar', 'MibTable', 'MibTableRow','MibTableColumn', 'NotificationType', 'TimeTicks', 'Counter32','snmpModules', 'mib-2')
DisplayString, TestAndIncr, TimeStamp = mibBuilder.importSymbols('SNMPv2-TC', 'DisplayString', 'TestAndIncr', 'TimeStamp')

# Objects

system = MibIdentifier((1, 3, 6, 1, 2, 1, 1))
sysDescr = MibScalar((1, 3, 6, 1, 2, 1, 1, 1), DisplayString().subtype(subtypeSpec=constraint.ValueSizeConstraint(0, 255))).setMaxAccess("readonly")
sysObjectID = MibScalar((1, 3, 6, 1, 2, 1, 1, 2), ObjectIdentifier()).setMaxAccess("readonly")
sysUpTime = MibScalar((1, 3, 6, 1, 2, 1, 1, 3), TimeTicks()).setMaxAccess("readonly")
sysContact = MibScalar((1, 3, 6, 1, 2, 1, 1, 4), DisplayString().subtype(subtypeSpec=constraint.ValueSizeConstraint(0, 255))).setMaxAccess("readwrite")
sysName = MibScalar((1, 3, 6, 1, 2, 1, 1, 5), DisplayString().subtype(subtypeSpec=constraint.ValueSizeConstraint(0, 255))).setMaxAccess("readwrite")
sysLocation = MibScalar((1, 3, 6, 1, 2, 1, 1, 6), DisplayString().subtype(subtypeSpec=constraint.ValueSizeConstraint(0, 255))).setMaxAccess("readwrite")
sysServices = MibScalar((1, 3, 6, 1, 2, 1, 1, 7), Integer().subtype(subtypeSpec=constraint.ValueRangeConstraint(0, 127))).setMaxAccess("readonly")
sysORLastChange = MibScalar((1, 3, 6, 1, 2, 1, 1, 8), TimeStamp()).setMaxAccess("readonly")
sysORTable = MibTable((1, 3, 6, 1, 2, 1, 1, 9))
sysOREntry = MibTableRow((1, 3, 6, 1, 2, 1, 1, 9, 1)).setIndexNames((0, "SNMPv2-MIB", "sysORIndex"))
sysORIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 1, 9, 1, 1), Integer().subtype(subtypeSpec=constraint.ValueRangeConstraint(1, 2147483647L))).setMaxAccess("noaccess")
sysORID = MibTableColumn((1, 3, 6, 1, 2, 1, 1, 9, 1, 2), ObjectIdentifier()).setMaxAccess("readonly")
sysORDescr = MibTableColumn((1, 3, 6, 1, 2, 1, 1, 9, 1, 3), DisplayString()).setMaxAccess("readonly")
sysORUpTime = MibTableColumn((1, 3, 6, 1, 2, 1, 1, 9, 1, 4), TimeStamp()).setMaxAccess("readonly")
snmp = MibIdentifier((1, 3, 6, 1, 2, 1, 11))
snmpInPkts = MibScalar((1, 3, 6, 1, 2, 1, 11, 1), Counter32()).setMaxAccess("readonly")
snmpOutPkts = MibScalar((1, 3, 6, 1, 2, 1, 11, 2), Counter32()).setMaxAccess("readonly")
snmpInBadVersions = MibScalar((1, 3, 6, 1, 2, 1, 11, 3), Counter32()).setMaxAccess("readonly")
snmpInBadCommunityNames = MibScalar((1, 3, 6, 1, 2, 1, 11, 4), Counter32()).setMaxAccess("readonly")
snmpInBadCommunityUses = MibScalar((1, 3, 6, 1, 2, 1, 11, 5), Counter32()).setMaxAccess("readonly")
snmpInASNParseErrs = MibScalar((1, 3, 6, 1, 2, 1, 11, 6), Counter32()).setMaxAccess("readonly")
snmpInTooBigs = MibScalar((1, 3, 6, 1, 2, 1, 11, 8), Counter32()).setMaxAccess("readonly")
snmpInNoSuchNames = MibScalar((1, 3, 6, 1, 2, 1, 11, 9), Counter32()).setMaxAccess("readonly")
snmpInBadValues = MibScalar((1, 3, 6, 1, 2, 1, 11, 10), Counter32()).setMaxAccess("readonly")
snmpInReadOnlys = MibScalar((1, 3, 6, 1, 2, 1, 11, 11), Counter32()).setMaxAccess("readonly")
snmpInGenErrs = MibScalar((1, 3, 6, 1, 2, 1, 11, 12), Counter32()).setMaxAccess("readonly")
snmpInTotalReqVars = MibScalar((1, 3, 6, 1, 2, 1, 11, 13), Counter32()).setMaxAccess("readonly")
snmpInTotalSetVars = MibScalar((1, 3, 6, 1, 2, 1, 11, 14), Counter32()).setMaxAccess("readonly")
snmpInGetRequests = MibScalar((1, 3, 6, 1, 2, 1, 11, 15), Counter32()).setMaxAccess("readonly")
snmpInGetNexts = MibScalar((1, 3, 6, 1, 2, 1, 11, 16), Counter32()).setMaxAccess("readonly")
snmpInSetRequests = MibScalar((1, 3, 6, 1, 2, 1, 11, 17), Counter32()).setMaxAccess("readonly")
snmpInGetResponses = MibScalar((1, 3, 6, 1, 2, 1, 11, 18), Counter32()).setMaxAccess("readonly")
snmpInTraps = MibScalar((1, 3, 6, 1, 2, 1, 11, 19), Counter32()).setMaxAccess("readonly")
snmpOutTooBigs = MibScalar((1, 3, 6, 1, 2, 1, 11, 20), Counter32()).setMaxAccess("readonly")
snmpOutNoSuchNames = MibScalar((1, 3, 6, 1, 2, 1, 11, 21), Counter32()).setMaxAccess("readonly")
snmpOutBadValues = MibScalar((1, 3, 6, 1, 2, 1, 11, 22), Counter32()).setMaxAccess("readonly")
snmpOutGenErrs = MibScalar((1, 3, 6, 1, 2, 1, 11, 24), Counter32()).setMaxAccess("readonly")
snmpOutGetRequests = MibScalar((1, 3, 6, 1, 2, 1, 11, 25), Counter32()).setMaxAccess("readonly")
snmpOutGetNexts = MibScalar((1, 3, 6, 1, 2, 1, 11, 26), Counter32()).setMaxAccess("readonly")
snmpOutSetRequests = MibScalar((1, 3, 6, 1, 2, 1, 11, 27), Counter32()).setMaxAccess("readonly")
snmpOutGetResponses = MibScalar((1, 3, 6, 1, 2, 1, 11, 28), Counter32()).setMaxAccess("readonly")
snmpOutTraps = MibScalar((1, 3, 6, 1, 2, 1, 11, 29), Counter32()).setMaxAccess("readonly")
snmpEnableAuthenTraps = MibScalar((1, 3, 6, 1, 2, 1, 11, 30), Integer().subtype(subtypeSpec=constraint.SingleValueConstraint(2,1,)).subtype(namedValues=namedval.NamedValues(("enabled", 1), ("disabled", 2), ))).setMaxAccess("readwrite")
snmpSilentDrops = MibScalar((1, 3, 6, 1, 2, 1, 11, 31), Counter32()).setMaxAccess("readonly")
snmpProxyDrops = MibScalar((1, 3, 6, 1, 2, 1, 11, 32), Counter32()).setMaxAccess("readonly")
snmpMIB = ModuleIdentity((1, 3, 6, 1, 6, 3, 1))
snmpMIBObjects = MibIdentifier((1, 3, 6, 1, 6, 3, 1, 1))
snmpTrap = MibIdentifier((1, 3, 6, 1, 6, 3, 1, 1, 4))
snmpTrapOID = MibScalar((1, 3, 6, 1, 6, 3, 1, 1, 4, 1), ObjectIdentifier()).setMaxAccess("notifyonly")
snmpTrapEnterprise = MibScalar((1, 3, 6, 1, 6, 3, 1, 1, 4, 3), ObjectIdentifier()).setMaxAccess("notifyonly")
snmpTraps = MibIdentifier((1, 3, 6, 1, 6, 3, 1, 1, 5))
snmpSet = MibIdentifier((1, 3, 6, 1, 6, 3, 1, 1, 6))
snmpSetSerialNo = MibScalar((1, 3, 6, 1, 6, 3, 1, 1, 6, 1), TestAndIncr()).setMaxAccess("readwrite")
snmpMIBConformance = MibIdentifier((1, 3, 6, 1, 6, 3, 1, 2))
snmpMIBCompliances = MibIdentifier((1, 3, 6, 1, 6, 3, 1, 2, 1))
snmpMIBGroups = MibIdentifier((1, 3, 6, 1, 6, 3, 1, 2, 2))

# Augmentions

# Notifications

authenticationFailure = NotificationType((1, 3, 6, 1, 6, 3, 1, 1, 5, 5)).setObjects()
warmStart = NotificationType((1, 3, 6, 1, 6, 3, 1, 1, 5, 2)).setObjects()
coldStart = NotificationType((1, 3, 6, 1, 6, 3, 1, 1, 5, 1)).setObjects()

# Groups

snmpGroup = ObjectGroup((1, 3, 6, 1, 6, 3, 1, 2, 2, 8)).setObjects(("SNMPv2-MIB", "snmpEnableAuthenTraps"), ("SNMPv2-MIB", "snmpSilentDrops"), ("SNMPv2-MIB", "snmpInASNParseErrs"), ("SNMPv2-MIB", "snmpInPkts"), ("SNMPv2-MIB", "snmpInBadVersions"), ("SNMPv2-MIB", "snmpProxyDrops"), )
snmpWarmStartNotificationGroup = ObjectGroup((1, 3, 6, 1, 6, 3, 1, 2, 2, 11)).setObjects(("SNMPv2-MIB", "warmStart"), )
snmpObsoleteGroup = ObjectGroup((1, 3, 6, 1, 6, 3, 1, 2, 2, 10)).setObjects(("SNMPv2-MIB", "snmpOutNoSuchNames"), ("SNMPv2-MIB", "snmpInReadOnlys"), ("SNMPv2-MIB", "snmpInTotalReqVars"), ("SNMPv2-MIB", "snmpInSetRequests"), ("SNMPv2-MIB", "snmpOutGenErrs"), ("SNMPv2-MIB", "snmpOutGetRequests"), ("SNMPv2-MIB", "snmpOutPkts"), ("SNMPv2-MIB", "snmpOutBadValues"), ("SNMPv2-MIB", "snmpOutTraps"), ("SNMPv2-MIB", "snmpInNoSuchNames"), ("SNMPv2-MIB", "snmpInGetNexts"), ("SNMPv2-MIB", "snmpInGetRequests"), ("SNMPv2-MIB", "snmpOutGetResponses"), ("SNMPv2-MIB", "snmpInGenErrs"), ("SNMPv2-MIB", "snmpInTraps"), ("SNMPv2-MIB", "snmpInTotalSetVars"), ("SNMPv2-MIB", "snmpInGetResponses"), ("SNMPv2-MIB", "snmpOutSetRequests"), ("SNMPv2-MIB", "snmpInBadValues"), ("SNMPv2-MIB", "snmpInTooBigs"), ("SNMPv2-MIB", "snmpOutGetNexts"), ("SNMPv2-MIB", "snmpOutTooBigs"), )
snmpBasicNotificationsGroup = ObjectGroup((1, 3, 6, 1, 6, 3, 1, 2, 2, 7)).setObjects(("SNMPv2-MIB", "authenticationFailure"), ("SNMPv2-MIB", "coldStart"), )
snmpCommunityGroup = ObjectGroup((1, 3, 6, 1, 6, 3, 1, 2, 2, 9)).setObjects(("SNMPv2-MIB", "snmpInBadCommunityNames"), ("SNMPv2-MIB", "snmpInBadCommunityUses"), )
snmpNotificationGroup = ObjectGroup((1, 3, 6, 1, 6, 3, 1, 2, 2, 12)).setObjects(("SNMPv2-MIB", "snmpTrapOID"), ("SNMPv2-MIB", "snmpTrapEnterprise"), )
systemGroup = ObjectGroup((1, 3, 6, 1, 6, 3, 1, 2, 2, 6)).setObjects(("SNMPv2-MIB", "sysName"), ("SNMPv2-MIB", "sysObjectID"), ("SNMPv2-MIB", "sysORLastChange"), ("SNMPv2-MIB", "sysORID"), ("SNMPv2-MIB", "sysLocation"), ("SNMPv2-MIB", "sysServices"), ("SNMPv2-MIB", "sysUpTime"), ("SNMPv2-MIB", "sysORDescr"), ("SNMPv2-MIB", "sysORUpTime"), ("SNMPv2-MIB", "sysDescr"), ("SNMPv2-MIB", "sysContact"), )
snmpSetGroup = ObjectGroup((1, 3, 6, 1, 6, 3, 1, 2, 2, 5)).setObjects(("SNMPv2-MIB", "snmpSetSerialNo"), )

# Exports

# Objects
mibBuilder.exportSymbols("SNMPv2-MIB", system=system, sysDescr=sysDescr, sysObjectID=sysObjectID, sysUpTime=sysUpTime, sysContact=sysContact, sysName=sysName, sysLocation=sysLocation, sysServices=sysServices, sysORLastChange=sysORLastChange, sysORTable=sysORTable, sysOREntry=sysOREntry, sysORIndex=sysORIndex, sysORID=sysORID, sysORDescr=sysORDescr, sysORUpTime=sysORUpTime, snmp=snmp, snmpInPkts=snmpInPkts, snmpOutPkts=snmpOutPkts, snmpInBadVersions=snmpInBadVersions, snmpInBadCommunityNames=snmpInBadCommunityNames, snmpInBadCommunityUses=snmpInBadCommunityUses, snmpInASNParseErrs=snmpInASNParseErrs, snmpInTooBigs=snmpInTooBigs, snmpInNoSuchNames=snmpInNoSuchNames, snmpInBadValues=snmpInBadValues, snmpInReadOnlys=snmpInReadOnlys, snmpInGenErrs=snmpInGenErrs, snmpInTotalReqVars=snmpInTotalReqVars, snmpInTotalSetVars=snmpInTotalSetVars, snmpInGetRequests=snmpInGetRequests, snmpInGetNexts=snmpInGetNexts, snmpInSetRequests=snmpInSetRequests, snmpInGetResponses=snmpInGetResponses, snmpInTraps=snmpInTraps, snmpOutTooBigs=snmpOutTooBigs, snmpOutNoSuchNames=snmpOutNoSuchNames, snmpOutBadValues=snmpOutBadValues, snmpOutGenErrs=snmpOutGenErrs, snmpOutGetRequests=snmpOutGetRequests, snmpOutGetNexts=snmpOutGetNexts, snmpOutSetRequests=snmpOutSetRequests, snmpOutGetResponses=snmpOutGetResponses, snmpOutTraps=snmpOutTraps, snmpEnableAuthenTraps=snmpEnableAuthenTraps, snmpSilentDrops=snmpSilentDrops, snmpProxyDrops=snmpProxyDrops, snmpMIB=snmpMIB, snmpMIBObjects=snmpMIBObjects, snmpTrap=snmpTrap, snmpTrapOID=snmpTrapOID, snmpTrapEnterprise=snmpTrapEnterprise, snmpTraps=snmpTraps, snmpSet=snmpSet, snmpSetSerialNo=snmpSetSerialNo, snmpMIBConformance=snmpMIBConformance, snmpMIBCompliances=snmpMIBCompliances, snmpMIBGroups=snmpMIBGroups)

# Notifications
mibBuilder.exportSymbols("SNMPv2-MIB", authenticationFailure=authenticationFailure, warmStart=warmStart, coldStart=coldStart)

# Groups
mibBuilder.exportSymbols("SNMPv2-MIB", snmpGroup=snmpGroup, snmpWarmStartNotificationGroup=snmpWarmStartNotificationGroup, snmpObsoleteGroup=snmpObsoleteGroup, snmpBasicNotificationsGroup=snmpBasicNotificationsGroup, snmpCommunityGroup=snmpCommunityGroup, snmpNotificationGroup=snmpNotificationGroup, systemGroup=systemGroup, snmpSetGroup=snmpSetGroup)
