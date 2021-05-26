chatData = {}


def splitLines(chat):
    splitChat = []
    currentLine = ""

    # iterate through every character
    for idx, character in enumerate(chat[:-1]):
        if (character == "\n"):
            # if next line starts with "20", assumes it's a new message
            if chat[idx + 1] == "2" and chat[idx + 2] == "0":
                splitChat.append(currentLine)
                currentLine = ""
            else:
                currentLine += " "
        else:
            currentLine += character

    return splitChat

def proccessAudio(line):
    # alwats ends with "ptt"
    # count auduo as 30sec readtime
    # count audio as 1 msg from person and as 1 audio
    print(line)

def proccessMessage(line):
    splitLine = line.split(": ", 1)
    autor = splitLine[0].split(" - ", 1)[1]
    message = splitLine[1]
    print(autor + "|||" + message)

def whatsappAnalyzer(chat):
    # read file line by line
    for line in splitLines(chat):
        if ": " in line:
            proccessMessage(line)
        else:
            proccessAudio(line)
    print(chatData)
