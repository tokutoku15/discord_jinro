from JinroBot import JinroBot

f = open('.env','r', encoding='UTF-8')
env = f.read().split('\n')
ACCESS_TOKEN = env[0]
GUILD_ID = int(env[1])
TEXT_CHANNEL_ID = int(env[2])
VOICE_CHANNEL_ID = int(env[3])
f.close()

bot = JinroBot(GUILD_ID, TEXT_CHANNEL_ID, VOICE_CHANNEL_ID)
bot.run(ACCESS_TOKEN)