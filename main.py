from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, ForceReply
from pyrogram.types import InlineKeyboardMarkup as Keyboard, InlineKeyboardButton as Button
from pyrogram.errors import (ApiIdInvalid, PhoneNumberInvalid, PhoneCodeInvalid, PhoneCodeExpired, SessionPasswordNeeded, PasswordHashInvalid)
from pyrogram.errors import UserNotParticipant
from pyrolistener import Listener, exceptions
from typing import Union
import config


app = Client(
    "SessionsGenerator",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)
listener = Listener(client=app)


markup: Keyboard = Keyboard([
        [
            Button(config.OWNER_NAME, user_id=config.OWNER_ID)
        ],
        [
            Button("𝙿𝚈𝚁𝙾𝙶𝚁𝙰𝙼 (𝙱𝙾𝚃) 𖢣", "pyrogram bot"),
            Button("𝙿𝚈𝚁𝙾𝙶𝚁𝙰𝙼  𝚅2 𝄵", "pyrogram 2")
        ],
    ])


@app.on_message(filters.command("generate"))
@app.on_message(filters.command("start"))
async def s_type(_: Client, message: Message):
    user_id = message.from_user.id 
    subscribe = await subscription(user_id)
    if subscribe: return await message.reply(f"- 𝚈𝙾𝚄 𝙽𝙴𝙴𝙳 𝚃𝙾 𝚂𝚄𝙱𝚂𝙲𝚁𝙸𝙱𝙴 𝚃𝙾 𝙱𝙾𝚃 𝙲𝙷𝙰𝙽𝙽𝙴𝙻 𝙵𝙸𝚁𝚂𝚃.\n\n- 𝙲𝙷𝙰𝙽𝙽𝙴𝙻: {subscribe}\n\n- 𝚂𝚄𝙱𝚂𝙲𝚁𝙸𝙱𝙴 𝚃𝙷𝙴𝙽 𝚂𝙴𝙽𝙳 : /start", reply_to_message_id=message.id)
    caption = " 𝙲𝙷𝙾𝙾𝚂𝙴 𝚈𝙾𝚄𝚁 𝙿𝚈𝚁𝙾𝙶𝚁𝙰𝙼 𝚅𝙴𝚁𝚂𝙸𝙾𝙽 𝙰𝙽𝙳 𝙸𝙵 𝚃𝙷𝙴 𝚂𝙴𝚂𝚂𝙸𝙾𝙽 𝙵𝙾𝚁 𝙰 𝙱𝙾𝚃 𝙾𝚁 𝙽𝙾𝚃 𓀎"
    await message.reply(caption, reply_markup=markup, reply_to_message_id=message.id)


@app.on_callback_query(filters.regex(r"^(pyrogram )"))
async def gen(_: Client, callback: CallbackQuery):
    cd: str = callback.data
    is_bot: Union[None, bool] = None
    version: Union[None, int] = None
    if cd.endswith("bot"):
        await callback.answer("- 𝚃𝙷𝙴 𝚂𝙴𝚂𝚂𝙸𝙾𝙽 𝚆𝙸𝙻𝙻 𝙱𝙴 𝙸𝙽 𝙿𝚈𝚁𝙾𝙶𝚁𝙰𝙼  𝚅2 𝄵", show_alert=True)
        is_bot = True
        version = 2
    else: version = 2
    await callback.edit_message_text("- 𝙿𝚈𝚁𝙾𝙶𝚁𝙰𝙼 𝚂𝙴𝚂𝚂𝙸𝙾𝙽 𝙴𝚇𝚃𝚁𝙰𝙲𝚃𝙾𝚁 𝚂𝚃𝙰𝚁𝚃𝙴𝙳.")
    s_vars = await getter(callback, is_bot)
    if not s_vars: return
    await registration(s_vars[0], s_vars[1], s_vars[2], is_bot, callback)
        

async def getter(callback: CallbackQuery, is_bot: bool):
    user_id: int = callback.from_user.id
    try: s_api_id: Message = await listener.listen(
        from_id=user_id,
        chat_id=user_id,
        text="- 𝚂𝙴𝙽𝙳 𝚈𝙾𝚄𝚁 𝙰𝙿𝙸 𝙸𝙳 \n- 𝚂𝙴𝙽𝙳 /default 𝚃𝙾 𝚄𝚂𝙴 𝙳𝙴𝙵𝙰𝚄𝙻𝚃 𝙰𝙿𝙸𝚂\n- 𝚂𝙴𝙽𝙳 /cancel 𝚃𝙾 𝚂𝚃𝙾𝙿 𝚃𝙷𝙴 𝙿𝚁𝙾𝙲𝙴𝚂𝚂",
        reply_markup=ForceReply(selective=True, placeholder="- 𝚈𝙾𝚄𝚁 𝙰𝙿𝙸 𝙸𝙳 : "),
        reply_to_message_id=callback.message.id,
        timeout=60,
    )
    except exceptions.TimeOut: return await callback.message.reply("- 𝚁𝚄𝙽 𝙾𝚄𝚃 𝙾𝙵 𝚃𝙸𝙼𝙴 𝚃𝙾 𝚁𝙴𝙲𝙴𝙸𝚅𝙴 𝚃𝙷𝙴 𝙰𝙿𝙸 𝙸𝙳.", reply_markup=markup)
    if s_api_id.text == "/default": 
        _id: int = app.api_id
        _hash: str = app.api_hash
    elif s_api_id.text == "/cancel":
        await s_api_id.reply("- 𝙿𝚈𝚁𝙾𝙶𝚁𝙰𝙼 𝚂𝙴𝚂𝚂𝙸𝙾𝙽 𝙲𝙰𝙽𝙲𝙴𝙻𝙻𝙴𝙳.", reply_markup=markup, reply_to_message_id=s_api_id.id)
        return False
    else:
        try: int(s_api_id.text)
        except ValueError: return await s_api_id.reply("- 𝙰𝙿𝙸 𝙸𝙳 𝙼𝚄𝚂𝚃 𝙱𝙴 𝚃𝚈𝙿𝙴 𝙾𝙵 𝙸𝙽𝚃𝙴𝙶𝙴𝚁\n- 𝚃𝚁𝚈 𝙰𝙶𝙰𝙸𝙽.", reply_to_message_id=s_api_id.id,  reply_markup=markup)
        try: s_api_hash: Message = await listener.listen(
            from_id=user_id,
            chat_id=user_id,
            text="- 𝚂𝙴𝙽𝙳 𝚈𝙾𝚄𝚁 𝙰𝙿𝙸 𝙷𝙰𝚂𝙷\n- 𝚂𝙴𝙽𝙳 /cancel 𝚃𝙾 𝙲𝙰𝙽𝙲𝙴𝙻 𝚃𝙷𝙴 𝙿𝚁𝙾𝙲𝙴𝚂𝚂.",
            reply_markup=ForceReply(selective=True, placeholder="- 𝚈𝙾𝚄𝚁 𝙰𝙿𝙸 𝙷𝙰𝚂𝙷 : "),
            reply_to_message_id=s_api_id.id,
            timeout=60
        )
        except exceptions.TimeOut: await callback.message.reply("- 𝚁𝚄𝙽 𝙾𝚄𝚃 𝙾𝙵 𝚃𝙸𝙼𝙴 𝚃𝙾 𝚁𝙴𝙲𝙴𝙸𝚅𝙴 𝚃𝙷𝙴 𝙰𝙿𝙸 𝙷𝙰𝚂𝙷. ‌ਊ", reply_markup=markup)
        if s_api_hash.text == "/cancel":
            await s_api_hash.reply("- 𝙿𝚈𝚁𝙾𝙶𝚁𝙰𝙼 𝚂𝙴𝚂𝚂𝙸𝙾𝙽 𝙲𝙰𝙽𝙲𝙴𝙻𝙻𝙴𝙳.", reply_markup=markup, reply_to_message_id=s_api_hash.id)
            return False
        _id, _hash = int(s_api_id.text), s_api_hash.text
    try: tp: Message = await listener.listen(
        from_id=user_id,
        chat_id=user_id,
        text=f"- 𝚂𝙴𝙽𝙳 𝚈𝙾𝚄𝚁 {'𝙱𝙾𝚃 𝚃𝙾𝙺𝙴𝙽' if is_bot else '𝙿𝙷𝙾𝙽𝙴 𝙽𝚄𝙼𝙱𝙴𝚁 -> +128372'}\n- 𝚂𝙴𝙽𝙳 /cancel 𝚃𝙾 𝙺𝙸𝙻𝙻 𝚃𝙷𝙴 𝙿𝚁𝙾𝙲𝙴𝚂𝚂. ࿊",
        reply_markup=ForceReply(selective=True, placeholder=f"- 𝚈𝙾𝚄𝚁 {'𝙱𝙾𝚃 𝚃𝙾𝙺𝙴𝙽' if is_bot else '𝙿𝙷𝙾𝙽𝙴 𝙽𝚄𝙼𝙱𝙴𝚁'} : "),
        timeout=60
    )
    except exceptions.TimeOut: await callback.message.reply("- 𝚁𝚄𝙽 𝙾𝚄𝚃 𝙾𝙵 𝚃𝙸𝙼𝙴 𝚃𝙾 𝚁𝙴𝙲𝙴𝙸𝚅𝙴 𝚃𝙷𝙴 𝙱𝙾𝚃 𝚃𝙾𝙺𝙴𝙽. ‌ਊ", reply_markup=markup)
    if tp.text == "/cancel":
        await tp.reply("- 𝙿𝚈𝚁𝙾𝙶𝚁𝙰𝙼 𝚂𝙴𝚂𝚂𝙸𝙾𝙽 𝙲𝙰𝙽𝙲𝙴𝙻𝙻𝙴𝙳.", reply_to_message_id=tp.id, reply_markup=markup)
        return False
    elif is_bot:
        _token = tp.text
        return _id, _hash, _token
    else :
        _number = tp.text
        return _id, _hash, _number
    

async def registration(_id: int, _hash: str, tp: str, is_bot: bool, callback: CallbackQuery):
    user_id = callback.from_user.id
    _token = tp if is_bot else None
    _number = tp if not is_bot else None
    await callback.message.reply(f"- 𝚃𝚁𝚈𝙸𝙽𝙶 𝚃𝙾 𝚂𝙸𝙶𝙽 𝙸𝙽 𝚅𝙸𝙰 {'𝙱𝙾𝚃 𝚃𝙾𝙺𝙴𝙽' if is_bot else '𝙿𝙷𝙾𝙽𝙴 𝙽𝚄𝙼𝙱𝙴𝚁'} 𐂠")
    if is_bot:
        client = Client("bot", api_id=_id, api_hash=_hash, bot_token=_token, in_memory=True)
        await client.connect()
        try:await client.sign_in_bot(_token)
        except: return await callback.message.reply(" 𝙸𝙽𝚅𝙰𝙻𝙸𝙳 𝙱𝙾𝚃 𝚃𝙾𝙺𝙴𝙽.\n- 𝚃𝚁𝚈 𝙰𝙶𝙰𝙸𝙽.", reply_markup=markup)
        session = await client.export_session_string()
        return await callback.message.reply(
            f"- 𝚈𝙾𝚄𝚁 𝚂𝙴𝚂𝚂𝙸𝙾𝙽 𝙷𝙰𝚂 𝙱𝙴𝙴𝙽 𝙶𝙴𝙽𝙴𝚁𝙰𝚃𝙴𝙳\n\n`{session}`",
            reply_to_message_id = callback.message.id
        )
    client: Client = Client("acc", in_memory=True)
    client.api_id = _id
    client.api_hash = _hash
    await client.connect()
    try: p_code_hash = await client.send_code(_number)
    except (ApiIdInvalid): return await callback.message.reply("- 𝚃𝙷𝙴𝚁𝙴 𝙸𝚂 𝙰𝙽 𝙴𝚁𝚁𝙾𝚁 𝚆𝙸𝚃𝙷 𝚈𝙾𝚄𝚁 \"𝙰𝙿𝙸 𝙸𝙳\" 𝙾𝚁 \"𝙰𝙿𝙸 𝙷𝙰𝚂𝙷\".\n- 𝚃𝚁𝚈 𝙰𝙶𝙰𝙸𝙽, 𝙿𝙻𝙴𝙰𝚂𝙴.", reply_markup=markup)
    except (PhoneNumberInvalid): return await callback.message.reply("- 𝚃𝙷𝙴𝚁𝙴 𝙸𝚂 𝙰𝙽 𝙴𝚁𝚁𝙾𝚁 𝚆𝙸𝚃𝙷 𝚈𝙾𝚄𝚁 \"𝙿𝙷𝙾𝙽𝙴 𝙽𝚄𝙼𝙱𝙴𝚁\".\n- 𝚃𝚁𝚈 𝙰𝙶𝙰𝙸𝙽, 𝙿𝙻𝙴𝙰𝚂𝙴.", reply_markup=markup)
    try: code = await listener.listen(
        from_id=user_id,
        chat_id=user_id,
        text="- 𝚆𝙴 𝙷𝙰𝚅𝙴 𝚂𝙴𝙽𝚃 𝙰𝙽 𝙾𝚃𝙿 𝙲𝙾𝙳𝙴 𝚃𝙾 𝚈𝙾𝚄𝚁 𝙰𝙲𝙲𝙾𝚄𝙽𝚃. \n- 𝙲𝙷𝙴𝙲𝙺 𝚈𝙾𝚄𝚁 𝙿𝚁𝙸𝚅𝙰𝚃𝙴 𝙲𝙷𝙰𝚃𝚂. ‌♡⁩",
        timeout=120,
        reply_markup=ForceReply(selective=True, placeholder="𝙸𝙽 𝚃𝙷𝙸𝚂 𝙵𝙾𝚁𝙼𝚄𝙻𝙰: 1 2 3 4 5 6")
    )
    except exceptions.TimeOut: return await callback.message.reply("- 𝚃𝙷𝙴 𝚃𝙸𝙼𝙴 𝚃𝙾 𝚁𝙴𝙲𝙴𝙸𝚅𝙴 𝚃𝙷𝙴 𝙲𝙾𝙳𝙴 𝙷𝙰𝚂 𝚁𝚄𝙽 𝙾𝚄𝚃.\n - 𝚃𝚁𝚈 𝙰𝙶𝙰𝙸𝙽.", reply_markup=markup)
    try: await client.sign_in(_number, p_code_hash.phone_code_hash, code.text.replace(" ", ""))
    except (PhoneCodeInvalid): return await callback.message.reply("- 𝚃𝙷𝙴 𝙲𝙾𝙳𝙴 𝚈𝙾𝚄 𝙷𝙰𝚅𝙴 𝚂𝙴𝙽𝚃 𝙸𝚂 𝚆𝚁𝙾𝙽𝙶.\n- 𝚃𝚁𝚈 𝙰𝙶𝙰𝙸𝙽.", reply_markup=markup, reply_to_message_id=code.id)
    except (PhoneCodeExpired): return await callback.message.reply("- 𝚃𝙷𝙴 𝙲𝙾𝙳𝙴 𝚈𝙾𝚄 𝙷𝙰𝚅𝙴 𝚂𝙴𝙽𝚃 𝙸𝚂 𝙴𝚇𝙿𝙸𝚁𝙴𝙳.\n- 𝚃𝚁𝚈 𝙰𝙶𝙰𝙸𝙽.", reply_markup=markup, reply_to_message_id=code.id)
    except (SessionPasswordNeeded):
        try:password = await listener.listen(
            from_id=user_id,
            chat_id=user_id,
            text="- 𝙴𝙽𝚃𝙴𝚁 𝚈𝙾𝚄𝚁 𝚃𝚆𝙾 𝚂𝚃𝙴𝙿 𝚅𝙴𝚁𝙸𝙵𝙸𝙲𝙰𝚃𝙸𝙾𝙽 𝙿𝙰𝚂𝚂𝚆𝙾𝚁𝙳.",
            reply_markup=ForceReply(selective=True, placeholder="- 𝚈𝙾𝚄𝚁 𝙿𝙰𝚂𝚂𝚆𝙾𝚁𝙳: "),
            timeout=180,
            reply_to_message_id=code.id
        )
        except exceptions.TimeOut:return await callback.message.reply("- 𝚃𝙷𝙴 𝚃𝙸𝙼𝙴 𝚃𝙾 𝚁𝙴𝙲𝙴𝙸𝚅𝙴 𝚃𝙷𝙴 𝙿𝙰𝚂𝚂𝚆𝙾𝚁𝙳 𝙷𝙰𝚂 𝚁𝚄𝙽 𝙾𝚄𝚃.",  reply_markup=markup)
        try: await client.check_password(password.text)
        except (PasswordHashInvalid): return await callback.message.reply("- 𝚃𝚆𝙾 𝚂𝚃𝙴𝙿 𝚅𝙴𝚁𝙸𝙵𝙸𝙲𝙰𝚃𝙸𝙾𝙽 𝙿𝙰𝚂𝚂𝚆𝙾𝚁𝙳 𝙸𝚂 𝙸𝙽𝚅𝙰𝙻𝙸𝙳. \n- 𝚃𝚁𝚈 𝙰𝙶𝙰𝙸𝙽. ", reply_markup=markup)
    session = await client.export_session_string()
    await client.send_message(
        "me",
        f"- 𝚈𝙾𝚄𝚁 𝚂𝙴𝚂𝚂𝙸𝙾𝙽 𝙷𝙰𝚂 𝙱𝙴𝙴𝙽 𝙶𝙴𝙽𝙴𝚁𝙰𝚃𝙴𝙳\n\n`{session}`",
        reply_to_message_id = callback.message.id
    )
    await client.disconnect()
    await app.send_message(user_id, "- 𝚈𝙾𝚄𝚁 𝙿𝚈𝚁𝙾𝙶𝚁𝙰𝙼 𝚂𝙴𝚂𝚂𝙸𝙾𝙽 𝙷𝙰𝚂 𝙱𝙴𝙴𝙽 𝙶𝙴𝙽𝙴𝚁𝙰𝚃𝙴𝙳 𝚂𝚄𝙲𝙲𝙴𝚂𝚂𝙵𝚄𝙻𝙻𝚈. \n- 𝙲𝙷𝙴𝙲𝙺 𝚈𝙾𝚄𝚁 𝚂𝙰𝚅𝙴𝙳 𝙼𝙴𝚂𝚂𝙰𝙶𝙴𝚂. 💙", reply_markup=Keyboard([[Button("ᯓ 𓆩 ˹𝙱𝙴𝙽˼ 𓆪 #1", user_id=5451878368)]]))


@app.on_message(filters.regex(r"^(المطور|المبرمج|بن|dev|ben|programmer|developer)$"))
async def dev(_: Client, message: Message):
    d_id = 5451878368 # YOUR ID
    user = await app.get_chat(d_id)
    p_path = await app.download_media(user.photo.big_file_id, file_name="downloads/developer.jpg")
    bio = user.bio
    fname = user.first_name 
    ky = Keyboard([[Button(fname, user_id=d_id)]])
    await message.reply_photo(p_path, caption=bio, reply_markup=ky, reply_to_message_id=message.id)


async def subscription(user_id):
    try: await app.get_chat_member(config.SUBSCRIBE_CHANNEL, user_id)
    except UserNotParticipant: return "@" + config.SUBSCRIBE_CHANNEL
    return 


app.run()
