from ctypes import resize
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, ReplyMarkup,
                      Update, CallbackQuery)
from telegram.ext import CallbackContext

import utils


def start(update: Update, context: CallbackContext):

    msg: Message = update.message
    update.message.reply_text(
        "Привет! Я могу считать наборы матриц для листогиба. Давай создадим наш первый конфиг файл. Введите имя конфиг файла")
    context.chat_data['configs'] = {}

    return prompt_create(update, context)


def prompt_create(update: Update, context: CallbackContext):

    msg: Message = update.message
    msg.reply_text("Введите имя конфига")

    return 'CREATE_NAME'


def create_name(update: Update, context: CallbackContext):

    msg: Message = update.message

    context.chat_data['create_config_name'] = msg.text

    msg.reply_text(
        "Отличное название! Теперь введите список доступных матриц через запятую")

    return 'CREATE_VALUES'


def create_values(update: Update, context: CallbackContext):

    msg: Message = update.message

    values = utils.parse_matrices_values(msg.text)
    name = context.chat_data['create_config_name']

    context.chat_data['configs'][name] = values
    context.chat_data['active_config'] = name

    update.message.reply_text(
        "Конфиг сохранен! Теперь будет использоваться данный конфиг. Можете вводить желаемый гиб")

    return 'IDLE'


def calculate(update: Update, context: CallbackContext):
    msg: Message = update.message

    values = context.chat_data['configs'][context.chat_data['active_config']]
    target = int(msg.text)

    selected, result = utils.knapsack(sorted(values, reverse=True), target)

    msg.reply_text(f'Доступные матрицы: {values}\n'
                   f'Выбор: {selected}\n'
                   f'Результат: {result}')


def prompt_select(update: Update, context: CallbackContext):

    msg: Message = update.message

    names = list(context.chat_data['configs'].keys())

    keyboard = ReplyKeyboardMarkup.from_column(
        names,
        resize_keyboard=True)

    msg.reply_text("Выберит конфиг", reply_markup=keyboard)

    return 'SELECT'


def set_config(update: Update, context: CallbackContext):

    msg: Message = update.message

    context.chat_data['active_config'] = msg.text

    msg.reply_text(f'Успешно выбран конфиг {msg.text}')

    return 'IDLE'


def prompt_delete(update: Update, context: CallbackContext):

    msg: Message = update.message

    names = list(context.chat_data['configs'].keys())

    keyboard = ReplyKeyboardMarkup.from_column(
        names,
        resize_keyboard=True)

    msg.reply_text("Выберит конфиг который хотите удалить",
                   reply_markup=keyboard)

    return 'DELETE'


def remove_config(update: Update, context: CallbackContext):

    msg: Message = update.message

    context.chat_data['configs'].pop(msg.text)

    if context.chat_data['active_config'] == msg.text:
        context.chat_data['active_config'] = list(
            context.chat_data['configs'].keys())[0]

    msg.reply_text(f'Конфиг {msg.text} удален')

    return 'IDLE'


def force_idle(update: Update, context: CallbackContext):
    return 'IDLE'
