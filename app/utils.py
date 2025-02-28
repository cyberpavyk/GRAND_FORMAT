import aiogram.types as tp
async def download(file_id, msg: tp.Message, id):
    file = await msg.bot.get_file(file_id=file_id)
    await msg.bot.download_file(file.file_path, f'dwnload_pic_{id}')
    return f'dwnload_pic_{id}'