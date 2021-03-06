# (c) @AbirHasan2005

import asyncio
from pyrogram import types, errors
from configs import Config
from bot.core.db.database import db


async def show_settings(m: "types.Message"):
    usr_id = m.chat.id
    user_data = await db.get_user_data(usr_id)
    if not user_data:
        await m.edit("Failed to fetch your data from database!")
        return
    upload_as_doc = user_data.get("upload_as_doc", True)
    caption = user_data.get("caption", None)
    apply_caption = user_data.get("apply_caption", True)
    thumbnail = user_data.get("thumbnail", None)
    buttons_markup = [
        [types.InlineKeyboardButton(f"ππΏπ»πΎπ°π³π΄π³ π°π π³πΎπ²ππΌπ΄π½π {'β' if upload_as_doc else 'ποΈ'}",
                                    callback_data="triggerUploadMode")],
        [types.InlineKeyboardButton(f"π°πΏπΏπ»π π²π°πΏππΈπΎπ½ {'β' if apply_caption else 'ποΈ'}",
                                    callback_data="triggerApplyCaption")],
        [types.InlineKeyboardButton(f"π°πΏπΏπ»π π³π΄π΅π°ππ»π π²π°πΏππΈπΎπ½ {'ποΈ' if caption else 'β'}",
                                    callback_data="triggerApplyDefaultCaption")],
        [types.InlineKeyboardButton("ππ΄π π²ππππΎπΌ π²π°πΏππΈπΎπ½",
                                    callback_data="setCustomCaption")],
        [types.InlineKeyboardButton(f"{'π²π·π°π½πΆπ΄' if thumbnail else 'ππ΄π'} ππ·ππΌπ±π½π°πΈπ»",
                                    callback_data="setThumbnail")]
    ]
    if thumbnail:
        buttons_markup.append([types.InlineKeyboardButton("ππ·πΎπ ππ·ππΌπ±π½π°πΈπ»",
                                                          callback_data="showThumbnail")])
    if caption:
        buttons_markup.append([types.InlineKeyboardButton("ππ·πΎπ π²π°πΏππΈπΎπ½",
                                                          callback_data="showCaption")])
    buttons_markup.append([types.InlineKeyboardButton("π²π»πΎππ΄",
                                                      callback_data="closeMessage")])

    try:
        await m.edit(
            text="**- π²ππππΎπΌπΈππ΄ ππ·π΄ π±πΎπ ππ΄πππΈπ½πΆπ -**",
            reply_markup=types.InlineKeyboardMarkup(buttons_markup),
            disable_web_page_preview=True,
            parse_mode="Markdown"
        )
    except errors.MessageNotModified: pass
    except errors.FloodWait as e:
        await asyncio.sleep(e.x)
        await show_settings(m)
    except Exception as err:
        Config.LOGGER.getLogger(__name__).error(err)
