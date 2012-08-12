import sys
from pysnmp.proto import rfc1902
from pysnmp.error import PySnmpError
from pyasn1.error import PyAsn1Error

#
# An OID-like object that embeds MIB resolution.
#
# Valid initializers include:
# MibVariable('1.3.6.1.2.1.1.1.0'),
# MibVariable('iso.org.dod.internet.mgmt.mib-2.system.sysDescr.0')
# MibVariable('SNMPv2-MIB', 'system'),
# MibVariable('SNMPv2-MIB', 'sysDescr', 0),
# MibVariable('IP-MIB', 'ipAdEntAddr', '127.0.0.1', 123),
# 

class MibVariable:
    stDirty, stOidOnly, stClean, stUnresolved = 1, 2, 4, 8
        
    def __init__(self, *args):
        self.__args = args
        self.__modNamesToLoad = None
        self.__state  = self.stDirty

    #
    # public API
    #
    def getMibSymbol(self):
        if self.__state & self.stClean:
            return self.__modName, self.__symName, self.__indices
        else:
            raise PySnmpError('%s object not fully initialized' % self.__class__.__name__)

    def getOid(self):
        if self.__state & (self.stOidOnly | self.stClean):
            return self.__oid
        else:
            raise PySnmpError('%s object not fully initialized' % self.__class__.__name__)

    def getLabel(self):
        if self.__state & self.stClean:
            return self.__label
        else:
            raise PySnmpError('%s object not fully initialized' % self.__class__.__name__)

    def getMibNode(self):  # XXX
        if self.__state & self.stClean:
            return self.__mibNode
        else:
            raise PySnmpError('%s object not fully initialized' % self.__class__.__name__)
   
    def isFullyResolved(self):
        return not (self.__state & self.stUnresolved)

    # a gateway to MibViewController to perform a deferred load
    def loadMibs(self, *modNames):
        self.__modNamesToLoad = modNames
        return self

    # this would eventually be called by an entity which posses a
    # reference to MibViewController
    def resolveWithMib(self, mibViewController, oidOnly=False):
        if self.__modNamesToLoad is not None:
            mibViewController.mibBuilder.loadModules(*self.__modNamesToLoad)
            self.__modNamesToLoad = None

        if self.__state & (self.stOidOnly | self.stClean):
            return self

        MibScalar, MibTableColumn, = mibViewController.mibBuilder.importSymbols(
            'SNMPv2-SMI', 'MibScalar', 'MibTableColumn'
        )

        if len(self.__args) == 1:  # OID or label
            try:
                self.__oid = rfc1902.ObjectName(self.__args[0])
            except PyAsn1Error:
                try:
                    label = tuple(self.__args[0].split('.'))
                except ValueError:
                    raise PySnmpError('Bad OID format %s' % (self.__args[0],))
                prefix, label, suffix = mibViewController.getNodeNameByOid(
                    label
                )
             
                if suffix:
                    try:
                        suffix = tuple([ int(x) for x in suffix ])
                    except ValueError:
                        raise PySnmpError('Unknown object name component %s' % (suffix,))

                self.__oid = rfc1902.ObjectName(prefix + suffix)

                self.__state |= self.stOidOnly

                if oidOnly:
                    return self
            else:
                self.__state |= self.stOidOnly

                if oidOnly:
                    return self

                prefix, label, suffix = mibViewController.getNodeNameByOid(
                    self.__oid
                )

            modName, symName, _ = mibViewController.getNodeLocation(prefix)

            self.__modName = modName
            self.__symName = symName

            self.__label = label

            mibNode, = mibViewController.mibBuilder.importSymbols(
                modName, symName
            )

            self.__mibNode = mibNode

            if isinstance(mibNode, MibTableColumn): # table column
                rowModName, rowSymName, _ = mibViewController.getNodeLocation(
                    mibNode.name[:-1]
                )
                rowNode, = mibViewController.mibBuilder.importSymbols(
                    rowModName, rowSymName
                )
                self.__indices = rowNode.getIndicesFromInstId(suffix)
            elif isinstance(mibNode, MibScalar): # scalar
                self.__indices = ( rfc1902.ObjectName(suffix), )
            else:
                self.__indices = ( rfc1902.ObjectName(suffix), )
                if suffix:
                    self.__state |= self.stUnresolved
            self.__state |= self.stClean
            return self
        elif len(self.__args) > 1:  # MIB, symbol[, index, index ...]
            self.__modName = self.__args[0]
            if self.__args[1]:
                self.__symName = self.__args[1]
            else:
                oid, _, _ = mibViewController.getFirstNodeName(self.__args[0])
                _, self.__symName, _ = mibViewController.getNodeLocation(oid)

            mibNode, = mibViewController.mibBuilder.importSymbols(
                self.__modName, self.__symName
            )

            self.__mibNode = mibNode

            self.__indices = ()
            self.__oid = rfc1902.ObjectName(mibNode.getName())

            prefix, label, suffix = mibViewController.getNodeNameByOid(
                self.__oid
            )
            self.__label = label

            if isinstance(mibNode, MibTableColumn): # table
                rowModName, rowSymName, _ = mibViewController.getNodeLocation(
                    mibNode.name[:-1]
                )
                rowNode, = mibViewController.mibBuilder.importSymbols(
                    rowModName, rowSymName
                )
                if self.__args[2:]:
                    instIds = rowNode.getInstIdFromIndices(*self.__args[2:])
                    self.__oid += instIds
                    self.__indices = rowNode.getIndicesFromInstId(instIds)
            elif self.__args[2:]: # any other kind of MIB node with indices
                instId = rfc1902.ObjectName(
                    '.'.join([ str(x) for x in self.__args[2:] ])
                )
                self.__oid += instId
                self.__indices = ( instId, )
            self.__state |= (self.stClean | self.stOidOnly)
            return self
        else:
            raise PySnmpError('Non-OID, label or MIB symbol')

    def prettyPrint(self):
        if self.__state & self.stClean:
            return '%s::%s.%s' % (
                self.__modName, self.__symName,
                '.'.join(['"%s"' % x.prettyPrint() for x in self.__indices ])
            )
        else:
            raise PySnmpError('%s object not fully initialized' % self.__class__.__name__)
 
    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, ', '.join([ repr(x) for x in self.__args]))

   # Redirect some attrs access to the OID object to behave alike

    def __getattr__(self, attr):
        if self.__state & self.stOidOnly:
            if attr in ('__str__', '__getitem__', '__eq__', '__ne__',
                        '__lt__', '__le__', '__ge__', '__ge__',
                        '__nonzero__', '__bool__', '__hash__', '__len__',
                        '__index__',
                        'asTuple', 'clone', 'subtype', 'isPrefixOf'):
                return getattr(self.__oid, attr)
            raise AttributeError
        else:
            raise PySnmpError('%s object not properly initialized' % self.__class__.__name__)

