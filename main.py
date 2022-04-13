import argparse

from telegram.ext import (CommandHandler, ConversationHandler, Filters,
                          MessageHandler, Updater, PicklePersistence)

import stages


def parse_args():

    parser = argparse.ArgumentParser()

    parser.add_argument('--token', action='store', required=True)

    args = parser.parse_args()

    return args


def main():

    main_conversation = ConversationHandler(
        entry_points=[
            CommandHandler('start', stages.start)],
        states={
            'CREATE_NAME': [
                MessageHandler(Filters.text, stages.create_name)],
            'CREATE_VALUES': [
                MessageHandler(Filters.text, stages.create_values)],
            'IDLE': [
                CommandHandler('select', stages.prompt_select),
                CommandHandler('delete', stages.prompt_delete),
                CommandHandler('create', stages.prompt_create),
                MessageHandler(Filters.text, stages.calculate)],
            'SELECT': [
                MessageHandler(Filters.text, stages.set_config)
            ],
            'DELETE': [
                MessageHandler(Filters.text, stages.remove_config)
            ],
        },
        fallbacks=[
            CommandHandler('cancel', stages.force_idle)]
    )

    args = parse_args()

    persistance = PicklePersistence('data.pkl')

    updater = Updater(args.token,
                      persistence=persistance,
                      use_context=True)

    updater.dispatcher.add_handler(main_conversation)

    updater.start_polling()
    print('Polling')


if __name__ == '__main__':
    main()
