import logging

LOGGER = logging.getLogger('ffmpeg_watchdog')
LOGGER.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s:%(funcName)s: %(message)s')
f_handler = logging.FileHandler('ffmpeg_watchdog.log', mode='a', encoding='utf-8')
# s_handler = logging.StreamHandler()

# добавление форматировщика к обработчику
f_handler.setFormatter(formatter)
# s_handler.setFormatter(formatter)
# добавление обработчика к логгеру
LOGGER.addHandler(f_handler)
# LOGGER.addHandler(s_handler)
