chatData = {
    "authors": {}
}

def splitLines(chat):
    splitChat = []
    currentLine = ""

    # iterate through every character
    for idx, character in enumerate(chat[:-1]):
        if (character == "\n"):
            # assumes it's a new message if next line starts with "****/**/**,"
            if chat[idx + 5] == "/" and chat[idx + 8] == "/" and chat[idx + 11] == ",":
                splitChat.append(currentLine)
                currentLine = ""
            else:
                currentLine += " "
        else:
            currentLine += character

    return splitChat

# gets authour of message and creates initial state if necessary
def getAuthor(messageData):
    author = messageData.split(" - ", 1)[1]
    if not author in chatData["authors"]:
        chatData["authors"][author] = {
            "audioCounter": 0,
            "mediaCounter": 0,
            "messageCounter": 0,
            "wordCounter": 0,
            "goodMorningCounter": 0,
            "stickerCounter": 0,
        }
    return author

# proccess non text messages and analyzes behaviour
def proccessNonTextMessage(line):
    if "this message has been deleted" in line:
        return
    elif "missed video call" in line or "missed voice call" in line:
        return
    elif "document" in line:
        # document attachment
        return
    elif "vcard" in line:
        # contact card
        return
    elif "sticker" in line:
        splitLine = line.split("sticker", 1)
        author = getAuthor(splitLine[0])
        chatData["authors"][author]["stickerCounter"] += 1
        return
    elif "ptt" in line:
        # audio file - count as 30sec readtime
        splitLine = line.split("ptt", 1)
        author = getAuthor(splitLine[0])
        chatData["authors"][author]["audioCounter"] += 1
        return
    # ignores unforseen scenarios, uncomment the print line if you would like to investigate
    # "missed group voice call" falls here
    # print(line)
    return

# proccess text messages and analyzes behaviour
def proccessMessage(line):
    splitLine = line.split(": ", 1)
    author = getAuthor(splitLine[0])
    message = splitLine[1]

    chatData["authors"][author]["messageCounter"] += 1
    if "m di" in message or "buenos" in message or "oa ta" in message:
        chatData["authors"][author]["goodMorningCounter"] += 1

# analyzes the entire whatsapp chat
def whatsappAnalyzer(chat):
    # read file line by line
    for line in splitLines(chat):
        if ": " in line:
            proccessMessage(line)
        else:
            proccessNonTextMessage(line)

    # prints resulting analyzed data
    print(chatData)
