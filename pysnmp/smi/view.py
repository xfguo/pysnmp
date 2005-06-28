# MIB modules management
from types import ClassType, InstanceType, TupleType
from pysnmp.smi.indices import OrderedDict, OidOrderedDict
from pysnmp.smi import error

__all__ = [ 'MibViewController' ]

class MibViewController:
    def __init__(self, mibBuilder):
        self.mibBuilder = mibBuilder
        self.lastBuildId = -1

    # Indexing part
    
    def __indexMib(self):
        if self.lastBuildId == self.mibBuilder.lastBuildId:
            return

        #
        # Create indices
        #
        
        # Module name -> module-scope indices
        self.__mibSymbolsIdx = OrderedDict()
        # Oid <-> label indices
        
        # Index modules names
        for modName in [ '' ] + self.mibBuilder.mibSymbols.keys():
            # Modules index
            self.__mibSymbolsIdx[modName] = mibMod = {
                'oidToLabelIdx': OidOrderedDict(),
                'labelToOidIdx': {},
                'varToNameIdx': {},
                'typeToModIdx': OrderedDict(),
                'oidToModIdx': {}
                }

            if not modName:
                globMibMod = mibMod
                continue

            # Types & MIB vars indices
            for n, v in self.mibBuilder.mibSymbols[modName].items():
                if type(v) == ClassType:
                    if mibMod['typeToModIdx'].has_key(n):
                        raise error.SmiError(
                            'Duplicate SMI type %s::%s, has %s' % \
                            (modName, n, mibMod['typeToModIdx'][n])
                            )
                    if not globMibMod['typeToModIdx'].has_key(n):
                        globMibMod['typeToModIdx'][n] = modName
                    mibMod['typeToModIdx'][n] = modName
                elif type(v) == InstanceType:
                    if mibMod['varToNameIdx'].has_key(n):
                        raise error.SmiError(
                            'Duplicate MIB variable %s::%s has %s' % \
                            (modName, n, mibMod['varToNameIdx'][n])
                            )
                    if not globMibMod['varToNameIdx'].has_key(n):
                        globMibMod['varToNameIdx'][n] = v.name
                    mibMod['varToNameIdx'][n] = v.name
                    if not globMibMod['oidToModIdx'].has_key(v.name):
                        globMibMod['oidToModIdx'][v.name] = modName
                    mibMod['oidToModIdx'][v.name] = modName
                    if not globMibMod['oidToLabelIdx'].has_key(v.name):
                        globMibMod['oidToLabelIdx'][v.name] = (n, )
                    mibMod['oidToLabelIdx'][v.name] = (n, )
# XXX complain
#                         raise error.SmiError(
#                             'Duplicate MIB variable name %s::%s has %s' % 
#                             (modName, v.name, globMibMod['oidToLabelIdx'][v.name])
#                             )
                else:
                    raise error.SmiError(
                        'Unexpected object %s::%s' % (modName, n)
                        )
            
        # Build oid->long-label index
        oidToLabelIdx = self.__mibSymbolsIdx['']['oidToLabelIdx']
        labelToOidIdx = self.__mibSymbolsIdx['']['labelToOidIdx']
        if oidToLabelIdx:
            prevOid = oidToLabelIdx.keys()[0]
        else:
            prevOid = ()
        baseLabel = ()
        for key in oidToLabelIdx.keys():
            keydiff = len(key) - len(prevOid)
            if keydiff > 0:
                baseLabel = oidToLabelIdx[prevOid]
                if keydiff > 1:
                    baseLabel = baseLabel + key[-keydiff:-1]
            if keydiff < 0:
                keyLen = len(key)
                i = keyLen-1
                while i:
                    baseLabel = oidToLabelIdx.get(key[:i])
                    if baseLabel:
                        if i != keyLen-1:
                            baseLabel = baseLabel + key[i:-1]
                        break
                    i = i - 1
            # Build oid->long-label index
            oidToLabelIdx[key] = baseLabel + oidToLabelIdx[key]
            # Build label->oid index
            labelToOidIdx[oidToLabelIdx[key]] = key
            prevOid = key

        # Build module-scope oid->long-label index
        for mibMod in self.__mibSymbolsIdx.values():
            for oid in mibMod['oidToLabelIdx'].keys():
                mibMod['oidToLabelIdx'][oid] = oidToLabelIdx[oid]
                mibMod['labelToOidIdx'][oidToLabelIdx[oid]] = oid
            
        self.lastBuildId = self.mibBuilder.lastBuildId

    # Module management
    
    def getFirstModuleName(self):
        self.__indexMib()
        modNames = self.__mibSymbolsIdx.keys()
        if modNames:
            return modNames[0]
        raise error.SmiError('No modules loaded at %s' % self)

    def getNextModuleName(self, modName):
        self.__indexMib()
        try:
            return self.__mibSymbolsIdx.nextKey(modName)
        except KeyError:
            raise error.SmiError(
                'No module next to %s at %s' % (modName, self)
                )

    # MIB tree node management

    def __getOidLabel(self, nodeName, oidToLabelIdx, labelToOidIdx):
        """getOidLabel(nodeName) -> (oid, label, suffix)"""
        if not nodeName:
            return nodeName, nodeName, ()
        oid = labelToOidIdx.get(nodeName)
        if oid:
            return oid, nodeName, ()
        label = oidToLabelIdx.get(nodeName)
        if label:
            return nodeName, label, ()
        if len(nodeName) < 2:
            return nodeName, nodeName, ()
        oid, label, suffix = self.__getOidLabel(
            nodeName[:-1], oidToLabelIdx, labelToOidIdx
            )
        suffix = suffix + nodeName[-1:]
        resLabel = label + suffix
        resOid = labelToOidIdx.get(resLabel)
        if resOid:
            return resOid, resLabel, ()
        resOid = oid + suffix
        resLabel = oidToLabelIdx.get(resOid)
        if resLabel:
            return resOid, resLabel, ()
        return oid, label, suffix

    def getNodeNameByOid(self, nodeName, modName=''):
        self.__indexMib()        
        mibMod = self.__mibSymbolsIdx.get(modName)
        if mibMod is None:
            raise error.SmiError(
                'No module %s at %s' % (modName, self)
                )
        oid, label, suffix = self.__getOidLabel(
            nodeName, mibMod['oidToLabelIdx'], mibMod['labelToOidIdx']
            )
        if oid == label:
            raise error.NoSuchInstanceError(
                str='Can\'t resolve node name %s::%s at %s' % 
                (modName, nodeName, self)
                )
        return oid, label, suffix

    def getNodeNameByDesc(self, nodeName, modName=''):
        self.__indexMib()        
        mibMod = self.__mibSymbolsIdx.get(modName)
        if mibMod is None:
            raise error.SmiError(
                'No module %s at %s' % (modName, self)
                )
        oid = mibMod['varToNameIdx'].get(nodeName)
        if oid is None:
            raise error.NoSuchInstanceError(
                str='No such symbol %s::%s at %s' % (modName, nodeName, self)
                )
        return self.getNodeNameByOid(oid, modName)

    def getNodeName(self, nodeName, modName=''):
        if type(nodeName) == TupleType:
            return self.getNodeNameByOid(nodeName, modName)
        else:
            return self.getNodeNameByDesc(nodeName, modName)

    def getFirstNodeName(self, modName=''):
        self.__indexMib()        
        mibMod = self.__mibSymbolsIdx.get(modName)
        if mibMod is None:
            raise error.SmiError(
                'No module %s at %s' % (modName, self)
                )
        if not mibMod['oidToLabelIdx']:
            raise error.NoSuchInstanceError(
                str='No variables at MIB module %s at %s' % (modName, self)
                )
        oid, label = mibMod['oidToLabelIdx'].items()[0]
        return oid, label, ()
        
    def getNextNodeName(self, nodeName, modName=''):
        oid, label, suffix = self.getNodeName(nodeName, modName)
        try:
            return self.getNodeName(
                self.__mibSymbolsIdx[modName]['oidToLabelIdx'].nextKey(oid) + suffix,
                modName
                )
        except KeyError:
            raise error.NoSuchInstanceError(
                str='No name next to %s::%s at %s' % (modName, nodeName, self)
                )
    
    def getParentNodeName(self, nodeName, modName=''):
        oid, label, suffix = self.getNodeName(nodeName, modName)
        if len(oid) < 2:
            raise error.NoSuchInstanceError(
                str='No parent name for %s::%s at %s' %
                (modName, nodeName, self)
                )
        return oid[:-1], label[:-1], oid[-1:] + suffix

    def getNodeLocation(self, nodeName, modName=''):
        oid, label, suffix = self.getNodeName(nodeName, modName)
        return self.__mibSymbolsIdx['']['oidToModIdx'][oid], label[-1], suffix
    
    # MIB type management

    def getTypeName(self, typeName, modName=''):
        self.__indexMib()
        mibMod = self.__mibSymbolsIdx.get(modName)
        if mibMod is None:
            raise error.SmiError(
                'No module %s at %s' % (modName, self)
                )
        m = mibMod['typeToModIdx'].get(typeName)
        if m is None:
            raise error.NoSuchInstanceError(
                str='No such type %s::%s at %s' % (modName, typeName, self)
                )
        return m, typeName
        
    def getFirstTypeName(self, modName=''):
        self.__indexMib()
        mibMod = self.__mibSymbolsIdx.get(modName)
        if mibMod is None:
            raise error.SmiError(
                'No module %s at %s' % (modName, self)
                )
        if not mibMod['typeToModIdx']:
            raise error.NoSuchInstanceError(
                str='No types at MIB module %s at %s' % (modName, self)
                )
        t = mibMod['typeToModIdx'].keys()[0]
        return mibMod['typeToModIdx'][t], t
        
    def getNextType(self, typeName, modName=''):
        m, t = self.getTypeName(typeName, modName)
        try:
            return self.__mibSymbolsIdx[m]['typeToModIdx'].nextKey(t)
        except KeyError:
            raise error.NoSuchInstanceError(
                str='No type next to %s::%s at %s' % (modName, typeName, self)
                )
