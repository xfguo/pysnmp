# MIB tree foundation class

moduleID = 'PYSNMP_MODULE_ID'

class MibNode:
    label = ''
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.name)

    def getName(self): return self.name
    
    def getLabel(self): return self.label
    def setLabel(self, label):
        self.label = label
        return self

    def clone(self, name=None):
        myClone = self.__class__(self.name)
        if name is not None:
            myClone.name = name
        if self.label is not None:
            myClone.label = self.label
        return myClone
