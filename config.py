import configparser


inifile = configparser.SafeConfigParser()
inifile.read('config.ini')
bot_setting = inifile['BOT_SETTING']

token = bot_setting['token']
guild_id = bot_setting['guild_id']
