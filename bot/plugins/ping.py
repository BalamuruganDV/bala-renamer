# (c) @Aadhi000
from bot.client import Client
from pyrogram import filters
from pyrogram import types
from bot.core.db.add import add_user_to_database


@Client.on_message(filters.command(["start", "ping"]) & filters.private & ~filters.edited)
async def ping_handler(c: Client, m: "types.Message"):
    if not m.from_user:
        return await m.reply_text("I don't know about you sir :(")
    await add_user_to_database(c, m)
    await c.send_flooded_message(
        chat_id=m.chat.id,
        text="<b>π·π΄π πΈ π°πΌ πΎπΏ-ππ΄π½π°πΌπ΄ π±πΎπ!</b>\n\n"
             "<b>πΈ π²π°π½ ππ΄π½π°πΌπ΄ πΌπ΄π³πΈπ° ππΈππ·πΎππ π³πΎππ½π»πΎπ°π³πΈπ½πΆ πΈπ!</b>\n"
             "<b>ππΏπ΄π΄π³ π³π΄πΏπ΄π½π³π πΎπ½ ππΎππ πΌπ΄π³πΈπ° π³π².</b>\n\n"
             "<b>πΉπππ ππ΄π½π³ πΌπ΄ πΌπ΄π³πΈπ° π°π½π³ ππ΄πΏπ»π πΈπ ππΈππ· /rename π²πΎπΌπΌπ°π½π³.</b>",
        reply_markup=types.InlineKeyboardMarkup([[
           types.InlineKeyboardButton("π±πΎπ ππ΄πππΈπ½πΆπ",
                                      callback_data="showSettings")
        ]])
    )


@Client.on_message(filters.command("help") & filters.private & ~filters.edited)
async def help_handler(c: Client, m: "types.Message"):
    if not m.from_user:
        return await m.reply_text("I don't know about you sar :(")
    await add_user_to_database(c, m)
    await c.send_flooded_message(
        chat_id=m.chat.id,
        text="<b>πΈ π²π°π½ ππ΄π½π°πΌπ΄ πΌπ΄π³πΈπ° ππΈππ·πΎππ π³πΎππ½π»πΎπ°π³πΈπ½πΆ πΈπ!</b>\n"
             "<b>ππΏπ΄π΄π³ π³π΄πΏπ΄π½π³π πΎπ½ ππΎππ πΌπ΄π³πΈπ° π³π².</b>\n\n"
             "<b>πΉπππ ππ΄π½π³ πΌπ΄ πΌπ΄π³πΈπ° π°π½π³ ππ΄πΏπ»π πΈπ ππΈππ· /rename π²πΎπΌπΌπ°π½π³.</b>\n\n"
             "<b>ππΎ ππ΄π π²ππππΎπΌ ππ·ππΌπ±π½π°πΈπ» ππ΄πΏπ»π ππΎ π°π½π πΈπΌπ°πΆπ΄ ππΈππ· /set_thumbnail</b>\n\n"
             "<b>ππΎ ππ΄π΄ π²ππππΎπΌ ππ·ππΌπ±π½π°πΈπ» πΏππ΄ππ /show_thumbnail</b>",
        reply_markup=types.InlineKeyboardMarkup([[
           types.InlineKeyboardButton("π±πΎπ ππ΄πππΈπ½πΆπ",
                                      callback_data="showSettings")]])
    )
