import telebot, sql_queries, os, dotenv
from flask import Flask, request
from config import config

def main():
    dotenv.load_dotenv()
    server = Flask(__name__)

    #specify which bot you want to use here: currently set to `telebot`
    bot_dict = config("db.ini", "telebot")
    #specify which webhook url you want to use here: currently set to `webhook_url`
    webhook_url = config("db.ini", "webhook_url")

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

    @server.route('/' + bot_dict['token'], methods=['POST'])
    def getMessage():
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "!", 200

    @server.route("/")
    def webhook():
        bot.remove_webhook()
        bot.set_webhook(url=webhook_url['webhook_url'] +bot_dict['token'])
        return "!", 200
    
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

if __name__ == "__main__":
    main()