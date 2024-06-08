import asyncio

from telethon import TelegramClient, events
from telethon.tl.types import PeerUser
from loguru import logger

from phigros.phigros import Phigros
from config import get_config

conf = get_config()
client = TelegramClient(
    "tgPhiBot",
    conf.api_id,
    conf.api_hash,
    
    proxy=conf.proxy
).start(bot_token=conf.bot_token)

phigros = Phigros()

@client.on(event=events.NewMessage(pattern="/start"))
async def start(event: events.NewMessage.Event):
    event.respond("luohua's Phigros Telegram Bot.\n\n"
                  "Usage: \n"
                  "/phi bind <token> bind your phigros account to your telegram account\n"
                  "/b19 get your phigros b19 graph, bind your accounnt before use this function.")
    return

@client.on(event=events.NewMessage(pattern="/phi bind (.*)"))
async def bind_phigros_account(event):
    token = event.pattern_match.group(1)
    if not token:
        event.respond("Can not find token")
        return
    sender_id = event.from_id
    if not sender_id or not isinstance(sender_id, PeerUser):
        event.respond("Anonymous user is not supported.")
        return
    sender_id = sender_id.user_id
    conf.users[sender_id] = token
    event.respond(f"Successfully bind token: || {token} || \nNotice that this message does not means the token is valid.")
    
@client.on(event=events.NewMessage(pattern="/b19"))
async def get_b19(event):
    sender_id = event.from_id
    if not sender_id or not isinstance(sender_id, PeerUser):
        event.respond("Anonymous user is not supported.")
        return
    token: str = conf.users.get(sender_id)
    if not token:
        event.respond("Please bind your account first.")
        return
    file = await phigros.get_b19_img(token)
    event.respond("Developing...")
    

async def run():
    logger.info("TelegramPhigrosBot start running.")
    client.run_until_disconnected()
    logger.info("Bot is shuting down...")

if __name__ == "__main__":
    asyncio.run(run)