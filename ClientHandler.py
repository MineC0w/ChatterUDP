class Client():
    def __init__(self, ip, port):
        self._ip = ip
        self._port = port
        self._chatHistory = ""

    def LoadChat(self):
        # Load chat from file
        pass

    def SaveChat(self):
        # Save chat to file
        pass
    def getSendAdd(self):
        return (self._ip, int(self._port))

    def getChat(self):
        return self._chatHistory

    def addChat(self, data):
        self._chatHistory += data




