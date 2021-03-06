# (c) @Aadhi000

import time
import mimetypes
import traceback
from bot.client import (
    Client
)
from pyrogram import filters
from pyrogram.file_id import FileId
from pyrogram.types import Message
from bot.core.file_info import (
    get_media_file_id,
    get_media_file_size,
    get_media_file_name,
    get_file_type,
    get_file_attr
)
from configs import Config
from bot.core.display import progress_for_pyrogram
from bot.core.db.database import db
from bot.core.db.add import add_user_to_database
from bot.core.handlers.not_big import handle_not_big
from bot.core.handlers.time_gap import check_time_gap
from bot.core.handlers.big_rename import handle_big_rename


@Client.on_message(filters.command(["rename", "r"]) & filters.private & ~filters.edited)
async def rename_handler(c: Client, m: Message):
    # Checks
    if not m.from_user:
        return await m.reply_text("I don't know about you sar :(")
    if m.from_user.id not in Config.PRO_USERS:
        is_in_gap, sleep_time = await check_time_gap(m.from_user.id)
        if is_in_gap:
            await m.reply_text("ππΎπππ ππΈπ,\n"
                               "π½πΎ π΅π»πΎπΎπ³πΈπ½πΆ π°π»π»πΎππ΄π³!\n\n"
                               f"ππ΄π½π³ ππ·πΈπ π°π΅ππ΄π `{str(sleep_time)}s` !!",
                               quote=True)
            return
    await add_user_to_database(c, m)
    if (not m.reply_to_message) or (not m.reply_to_message.media) or (not get_file_attr(m.reply_to_message)):
        return await m.reply_text("ππ΄πΏπ»π ππΎ π°π½π π³πΎπ²ππΌπ΄π½π/ππΈπ³π΄πΎ/π°ππ³πΈπΎ ππΎ ππ΄π½π°πΌπ΄ πΈπ!", quote=True)

    # Proceed
    editable = await m.reply_text("π½πΎπ ππ΄π½π³ πΌπ΄ π½π΄π π΅πΈπ»π΄ π½π°πΌπ΄!", quote=True)
    user_input_msg: Message = await c.listen(m.chat.id)
    if user_input_msg.text is None:
        await editable.edit("<b>πΏππΎπ²π΄ππ π²π°π½π²π΄π»π»π΄π³</b>")
        return await user_input_msg.continue_propagation()
    if user_input_msg.text and user_input_msg.text.startswith("/"):
        await editable.edit("<b>πΏππΎπ²π΄ππ π²π°π½π²π΄π»π»π΄π³</b>")
        return await user_input_msg.continue_propagation()
    _raw_file_name = get_media_file_name(m.reply_to_message)
    if not _raw_file_name:
        _file_ext = mimetypes.guess_extension(get_file_attr(m.reply_to_message).mime_type)
        _raw_file_name = "UnknownFileName" + _file_ext
    if user_input_msg.text.rsplit(".", 1)[-1].lower() != _raw_file_name.rsplit(".", 1)[-1].lower():
        file_name = user_input_msg.text.rsplit(".", 1)[0][:255] + "." + _raw_file_name.rsplit(".", 1)[-1].lower()
    else:
        file_name = user_input_msg.text[:255]
    await editable.edit("<b>π°π²π²π΄πππΈπ½πΆ π΅πΈπ»π΄ π³π΄ππ°πΈπ»π...</b>")
    is_big = get_media_file_size(m.reply_to_message) > (10 * 1024 * 1024)
    if not is_big:
        _default_thumb_ = await db.get_thumbnail(m.from_user.id)
        if not _default_thumb_:
            _m_attr = get_file_attr(m.reply_to_message)
            _default_thumb_ = _m_attr.thumbs[0].file_id \
                if (_m_attr and _m_attr.thumbs) \
                else None
        await handle_not_big(c, m, get_media_file_id(m.reply_to_message), file_name,
                             editable, get_file_type(m.reply_to_message), _default_thumb_)
        return
    file_type = get_file_type(m.reply_to_message)
    _c_file_id = FileId.decode(get_media_file_id(m.reply_to_message))
    try:
        c_time = time.time()
        file_id = await c.custom_upload(
            file_id=_c_file_id,
            file_size=get_media_file_size(m.reply_to_message),
            file_name=file_name,
            progress=progress_for_pyrogram,
            progress_args=(
                "ππΏπ»πΎπ°π³πΈπ½πΆ.....\n"
                f"DC: {_c_file_id.dc_id}",
                editable,
                c_time
            )
        )
        if not file_id:
            return await editable.edit("Failed to Rename!\n\n"
                                       "Maybe your file corrupted :(")
        await handle_big_rename(c, m, file_id, file_name, editable, file_type)
    except Exception as err:
        await editable.edit("Failed to Rename File!\n\n"
                            f"**Error:** `{err}`\n\n"
                            f"**Traceback:** `{traceback.format_exc()}`")
