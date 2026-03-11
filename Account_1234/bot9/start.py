
import asyncio
import random
import sys
import os
account_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(account_dir))
workspace_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) )
sys.path.append(workspace_root)
from telethon import TelegramClient, events
from should_send_message import should_send_message
from telethon.errors import FloodWaitError
from common.common_functions import load_target_groups, next_format, contains_keyword, send_message_safe, file_exists
parent = os.path.normpath(os.path.join(os.path.abspath(__file__), ".."))
workspace_root = os.path.dirname(parent)
groups_path = os.path.join(os.path.dirname(parent), "groups.txt")
try:
    from api import apiId, apiHash, sessionName, KEYWORDS, formats
    api_id = apiId()
    api_hash = apiHash()
    session_name = sessionName()
    FORMATS = formats()

except Exception as e:
    print(f"[WARNING] Failed to import from api.py: {e}")
    api_id = None
    api_hash = None
    session_name = None
    KEYWORDS = None
    FORMATS = []
TARGET_GROUPS = load_target_groups(groups_path, fromItem=120, toItem=135)
last_format_index = {}
active_groups = set()
client = TelegramClient(session_name, api_id, api_hash)
async def send_message_safe(chat_id, chat_title, group_link):
    try:
        last_msg = await client.get_messages(chat_id, limit=1)
        if last_msg and last_msg[0].out:
            last_sent_time = last_msg[0].date.timestamp()
            now = time.time()
            wait_time = max(0, 30 - (now - last_sent_time))
            if wait_time > 0:
                print(f"Waiting {int(wait_time)}s before sending again in {group_link}")
                await asyncio.sleep(wait_time)
            print(f"⏭ Skipped (already last): {group_link}")
            return
        msg = next_format(chat_id, last_format_index, FORMATS)
        await client.send_message(chat_id, msg)
        print(f"[OK] Sent in: {group_link}")
        await asyncio.sleep(random.randint(30, 45))
    except FloodWaitError as e:
        print(f"[WARNING] Skipped {group_link}: FloodWait {e.seconds}s - will retry on next trigger")
    except Exception as e:
        print(f"[ERROR] Error in {group_link}: {e}")
    finally:
        active_groups.discard(chat_id)
@client.on(events.NewMessage)
async def handler(event):
    if event.out:
        return
    if not event.is_group:
        return
    if not event.raw_text:
        return
    chat = await event.get_chat()
    if not getattr(chat, "username", None):
        return
    group_link = f"https://t.me/{chat.username}"
    if group_link not in TARGET_GROUPS:
        return
    text = event.raw_text.strip()
    length = len(text)
    has_keyword = contains_keyword(text, KEYWORDS)
    if not should_send_message(text, length, has_keyword):
        return
    gid = event.chat_id
    if gid in active_groups:
        print(f"[INFO] Already queued: {group_link}")
        return
    last_msg = await client.get_messages(gid, limit=1)
    if last_msg and last_msg[0].out:
        print(f"[INFO] Skipped (our last msg): {chat.title}")
        return
    active_groups.add(gid)
    asyncio.create_task(
        send_message_safe(gid, chat.title, group_link)
    )
async def main():
    print("=== Starting Bot Setup ===")
    if not TARGET_GROUPS or len(FORMATS) == 0:
        print("[ERROR] Failed to load target groups or formats. Exiting.")
        return
    print(f"[OK] Setup complete. Starting bot...")
    await client.start()
    me = await client.get_me()
    print(f"[INFO] Bot Account: {me.first_name}, Running (Selected Groups Only)")
    print("Loaded links:")
    for idx, link in enumerate(TARGET_GROUPS, 1):
        print(f"{idx}. {link}")
    print("Started Sending_ _ _ ________________________________")
            
    await client.run_until_disconnected()
asyncio.run(main())
