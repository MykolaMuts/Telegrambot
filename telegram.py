import telebot
# import sqlite3
import logging
import database
import raspberry

# Set up the logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.info('Starting Bot...')


def logging_send(message):
    text = str(message.text).lower()
    logging.info(f'User ({message.chat.id}) says: {text}')


# conn = sqlite3.connect('memory_game.db')
# cursor = conn.cursor()

bot = telebot.TeleBot('5913408107:AAFYIWlvC2rODIALey1TZYbQoulFdpk0gRI')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Memory game')


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, '/create_table: to create a table \n'
                                      '/drop_table: to drop a table \n'
                                      '/add_user: To add new user \n'
                                      '/change_user_name: to change user name \n')


@bot.message_handler(commands=['create_table'])
def create_table(message):
    bot.send_message(message.chat.id, 'Creating table')
    database.create_table()
    bot.send_message(message.chat.id, 'Table created successfully.')

@bot.message_handler(commands=['drop_table'])
def drop_table(message):
    bot.send_message(message.chat.id, 'Dropping table')
    database.drop_table()
    bot.send_message(message.chat.id, 'Table drop successfully')


@bot.message_handler(commands=['add_user'])
def add_user(message):
    user_name = None
    password = None

    def get_user_name(message):
        nonlocal user_name
        user_name = message.text
        bot.send_message(message.chat.id, 'Create a password')
        bot.register_next_step_handler(message, get_password)

    def get_password(message):
        nonlocal password
        password = message.text
        add_user(message)

    def add_user(message):
        if database.add_user(user_name, password):
            bot.send_message(message.chat.id, 'User added successfully \n')
        else:
            bot.send_message(message.chat.id, 'User name is already taken')

    bot.send_message(message.chat.id, 'Create a user name')
    bot.register_next_step_handler(message, get_user_name)


@bot.message_handler(commands=['change_user_name'])
def change_user_name(message):
    user_name = None
    password = None
    new_user_name = None

    #####!!!!!
    def get_user_name(message):
        nonlocal user_name
        user_name = message.text
        bot.send_message(message.chat.id, 'Please type a password')
        bot.register_next_step_handler(message, get_password)

    def get_password(message):
        nonlocal password
        password = message.text
        bot.send_message(message.chat.id, 'Create a new name')
        bot.register_next_step_handler(message, get_new_user_name)

    def get_new_user_name(message):
        nonlocal new_user_name
        new_user_name = message.text
        update_scores(message)

    def update_scores(message):
        if database.change_user_name(user_name, password, new_user_name):
            bot.send_message(message.chat.id, 'User_name change successfully')
        else:
            bot.send_message(message.chat.id, 'User name or Password is wrong(')

    bot.send_message(message.chat.id, 'Please send the user name')
    bot.register_next_step_handler(message, get_user_name)


@bot.message_handler(commands=['increment_games'])
def increment(message):

    def increment(message):
        name = message.text
        if database.increment_games(name):
            bot.send_message(message.chat.id, 'Games incremented successfully')
        else:
            bot.send_message(message.chat.id, 'User name not found')

    bot.send_message(message.chat.id, 'Please send the user name')
    bot.register_next_step_handler(message, increment)




@bot.message_handler(commands=['update_scores'])
def update_scores(message):
    user_name = None
    score = None

    def get_user_name(message):
        nonlocal user_name
        user_name = message.text
        bot.send_message(message.chat.id, 'Please send the score')
        bot.register_next_step_handler(message, get_score)

    def get_score(message):
        nonlocal score
        score = int(message.text)
        update_scores(message)

    def update_scores(message):
        if database.update_score(user_name, score):
            bot.send_message(message.chat.id, 'Scores updated successfully')
        else:
            bot.send_message(message.chat.id, 'Something goes wrong(')

    bot.send_message(message.chat.id, 'Please send the user name')
    bot.register_next_step_handler(message, get_user_name)


@bot.message_handler(commands=['login'])
def login(message):
    user_name = None
    password = None

    def get_user_name(message):
        nonlocal user_name
        user_name = message.text
        bot.send_message(message.chat.id, 'Create a password')
        bot.register_next_step_handler(message, get_password)

    def get_password(message):
        nonlocal password
        password = message.text
        check(message)

    def check(message):
        if database.login(user_name, password):
            raspberry.login(user_name, password)
        else:
            database.add_user(user_name, password)
            bot.send_message(message.chat.id, 'Create a new user')

    bot.send_message(message.chat.id, 'Create a user name')
    bot.register_next_step_handler(message, get_user_name)



bot.polling()
