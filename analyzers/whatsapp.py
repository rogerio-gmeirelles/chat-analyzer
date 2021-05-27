import nltk
import datetime
import unidecode
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from emoji import UNICODE_EMOJI
from PIL import Image

# initial chat data
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

# variable which will store every word and message for the word cloud
messageSummary = ""

# split chat in messages
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

# creates word cloud based on messageSummary
def createWordCloud():
    # gera a wordcloud
    mask = np.array(Image.open("images/heart.png"))

    # remove words from cloud
    stopwords = set(STOPWORDS)
    nltk.download('stopwords')
    portugueseStopwords = nltk.corpus.stopwords.words('portuguese')
    stopwords.update(portugueseStopwords)
    stopwords.update([
        "da", "meu", "em", "de", "ao", "os", "que", "pra", "para", "e", "o", "a", "tb", "esse",
        "tambem", "ou", "um", "mas", "ja", "se", "dp", "ne", "por", "msm", "mesmo", "mim", "essa",
        "isso", "uma", "dai", "era", "dps", "porque", "pq", "kkk", "kkkkk", "kkkk", "kkkkkk", "vcs",
        "acho", "ele", "ela", "vc", "eu", "na", "tipo", "mt", "sim", "nao", "ah", "ahh", "ahhh",
        "pro", "ta", "entao", "ai", "tava", "pois", "outro", "outra", "coisa", "ficar", "ser", "la",
        "ainda", "ate", "meio", "faz", "pode", "tao", "deu", "iria", "coisas", "acha", "tanto",
        "menos", "pouco", "alguma", "sei", "sao", "achei", "simm", "dar", "ia", "fala", "hahah",
        "qnd", "algo", "toda", "quase", "haha", "deve", "hr"
    ])
    wordcloud = WordCloud(stopwords=stopwords, background_color="black", width=1000, height=1000, max_words=150,mask=mask, max_font_size=60,min_font_size=7).generate(messageSummary)

    # generates the final image
    fig, ax = plt.subplots(figsize=(10,10))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.set_axis_off()
    plt.imshow(wordcloud)
    wordcloud.to_file("wordcloud.png")

# proccess text messages and analyzes behaviour
def proccessMessage(line):
    splitLine = line.split(": ", 1)
    author = getAuthor(splitLine[0])
    message = splitLine[1]

    # counts how many messages by weekday
    proccessDateActivity(splitLine[0])

    # counts message for which ever author
    chatData["authors"][author]["messageCounter"] += 1

    # checks if message is a media or not
    if "<Media omitted>" in message:
        chatData["authors"][author]["mediaCounter"] += 1
    else:
        # adds message to be analyzed by the word cloud
        global messageSummary
        messageSummary += " " + unidecode.unidecode(message.lower())
        # counts how many words in message
        chatData["authors"][author]["wordCounter"] += len(message.split())
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

# removes less frequent or unecessary emojis
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
    createWordCloud()

    # prints resulting analyzed data
    print(chatData)
