__author__ = 'User'

# Returns a stack where each element is of same format




def fragment_data(msg):

    # Define fragment types

    TEXT = "TEXT"
    EMOJI = "EMOJI"
    BREAK_IGNORE = [" ", "\n", "\r", "\t"]
    # find emojis
    emoji = False
    ignore = False
    msgLen = len(msg)
    fragBuffer = ""
    msgStack = []
    msgFragmentsTypes = []
    for i in range(0, msgLen):
        if i < msgLen-1 and msg[i] == "\\":
            ignore = True
            print "Saw \\, ignoring rest of word."
            continue
        if msg[i] in BREAK_IGNORE and ignore: #Should stop ignoring stuff now
            ignore = False
            print "Word ended, no longer ignoring."
        if emoji: # Check if currently expecting emoji chars
            if msg[i] == ":": # End of emoji
                msgStack.append(fragBuffer)
                msgFragmentsTypes.append(EMOJI)
                fragBuffer = ""
                emoji = False
            else:
                fragBuffer += msg[i]
        elif msg[i] == ":" and not ignore: # Beginning of emoji. Add check if \ later
            msgStack.append(fragBuffer)
            msgFragmentsTypes.append(TEXT)
            fragBuffer = ""
            emoji = True
        else: fragBuffer += msg[i]
    if fragBuffer != "":
        msgStack.append(fragBuffer)
        msgFragmentsTypes.append(TEXT)
    return (msgStack, msgFragmentsTypes)




def main():
    fragments, types = fragment_data("\\\Hello, World! \:lol:\n:xd:")

    print len(fragments)
    print len(types)

    for i in range(0, len(fragments)):

        print "%s (%s)\n" % (fragments[i], types[i])

if __name__ == "__main__":
    main()

