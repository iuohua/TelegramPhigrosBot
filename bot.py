import asyncio
from typing import Optional

from telethon import TelegramClient, events
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
from telethon.functions import messages
from loguru import logger

from phigros.phigros import Phigros
from phigros.gameInfo import update_difficulty
from config import get_config, save_config
from model import CustomMarkdown

conf = get_config()
client = TelegramClient(
    "tgPhiBot",
    conf.api_id,
    conf.api_hash,
    
    proxy=conf.proxy
).start(bot_token=conf.bot_token)
client.parse_mode = CustomMarkdown()

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
                  "/phi bind <token> bind your phigros account to your telegram account. (DO NOT bind your account in a public group)\n"
                  "/b19 get your phigros b19 graph, bind your accounnt before use this function. (gugugu...)\n"
                  "/b19_text get your phigros b19 data, text version.\n"
                  "Author: @luohua If you can help with B19 graph generation, please contact me (or directly PR)\n\n"
                  "Open source on https://github.com/iuohua/TelegramPhigrosBot with AGPL License")
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
    await event.respond(f"Successfully bind token: [{token}](spoiler) \nNotice that this message does not means the token is valid.")
    
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
    await event.respond("B19 graph is not support. Please use /b19_text.")

@client.on(event=events.NewMessage(pattern="^/b19_text(@PhigrosB19Bot)? *$"))
async def get_b19_text(event):
    sender_id = get_id(event.from_id, event.peer_id)
    sender = await event.get_sender()
    logger.info(f"Trying to get b19_text for {sender.username}({sender_id})")
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
    if not sender_id or sender_id != conf.owner:
        return
    file_message = event.reply_to
    # logger.debug(file_message)
    if not file_message:
        await event.respond("Please reply to a file")
        return
    reply_id = file_message.reply_to_msg_id
    if not reply_id:
        await event.respond("Please reply to a file")
        return
    reply = await client.get_messages(await event.get_chat(), ids=reply_id)
    if not reply.media:
        await event.respond("Please reply to a file")
        return
    logger.info("Downloading file...")
    await event.respond("Downloading...")
    await client.download_media(reply.media, "update.apk")
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