from email.message import Message
import json
from ast import Call
from typing import List, Tuple
import stages
import argparse

import numpy as np
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (CallbackContext, CommandHandler, ConversationHandler,
                          Filters, MessageHandler, Updater, CallbackQueryHandler)


def knapsack(w: List[int],
             W: int) -> Tuple[List[int], int]:

    n = len(w)

    res = np.zeros((n + 1, W + 1), np.int32)

    for i in range(1, n + 1):
        for j in range(W + 1):
            if w[i - 1] > j:
                res[i][j] = res[i - 1][j]
            else:
                res[i][j] = max(res[i - 1, j],
                                res[i - 1, j - w[i-1]] + w[i-1])

    return restore_knapsack(w, res), res[-1, -1]


def restore_knapsack(w: List[int],
                     res: np.ndarray) -> List[int]:

    if res[-1, -1] == 0:
        return []
    if res[-1, -1] == res[-2, -1]:
        return restore_knapsack(w, res[:-1])
    else:
        it = w[res.shape[0] - 2]
        return [*restore_knapsack(w, res[:-1, :res[-1, -1] - it + 1]), it]


def parse_args():

    parser = argparse.ArgumentParser()

    parser.add_argument('--token', action='store', required=True)

    args = parser.parse_args()

    return args


def cmd_start(update: Update, context: CallbackContext):

    if 'configs' not in context.chat_data:
        update.message.reply_text(
            'Для начала работы создайте конфиг при помощи команды /edit_config')


def cmd_config(update: Update, context: CallbackContext):

    # update.message.reply_text('Команда для выбора конфига')
    # update.message.reply_text('Выберите конфиг', reply_markup=)

    return 'SELECT'


def cmd_edit_config(update: Update, context: CallbackContext):

    update.message.reply_text('Команда для редактирования конфигов')

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton('Создать', callback_data='new'),
          InlineKeyboardButton('Изменить', callback_data='edit'),
          InlineKeyboardButton('Удалить', callback_data='remove')]])

    update.message.reply_text('*Конфигуратор*\n'
                              'Выберите действие',
                              parse_mode='MarkdownV2',
                              reply_markup=keyboard)


def solve(update: Update, context: CallbackContext):

    # update.effective_message
    pass


def create_config(update: Update, context: CallbackContext):
    breakpoint()


def main():

    # main_conversation = ConversationHandler(
    #     entry_points=[CommandHandler('start', stages.start)],
    #     stages={
    #         CREATE: [MessageHandler(Filters.text, stages.create_config)],
    #         IDLE: [CommandHandler('select_config', stages.prompt_select_config),
    #                CommandHandler('edit_config', stages.prompt_editor),
    #                MessageHandler(Filters.text), stages.calculate],
    #         SELECT: [CallbackQueryHandler(stages.set_config,
    #                                       pattern='sel_config_*')],
    #         EDITOR: [CallbackQueryHandler(stages.prompt_edit_config,
    #                                       pattern='edit_select'),
    #                  CallbackQueryHandler(stages.prompt_remove_config,
    #                                       pattern='remove_select'),
    #                  CallbackQueryHandler(stages.create_config,
    #                                       pattern='create_config')],
    #         EDIT: [CallbackQueryHandler(stages.prompt_select_edit_config,
    #                                     pattern='edit_config_*')],
    #     }
    # )

    main_conversation = ConversationHandler(
        entry_points=[CommandHandler('start', stages.start)],
        states={
            'CREATE_CONFIG_NAME': [MessageHandler(Filters.text, stages.create_config_name)],
            'CREATE_CONFIG_VALUES': [MessageHandler(Filters.text, stages.create_config_values)],
            'IDLE': [CommandHandler('config', stages.prompt_select_config),
                     MessageHandler(Filters.text, stages.calculate)],
            'SELECT': [CallbackQueryHandler(stages.set_config)]
        },
        fallbacks=[]
    )

    args = parse_args()

    updater = Updater(args.token, use_context=True)

    updater.dispatcher.add_handler(main_conversation)

    updater.start_polling()


if __name__ == '__main__':
    main()
