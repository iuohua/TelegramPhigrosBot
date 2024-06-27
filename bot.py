import asyncio
from typing import Optional

from telethon import TelegramClient, events
from telethon.tl.types import PeerUser
from loguru import logger

from phigros.phigros import Phigros
from phigros.gameInfo import update_difficulty
from config import get_config

conf = get_config()
client = TelegramClient(
    "tgPhiBot",
    conf.api_id,
    conf.api_hash,
    
    proxy=conf.proxy
).start(bot_token=conf.bot_token)

phigros = Phigros()

def get_token(event, sender_id: Optional[int]) -> str:
    if not sender_id or not isinstance(sender_id, PeerUser):
        event.respond("Anonymous user is not supported.")
        return
    token: Optional[str] = conf.users.get(sender_id)
    if not token:
        event.respond("Please bind your account first.")
        return
    return token
    
def get_id(sender_id) -> Optional[int]:
   if isinstance(sender_id, int):
       return sender_id
   if isinstance(sender_id, PeerUser):
       return sender_id.user_id
   return None 

@client.on(event=events.NewMessage(pattern="/start"))
async def start(event: events.NewMessage.Event):
    event.respond("luohua's Phigros B19 Telegram Bot.\n\n"
                  "Usage: \n"
                  "/phi bind <token> bind your phigros account to your telegram account\n"
                  "/b19 get your phigros b19 graph, bind your accounnt before use this function. (gugugu...)\n"
                  "/b19_text get your phigros b19 data, text version.\n"
                  "Author: @luohua If you can help with B19 graph generate, please contact (or directly PR)"
                  "Opensouce on https://github.com/iuohua/TelegramPhigrosBot with AGPT L")
    return

@client.on(event=events.NewMessage(pattern="/phi bind (.*)"))
async def bind_phigros_account(event):
    token = event.pattern_match.group(1)
    if not token:
        event.respond("Can not find token")
        return
    sender_id = get_id(event.from_id)
    if not sender_id:
        event.respond("Anonymous user is not supported.")
        return
    sender_id = sender_id.user_id
    conf.users[sender_id] = token
    event.respond(f"Successfully bind token: || {token} || \nNotice that this message does not means the token is valid.")
    
@client.on(event=events.NewMessage(pattern="/b19"))
async def get_b19_graph(event):
    sender_id = get_id(event.from_id)
    if not sender_id:
        event.respond("Anonymous user is not supported.")
        return
    token = get_token(event, sender_id)
    if not token:
        return
    # file = await phigros.get_b19_img(token)
    event.respond("")

@client.on(event=events.NewMessage(pattern="/b19_text"))
async def get_b19_text(event):
    sender_id = get_id(event.from_id)
    if not sender_id:
        event.respond("Anonymous user is not supported.")
        return
    token = get_token(event, sender_id)
    if not token:
        return
    message = await phigros.get_b19_info(token)
    logger.debug(message)
    event.respond(message)
    
@client.on(event=events.NewMessage(pattern="/update"))
async def update_diff(event):
    sender_id = get_id(event.from_id)
    if not sender_id or sender_id != conf.get("owner"):
        return
    file_message = event.reply_to
    if not file_message:
        event.respond("Please reply to a file")
    media = file_message.reply_media
    if not media:
        event.respond("Please reply to a file")
    logger.info("Downloading file...")
    await client.download_media(media, "update.apk")
    logger.info("Download complete, update difficulty")
    update_difficulty("update.apk")
    event.respond("Difficulty table updated.")

async def run():
    logger.info("TelegramPhigrosBot start running.")
    client.run_until_disconnected()
    logger.info("Bot is shuting down...")
    

if __name__ == "__main__":
    asyncio.run(run)