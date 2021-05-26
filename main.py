from analyzers.whatsapp import whatsappAnalyzer

whatsappChats = ["chats/whats_gabi_ate_20_maio.txt"]

for whatsChat in whatsappChats:
    file = open(whatsChat, "r")
    whatsappAnalyzer(file.read())
    file.close()
