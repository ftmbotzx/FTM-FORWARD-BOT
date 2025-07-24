
from pyrogram import Client
from config import Config

user_states = {}

@app.on_callback_query(filters.regex("userbot#string"))
async def prompt_string_session(client, query):
    user_id = query.from_user.id
    user_states[user_id] = "awaiting_string_session"
    await query.message.edit("🔐 Send me your Pyrogram String Session (v2) to activate the userbot.")

@app.on_message(filters.private & filters.user(Config.SUDO_USERS))
async def receive_string_session(client, message):
    user_id = message.from_user.id
    if user_states.get(user_id) == "awaiting_string_session":
        session = message.text.strip()
        try:
            userbot = Client(
                name="userbot",
                session_string=session,
                api_id=Config.API_ID,
                api_hash=Config.API_HASH
            )
            await userbot.start()
            me = await userbot.get_me()
            await message.reply(f"✅ Userbot logged in as {me.first_name} (@{me.username})")
            # Optionally store session in database
        except Exception as e:
            await message.reply(f"❌ Failed to log in: {e}")
        user_states[user_id] = None
