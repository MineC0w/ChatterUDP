class Client:
    def __init__(self, ip, port):
        self._ip = ip
        self._port = port
        self._chatHistory = ""
        self._unsavedChanges = ""
    def load_chat(self):
        # Load chat from file

        with open("chats/%s.txt" % self._ip, "a+") as log:
            for line in log:
                self._chatHistory += line
        log.close()

    def save_chat(self):
        # Save chat to file

        with open("chats/%s.txt" % self._ip, "a+") as log:
            log.write(self._unsavedChanges)
            log.close()
        self._unsavedChanges = ""

    def address(self):
        return (self._ip, int(self._port))

    def get_chat(self):
        return self._chatHistory

    def add_chat(self, data):
        self._chatHistory += data
        self._unsavedChanges += data





