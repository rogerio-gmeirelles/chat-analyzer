import datetime
from emoji import UNICODE_EMOJI

chatData = {
    "authors": {},
    "weekdayActivity": {
        "Sunday": 0,
        "Monday": 0,
        "Tuesday": 0,
        "Wednesday": 0,
        "Thursday": 0,
        "Friday": 0,
        "Saturday": 0,
    }
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
            "loveCounter": 0,
            "beautyCounter": 0,
            "emojis": {}
        }
    return author

# Counts how many messages by weekday
def proccessDateActivity(messageData):
    date = messageData.split(" - ")[0]
    weekDay = datetime.datetime.strptime(date, "%Y/%m/%d, %H:%M:%S").strftime('%A')
    chatData["weekdayActivity"][weekDay] += 1

# proccess and counts every emoji
def proccessEmojis(author, message):
    for character in message:
        if character in UNICODE_EMOJI['en']:
            if character in chatData["authors"][author]["emojis"]:
                chatData["authors"][author]["emojis"][character] += 1
            else:
                chatData["authors"][author]["emojis"][character] = 1

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
        proccessDateActivity(splitLine[0])
        author = getAuthor(splitLine[0])
        chatData["authors"][author]["stickerCounter"] += 1
        return
    elif "ptt" in line:
        # audio file - count as 30sec readtime
        splitLine = line.split("ptt", 1)
        proccessDateActivity(splitLine[0])
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

    proccessDateActivity(splitLine[0])

    chatData["authors"][author]["messageCounter"] += 1

    if "<Media omitted>" in message:
        chatData["authors"][author]["mediaCounter"] += 1
    else:
        # counts how many words in message
        wordCount = len(message.split())
        chatData["authors"][author]["wordCounter"] += wordCount
        # checks for "bom dia", "buenos" and "boa tarde" variations in messages
        if "m di" in message or "buenos" in message or "oa ta" in message:
            chatData["authors"][author]["goodMorningCounter"] += 1
        # checks for love declarations
        if "te amo" in message or "meu amor" in message or "a amor" in message:
            chatData["authors"][author]["loveCounter"] += 1
        # checks for love declarations
        if ("linda" in message and author == "Rogério M.") or ("lindo" in message and author == "Gabriela Motta"):
            chatData["authors"][author]["beautyCounter"] += 1
        # looks for most used emojis
        proccessEmojis(author, message)

def clearsEmojiData():
    for author in chatData["authors"]:
        emojis = {}
        emojiDictionary = chatData["authors"][author]["emojis"]
        for emoji in emojiDictionary.keys():
            emojiCount = emojiDictionary[emoji]
            # only saves emojis used more than times by author and discards color and sex emojis
            if emojiCount > 30 and emoji != "🏻" and emoji != "♀" and emoji != "🏽" and emoji != "🏼" and emoji != "♂" and emoji != "☝":
                emojis[emoji] = emojiCount
        chatData["authors"][author]["emojis"] = emojis

# analyzes the entire whatsapp chat
def whatsappAnalyzer(chat):
    # read file line by line
    for line in splitLines(chat):
        if ": " in line:
            proccessMessage(line)
        else:
            proccessNonTextMessage(line)
    
    clearsEmojiData()

    # prints resulting analyzed data
    print(chatData)
