import asyncio
import random
from telethon import TelegramClient, events
# ================= TELEGRAM API =================

def apiId(id):
    return id or 36591536
# api_id = 36521355
def apiHash(hash):
    return hash or "fb331e311d3e1814c9bc99e7b80f5034"
# api_hash = "e0afd99ef6508faddc6289aeca903150"
def sessionName(name):
    return name or "auto_send_session"
# session_name = "auto_send_session"

def phoneNumber(num):
    return num or "+919668194139"

# ================= KEYWORDS =================
KEYWORDS = [
    "proxy support",
    "interview support",
    "interview",
    "interview help",
    "support available",
    "proxy",
    "assessment",
    "exam",
    "test"
]

# ================= Send FORMATS =================
FORMAT_1 = """_._._._._._._._._._._._
Interview Support 
°°°°°°°°°°°°°°°°°°°°

For all technologies, including:
📍Salesforce📍Java📍Java Full Stack📍C, C++📍Spring Boot Microservices📍Spring Hibernate📍Dot Net / .NET📍SAP📍Data Science📍AWS Admin📍AWS DevOps📍Azure Admin📍Azure Data Engineer📍Data Engineering📍Azure DevOps📍Selenium 📍Manual Testing📍Automation Testing📍Python📍Python Full Stack📍SQL📍Power BI📍REST API📍Django📍Big Data📍React JS & Node.js📍MongoDB📍Oracle📍Data Analyst📍BA📍ETL📍DevOps📍React Angular📍QA📍Azure📍Dot Net📍PL/SQL📍 Networking📍ServiceNow📍AI/ML

We provide support using advanced tools which are:
🔹 100% invisible in Task Manager
🔹 100% invisible on screen share
🔹 100% on spot answers
🔹 100% safe and secured

For: INDIA, USA, UK, Canada, Aust
(IST/CST/PST/EST time zones)

WhatsApp me for more details....
+91 98850 74380"""

FORMAT_2 = """_._._._._._._._._._._._._._._._

Interview Support  

For all technologies, including:
Salesforce, Java, Java Full Stack, C, C++, Spring Boot Microservices, Spring Hibernate, Dot Net / .NET, SAP, Data Science, AWS Admin, AWS DevOps, Azure Admin, Azure Data Engineer, Data Engineering, Azure DevOps, Selenium , Manual Testing, Automation Testing, Python, Python Full Stack, SQL, Power BI, REST API, Django, Big Data, React JS & Node.js, MongoDB, Oracle, Data Analyst, BA, ETL, DevOps, React Angular, QA, Azure, Dot Net, PL/SQL,  Networking, ServiceNow, AI/ML

We provide support using advanced tools which are:
🔹 100% invisible in Task Manager
🔹 100% invisible on screen share
🔹 100% on spot answers
🔹 100% safe and secured

For: INDIA, USA, UK, Canada, Aust
(IST/CST/PST/EST time zones)

WhatsApp If Your Interview 
is confirmed: +91 9133 81 7162"""

FORMAT_3 = """+91 9133817162 whatsapp only

📢 Interview support
         Apttitude round support
             Online Test/Exam support 

We Cover All technologies example:
    Java | Python | Node.js | React.js | Angular .NET | Salesforce | DevOps | AWS | Azure GCP | Data Science | ML | AI | BA | Manual Testing Automation (Selenium, Cypress) ,SAP | ServiceNow SQL | Oracle | Power BI | Tableau n all

🎤 Proxy with advance software
Which gonna be invisible to panalist
🔹 100℅ invisible on screen share
🔹 100℅ invisible in task Manager
🔹 100% on spot answers
🔹 100℅ safe and secured 

🌍 supported 🇺🇸 🇬🇧 🇮🇳 🇨🇦 🇦🇺 & All

+91 9133817162 whatsapp only"""

FORMAT_4 = """_._._._._._._._._._._._
Interview Support 
°°°°°°°°°°°°°°°°°°°°

For all technologies, including:
📍Salesforce📍Java📍Java Full Stack📍C, C++📍Spring Boot Microservices📍Spring Hibernate📍Dot Net / .NET📍SAP📍Data Science📍AWS Admin📍AWS DevOps📍Azure Admin📍Azure Data Engineer📍Data Engineering📍Azure DevOps📍Selenium 📍Manual Testing📍Automation Testing📍Python📍Python Full Stack📍SQL📍Power BI📍REST API📍Django📍Big Data📍React JS & Node.js📍MongoDB📍Oracle📍Data Analyst📍BA📍ETL📍DevOps📍React Angular📍QA📍Azure📍Dot Net📍PL/SQL📍 Networking📍ServiceNow📍AI/ML

We provide support using advanced tools which are:
🔹 100% invisible in Task Manager
🔹 100% invisible on screen share
🔹 100% on spot answers
🔹 100% safe and secured

For: INDIA, USA, UK, Canada, Aust
(IST/CST/PST/EST time zones)

WhatsApp me for more details....
+91 98850 74380"""

FORMATS = [FORMAT_1, FORMAT_2, FORMAT_3, FORMAT_4]

# ================= STATE =================

last_format_index = {}
active_groups = set()

# ================= HELPERS =================

def next_format(chat_id):
    i = last_format_index.get(chat_id, -1)
    i = (i + 1) % len(FORMATS)
    last_format_index[chat_id] = i
    return FORMATS[i]

def contains_keyword(text):
    t = text.lower()
    return any(k.lower() in t for k in KEYWORDS)

# ================= CLIENT =================

client = TelegramClient(session_name, api_id, api_hash)

# ================= SAFE SEND =================

async def send_message_safe(chat_id, chat_title, group_link):

    try:
        await asyncio.sleep(random.randint(5, 15))

        # Check last message
        last_msg = await client.get_messages(chat_id, limit=1)
        if last_msg and last_msg[0].out:
            print(f"⏭ Skipped (already last): {group_link}")
            return

        msg = next_format(chat_id)
        await client.send_message(chat_id, msg)

        print(f"✅ Sent in: {group_link}")

    except Exception as e:
        print(f"❌ Error in {group_link}: {e}")

    finally:
        active_groups.discard(chat_id)

# ================= MESSAGE HANDLER =================

@client.on(events.NewMessage)
async def handler(event):

    if event.out:
        return

    if not event.is_group:
        return

    if not event.raw_text:
        return

    chat = await event.get_chat()

    # Only public groups
    if not getattr(chat, "username", None):
        return

    group_link = f"https://t.me/{chat.username}"

    # ✅ Only selected groups
    if group_link not in TARGET_GROUPS:
        return

    text = event.raw_text.strip()
    length = len(text)
    has_keyword = contains_keyword(text)

    if not (has_keyword or length > 250):
        return

    gid = event.chat_id

    if gid in active_groups:
        print(f"⏳ Already queued: {chat.title}")
        return

    last_msg = await client.get_messages(gid, limit=1)
    if last_msg and last_msg[0].out:
        print(f"⏭ Skipped (our last msg): {chat.title}")
        return

    active_groups.add(gid)

    asyncio.create_task(
        send_message_safe(gid, chat.title, group_link)
    )

# ================= LIST GROUPS =================

async def list_joined_groups():
    # iterate through dialogs and print only actual group links
    async for dialog in client.iter_dialogs():
        # telethon sets dialog.is_group for group chats (including megagroups)
        if dialog.is_group and getattr(dialog.entity, "username", None):
            print(f"https://t.me/{dialog.entity.username}")

# ================= RUN =================

async def main():
    await client.start()
    me = await client.get_me()
    print(f"🚀 Bot Account: {me.first_name}, Running (Selected Groups Only)")

    # output group links only
    await list_joined_groups()

    await client.run_until_disconnected()

asyncio.run(main())