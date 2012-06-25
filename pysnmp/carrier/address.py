
# An abstract transport address object piggybacking additional address component

class TransportAddressPair:
    def __init__(self, localAddr, remoteAddr):
        self.__localAddr = localAddr
        self.__remoteAddr = remoteAddr

    def getLocalAddr(self): return self.__localAddr
    def getRemoteAddr(self): return self.__remoteAddr

    def __eq__(self, addr): return self.__remoteAddr == addr
    def __ne__(self, addr): return self.__remoteAddr != addr
    def __lt__(self, addr): return self.__remoteAddr < addr
    def __le__(self, addr): return self.__remoteAddr <= addr
    def __gt__(self, addr): return self.__remoteAddr > addr
    def __ge__(self, addr): return self.__remoteAddr >= addr

    def __getitem__(self, i): return self.__remoteAddr[i]

    def __hash__(self): return hash(self.__remoteAddr)

    def __str__(self): return str(self.__remoteAddr)
    def __repr__(self): return '%s(%r, %r)' % (
                            self.__class__.__name__, 
                            self.__localAddr,
                            self.__remoteAddr
                        )
