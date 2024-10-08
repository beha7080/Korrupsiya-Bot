from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
IP = env.str("IP")
ADMINS = env.list("ADMINS")
WEB_APP_URL = env.str("WEB_APP_URL")