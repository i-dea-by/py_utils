from loguru import logger
import winreg

FIND_STR = 'The Bat!'


def main():
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Clients\Mail', 0, winreg.KEY_ALL_ACCESS)
    except OSError as ex:
        logger.error(f"No admin rights! Error: {ex}")
    except Exception as ex:
        logger.error(f"Something else wrong! Error: {ex}")
    else:
        value = winreg.QueryValue(reg_key, None)
        if value != FIND_STR:
            winreg.SetValueEx(reg_key, None, 0, winreg.REG_SZ, FIND_STR)
            logger.info(f"Changed from '{value}' to '{FIND_STR}'")
        else:
            logger.info('OK')

        reg_key.Close()


if __name__ == '__main__':
    logger.add("the_bat.log", level='DEBUG')
    main()
