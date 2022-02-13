import configparser
import os

def setting_get(setting: configparser.SectionProxy,name:str,default = ''):
    val = setting.get(name)
    if(val == None or val == ''):
        print(f"{name}が設定されてません。")
        val = str(default)
        setting[name] = val
        setting_get.is_none = True
    return val 


filename = 'config.ini'
inifile = configparser.SafeConfigParser()
if(not os.path.isfile(filename)):
    print("設定ファイルが存在しません。")
    inifile['BOT_SETTING'] = {}
else: inifile.read(filename)

setting_get.is_none = False
bot_setting = inifile['BOT_SETTING']
token = setting_get(bot_setting, 'token')
guild_id = int(setting_get(bot_setting, 'guild_id'))
text_ch_id = int(setting_get(bot_setting, 'text_ch_id'))
list_limit = int(setting_get(bot_setting, 'list_limit', 10))

if(setting_get.is_none):
    with open(filename, 'w') as file:
        inifile.write(file)
    print("終了します")
    exit()
def reload():
    guild_id = int(setting_get(bot_setting, 'guild_id'))
    text_ch_id = int(setting_get(bot_setting, 'text_ch_id'))
    list_limit = int(setting_get(bot_setting, 'list_limit', 10))
