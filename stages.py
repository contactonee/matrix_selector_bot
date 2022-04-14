import logging
from typing import DefaultDict

from telegram import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext, ConversationHandler

import utils

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def stage(func):
    def wrapper(update: Update, context: CallbackContext):
        logger.info('@' + update.effective_user.username
                    + (f' says: \"{update.message.text}\"'
                       if update.message is not None
                       else ''))
        logger.debug(context.chat_data)
        print(func)
        r = func(update, context)
        logger.debug(context.chat_data)
        return r
    return wrapper


@stage
def start(update: Update, context: CallbackContext):

    logger.debug(context.chat_data)

    # New user
    if 'configs' not in context.chat_data:

        context.chat_data['configs'] = {}

        update.message.reply_text(
            "Привет! Я могу считать наборы матриц для листогиба. Для начала создайте конфиг. Введите имя нового конфига")

        return 'CREATE_NAME'

    else:
        logger.info('%s already started the bot, skip intro',
                    update.effective_user.username)

        update.message.reply_text(
            "Привет! Я могу считать наборы матриц для листогиба.")
        return ConversationHandler.END


@stage
def prompt_create(update: Update, context: CallbackContext):

    update.message.reply_text("Введите имя нового конфига")

    return 'CREATE_NAME'


@stage
def create_name(update: Update, context: CallbackContext):

    context.chat_data['create_config_name'] = update.message.text

    update.message.reply_text(
        "Отличное название! Теперь введите список доступных матриц через запятую")

    return 'CREATE_VALUES'


@stage
def create_values(update: Update, context: CallbackContext):

    values = utils.parse_matrices_values(update.message.text)
    name = context.chat_data.pop('create_config_name')

    context.chat_data['configs'][name] = values
    context.chat_data['active_config'] = name

    logger.debug(context.chat_data)

    update.message.reply_text(
        "Конфиг сохранен! Теперь будет использоваться данный конфиг. Можете вводить желаемый гиб")

    return ConversationHandler.END


@stage
def calculate(update: Update, context: CallbackContext):

    values = context.chat_data['configs'][context.chat_data['active_config']]
    target = int(update.message.text)

    selected, result = utils.knapsack(sorted(values, reverse=True), target)

    update.message.reply_text(f'Доступные матрицы: {values}\n'
                              f'Выбор: {selected}\n'
                              f'Результат: {result}')


@stage
def prompt_select(update: Update, context: CallbackContext):

    names = list(context.chat_data['configs'].keys())

    keyboard = ReplyKeyboardMarkup.from_column(
        names,
        resize_keyboard=True)

    update.message.reply_text("Выберит конфиг", reply_markup=keyboard)

    return 'SELECT'


@stage
def set_config(update: Update, context: CallbackContext):

    context.chat_data['active_config'] = update.message.text

    update.message.reply_text(f'Успешно выбран конфиг {update.message.text}',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


@stage
def prompt_delete(update: Update, context: CallbackContext):

    names = list(context.chat_data['configs'].keys())

    keyboard = ReplyKeyboardMarkup.from_column(
        names,
        resize_keyboard=True)

    update.message.reply_text("Выберит конфиг который хотите удалить",
                              reply_markup=keyboard)

    return 'DELETE'


@stage
def remove_config(update: Update, context: CallbackContext):

    context.chat_data['configs'].pop(update.message.text)

    if context.chat_data['active_config'] == update.message.text:
        context.chat_data['active_config'] = list(
            context.chat_data['configs'].keys())[0]

    update.message.reply_text(f'Конфиг {update.message.text} удален',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


@stage
def force_idle(update: Update, context: CallbackContext):

    update.message.reply_text('Отмена', reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END
