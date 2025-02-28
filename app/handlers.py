from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
import random
import os 
 
import shutil
from app.utils import download
from app.state import get_msg
from app.form_pic import form_text, add_photo, conv_to_pdf

router = Router()

@router.message(CommandStart())
async def start_msg(msg: Message, state: FSMContext):
    await msg.answer("Я помогу Вам создать фото для участия в акции «Бессмертный полк». Отправьте мне фотографию вашего родственника.")
    await state.set_state(get_msg.get_photo)

@router.message(get_msg.get_photo)
async def get_photo(msg: Message, state: FSMContext):
    if msg.photo: 
        await state.update_data({"photo": msg.photo[-1].file_id})
        await msg.answer('Напишите ФИО родственника.')
        await state.set_state(get_msg.get_name)
        
    else: 
        await msg.answer('Это не тот фото, пожалуйста отправьте фото!')


@router.message(get_msg.get_name)
async def get_photo(msg: Message, state: FSMContext):
    if len(msg.text.split()) >= 3:
        if len(msg.text) < 45:
            await state.update_data({'name':msg.text})
            await msg.answer('Напишите годы жизни в формате: 1900-1975')
            await state.set_state(get_msg.get_era)

        else:
            await msg.answer('Имя слишком длинное, пожалуйста проверьте сообщение.')
    else:
            await msg.answer('Это не похоже на ФИО, попробуйте еще раз.')


@router.message(get_msg.get_era)
async def get_photo(msg: Message, state: FSMContext):
    if len(msg.text) < 13:
        await state.set_state(get_msg.get_rod)
        await state.update_data({'era':msg.text})
        await msg.answer('Напишите родословную связь, Ваше ФИО и организацию в формате: дед Ивановой Л.И., «название организации»')

    else:
        await msg.answer('Сообщение слишком большое, пожалуйста проверьте сообщение.')




@router.message(get_msg.get_rod)
async def get_photo(msg: Message, state: FSMContext):
    if len(msg.text) < 100:
        await state.update_data({'rod':msg.text})
    else:
        await msg.answer('Сообщение слишком большое, пожалуйста проверьте сообщение.')
    if await state.get_value('rod'):    
        id = random.randint(1,100)
        res = await state.get_data()
        photo_path = await download(res['photo'], msg=msg, id=id)
        path_to_changed_file = form_text(res=res, id=id)
        add_photo(img_path=photo_path,chandged_path=path_to_changed_file)
        new_path = conv_to_pdf(path=path_to_changed_file, id=id)
        path_xxx = FSInputFile(new_path, f"changed_{id}.pdf")
        
        
        await msg.answer_photo(path_xxx,caption='Результат!')
        await msg.answer_document(document=path_xxx, caption='Файл для вашего удобства')
        await msg.bot.send_document(chat_id='-4720386700', document=path_xxx)
        await msg.bot.send_document(chat_id='-4720386700', document=FSInputFile(f'changed_{id}.pptx'))

        shutil.rmtree(f'output_{id}') 
        os.remove(f'dwnload_pic_{id}')
        os.remove(f'changed_{id}.pptx') 
        await state.clear()
