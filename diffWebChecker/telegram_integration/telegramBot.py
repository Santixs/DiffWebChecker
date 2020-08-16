import telegram

def new_version(name, file):
    TOKEN = open("diffWebChecker/telegram_integration/token.txt", 'r').readline().strip()
    bot_chatID = open('diffWebChecker/telegram_integration/chatID.txt', 'r').readline().strip()
    bot = telegram.Bot(TOKEN)
    bot.sendMessage(bot_chatID, text=f"Hay una nueva actualización en la web {name}!")
    bot.sendDocument(bot_chatID, document=open(file, 'rb'))

