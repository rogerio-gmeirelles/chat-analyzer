from analyzers.whatsapp import whatsappAnalyzer

whatsappChats = ["chats/whatsapp/whats_gabi.txt"]

for whatsChat in whatsappChats:
    file = open(whatsChat, "r")
    whatsappAnalyzer(file.read())
    file.close()
