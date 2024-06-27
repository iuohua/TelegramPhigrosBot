import asyncio
from typing import Optional

from telethon import TelegramClient, events
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
from loguru import logger

from phigros.phigros import Phigros
from phigros.gameInfo import update_difficulty
from config import get_config, save_config

conf = get_config()
client = TelegramClient(
    "tgPhiBot",
    conf.api_id,
    conf.api_hash,
    
    proxy=conf.proxy
).start(bot_token=conf.bot_token)

phigros = Phigros()

async def get_token(event, sender_id: Optional[int]) -> str:
    if not sender_id:
        await event.respond("Anonymous user is not supported.")
        return
    token: Optional[str] = conf.users.get(sender_id)
    if not token:
        await event.respond("Please bind your account first.")
        return
    return token
    
def get_id(from_id, peer_id) -> Optional[int]:
   if isinstance(from_id, int):
       return from_id
   if isinstance(from_id, PeerUser):
       return from_id.user_id
   if not from_id and isinstance(peer_id, PeerUser):
       return peer_id.user_id
   return None

@client.on(event=events.NewMessage(pattern="/start"))
async def start(event: events.NewMessage.Event):
    await event.respond("luohua's Phigros B19 Telegram Bot.\n\n"
                  "Usage: \n"
                  "/phi bind <token> bind your phigros account to your telegram account\n"
                  "/b19 get your phigros b19 graph, bind your accounnt before use this function. (gugugu...)\n"
                  "/b19_text get your phigros b19 data, text version.\n"
                  "Author: @luohua If you can help with B19 graph generate, please contact (or directly PR)\n\n"
                  "Open source on https://github.com/iuohua/TelegramPhigrosBot with AGPT License")
    return

@client.on(event=events.NewMessage(pattern="^/phi bind (.*?)$"))
async def bind_phigros_account(event):
    token = event.pattern_match.group(1)
    if not token:
        await event.respond("Can not find token")
        return
    sender_id = get_id(event.from_id, event.peer_id)
    if not sender_id:
        await event.respond("Anonymous user is not supported.")
        return
    conf.users[sender_id] = token
    await event.respond(f"Successfully bind token: || {token} || \nNotice that this message does not means the token is valid.", parse_mode="md")
    
@client.on(event=events.NewMessage(pattern="^/b19(@PhigrosB19Bot)? *$"))
async def get_b19_graph(event):
    sender_id = get_id(event.from_id, event.peer_id)
    if not sender_id:
        await event.respond("Anonymous user is not supported.")
        return
    token = await get_token(event, sender_id)
    if not token:
        return
    # file = await phigros.get_b19_img(token)
    await event.respond("")

@client.on(event=events.NewMessage(pattern="^/b19_text(@PhigrosB19Bot)? *$"))
async def get_b19_text(event):
    sender_id = get_id(event.from_id, event.peer_id)
    if not sender_id:
        logger.debug("check")
        await event.respond("Anonymous user is not supported.")
        return
    token = await get_token(event, sender_id)
    if not token:
        return
    message = await phigros.get_b19_info(token)
    # logger.debug(message)
    await event.respond(message)
    
@client.on(event=events.NewMessage(pattern="/update"))
async def update_diff(event):
    sender_id = get_id(event.from_id, event.peer_id)
    if not sender_id or sender_id != conf.get("owner"):
        return
    file_message = event.reply_to
    if not file_message:
        await event.respond("Please reply to a file")
    media = file_message.reply_media
    if not media:
        await event.respond("Please reply to a file")
    logger.info("Downloading file...")
    await client.download_media(media, "update.apk")
    logger.info("Download complete, update difficulty")
    update_difficulty("update.apk")
    await event.respond("Difficulty table updated.")

if __name__ == "__main__":
    logger.info("TelegramPhigrosBot start running.")
    try:
        asyncio.run(client.run_until_disconnected())
    finally:
        logger.info("Bot is shuting down...")
        save_config(conf)