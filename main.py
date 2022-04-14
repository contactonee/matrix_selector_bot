import argparse
import logging

from telegram.ext import (CommandHandler, ConversationHandler, Filters,
                          MessageHandler, PicklePersistence, Updater)

import stages

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger('MAIN')
logger.setLevel(logging.DEBUG)


def parse_args():

    logger.debug('Parse args')

    parser = argparse.ArgumentParser()

    parser.add_argument('--token', action='store', required=True)

    args = parser.parse_args()

    return args


def main():

    logger.debug('Program start')

    args = parse_args()

    persistance = PicklePersistence('data.pkl')

    updater = Updater(token=args.token,
                      persistence=persistance,
                      use_context=True)

    updater.dispatcher.add_handler(
        ConversationHandler(
            name='create',
            entry_points=[
                CommandHandler('start', stages.start),
                CommandHandler('create', stages.prompt_create)],
            states={
                'CREATE_NAME': [
                    MessageHandler(Filters.text & ~Filters.command,
                                   stages.create_name)],
                'CREATE_VALUES': [
                    MessageHandler(Filters.text & ~Filters.command,
                                   stages.create_values)],
            },
            fallbacks=[
                CommandHandler('cancel', stages.force_idle)],
            persistent=True
        ))

    updater.dispatcher.add_handler(
        ConversationHandler(
            name='select',
            entry_points=[
                CommandHandler('select', stages.prompt_select)],
            states={
                'SELECT': [
                    MessageHandler(Filters.text & ~Filters.command,
                                   stages.set_config)
                ]
            },
            fallbacks=[
                CommandHandler('cancel', stages.force_idle)],
            persistent=True
        ))

    updater.dispatcher.add_handler(
        ConversationHandler(
            name='delete',
            entry_points=[
                CommandHandler('delete', stages.prompt_delete)],
            states={
                'DELETE': [
                    MessageHandler(Filters.text & ~Filters.command,
                                   stages.remove_config)
                ]
            },
            fallbacks=[
                CommandHandler('cancel', stages.force_idle)],
            persistent=True
        ))

    updater.dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command,
                       stages.calculate))

    updater.start_polling()
    logger.debug('Polling')


if __name__ == '__main__':
    main()
