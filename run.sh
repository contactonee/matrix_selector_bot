docker run \
--rm \
--volume matrix_selector_bot:/usr/src/app/data \
--env BOT_PICKLE_PERSISTANCE=data/data.pkl \
--env BOT_LOG_FILE=data/bot.log \
--env BOT_TOKEN=${TELEGRAM_BOT_TOKEN} \
$(docker build -q .) &