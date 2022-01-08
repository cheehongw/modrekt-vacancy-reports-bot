import telebot, sql_queries
from config import config

def main():
    bot_dict = config("db.ini", "telebot")
    bot = telebot.TeleBot(bot_dict['token'], parse_mode=bot_dict['parse_mode'])

    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        bot.send_message(message.chat.id, """This bot will get the latest module vacancies for any given module code!
Please reply to this bot with the following valid formats:
module_code
module_code number_of_rounds""")


    @bot.message_handler(func=lambda message: True)
    def get_module_information(message):
        user_message = message.text.upper()
        arguments = user_message.split()
        arg_len = len(arguments)

        return_msg = ''

        if (arg_len == 1):
            return_msg = sql_queries.handle_message(arguments[0])
        elif (arg_len == 2):
            try:
                number_of_rounds = int(arguments[1])
                return_msg = sql_queries.handle_message(arguments[0], arguments[1])
            except:
                return_msg = 'Please use a number for the second argument.'
        else:
            return_msg = 'Please follow the expected format.'

        bot.reply_to(message, return_msg)

    bot.infinity_polling()

if __name__ == "__main__":
    main()