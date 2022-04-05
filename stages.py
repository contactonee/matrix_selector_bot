from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, Message,
                      Update, CallbackQuery)
from telegram.ext import CallbackContext

from main import knapsack


def start(update: Update, context: CallbackContext):

    update.message.reply_text('Привет! Я могу считать наборы матриц для '
                              'листогиба. Давай создадим наш первый конфиг '
                              'файл. Введите имя конфиг файла')

    context.chat_data['configs'] = {}

    return 'CREATE_CONFIG_NAME'


def create_config_name(update: Update, context: CallbackContext):

    name = update.message.text

    context.chat_data['create_config_name'] = name

    update.message.reply_text('Отличное название! Теперь введите список '
                              'доступных матриц через запятую')

    return 'CREATE_CONFIG_VALUES'


def create_config_values(update: Update, context: CallbackContext):

    values: str = update.message.text

    values = values.strip(' \t\n').split(',')

    values = list(map(int, map(str.strip, values)))

    name = context.chat_data['create_config_name']

    context.chat_data['configs'][name] = values
    context.chat_data['active_config'] = name

    update.message.reply_text('Конфиг сохранен! Теперь будет использоваться '
                              'данный конфиг. Можете вводить желаемый гиб')

    return 'IDLE'


def prompt_select_config(update: Update, context: CallbackContext):

    msg: Message = update.message

    names = list(context.chat_data['configs'].keys())

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(k, callback_data=k)
            for k in names[z:z+3]
        ]
        for z in range(0, len(names), 3)
    ])

    msg.reply_text('Выберит конфиг', reply_markup=keyboard)

    return 'SELECT'


def set_config(update: Update, context: CallbackContext):

    query: CallbackQuery = update.callback_query

    context.chat_data['active_config'] = query.data

    query.edit_message_text(f'Успешно выбран конфиг {query.data}')

    return 'IDLE'


def calculate(update: Update, context: CallbackContext):
    msg: Message = update.message

    values = context.chat_data['configs'][context.chat_data['active_config']]
    target = int(msg.text)

    selected, result = knapsack(sorted(values, reverse=True), target)

    msg.reply_text(f'Available matrices: {values}\n'
                   f'Selected set: {selected}\n'
                   f'Result: {result}')
