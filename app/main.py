import logging
import os

from telegram.ext import (CommandHandler, ConversationHandler, Filters,
                          MessageHandler, PicklePersistence, Updater)

import stages

logging.basicConfig(
    filename=os.getenv('BOT_LOG_FILE'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger('MAIN')
logger.setLevel(logging.DEBUG)



def main():

    logger.debug('Program start')

    try:
        persistance = PicklePersistence(os.getenv('BOT_PICKLE_PERSISTANCE'))
    except:
        persistance = None

    updater = Updater(token=os.getenv('BOT_TOKEN'),
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
