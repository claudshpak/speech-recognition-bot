import os
import uuid
import aiofiles
import asyncio
import logging
import speech_recognition as sr
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F
from logger import setup_logger

setup_logger()

r = sr.Recognizer()
router = Router()

os.makedirs("./voice", exist_ok=True)
os.makedirs("./ready", exist_ok=True)

def recognise(filename):
    with sr.AudioFile(filename) as source:
        audio_text = r.record(source)
        
        try:
            text_ru = r.recognize_google(audio_text, language='ru-RU')
            logging.info('Распознано на русском')
            return f"{text_ru}"
        except:
            pass
        
        try:
            text_en = r.recognize_google(audio_text, language='en-US')
            logging.info('Распознано на английском')
            return f"{text_en}"
        except:
            pass
        
        logging.exception('Не удалось распознать аудио')
        return "Не получилось распознать аудио. Попробуйте еще раз."

async def process_voice_message(message: Message, file_id, file_extension='ogg'):
    logging.info('Получено голосовое сообщение от %s', message.from_user.username)
    
    processing_msg = await message.reply("✅ Получил, обрабатываю...")
    
    filename = str(uuid.uuid4())
    file_name_full = f"./voice/{filename}.{file_extension}"
    file_name_full_converted = f"./ready/{filename}.wav"

    try:
        file_info = await message.bot.get_file(file_id)
        downloaded_file = await message.bot.download_file(file_info.file_path)

        async with aiofiles.open(file_name_full, 'wb') as new_file:
            await new_file.write(downloaded_file.getvalue())

        process = await asyncio.create_subprocess_exec(
            'ffmpeg', '-i', file_name_full, file_name_full_converted
        )
        await process.communicate()

        text = recognise(file_name_full_converted)

        await processing_msg.delete()
        await message.reply(text)
        logging.info('Отправлено сообщение')

    except Exception as e:
        await processing_msg.edit_text("❌ Произошла ошибка при обработке")
        logging.exception('Ошибка при обработке аудио: %s', e)

@router.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer("Перешлите мне голосовое сообщение на русском или английском, и я его расшифрую.")

@router.message(F.content_type == 'voice')
async def voice_processing(message: Message):
    file_id = message.voice.file_id
    await process_voice_message(message, file_id)

@router.message(F.content_type == 'audio')
async def audio_processing(message: Message):
    if message.audio and not message.audio.title and not message.audio.performer:
        file_id = message.audio.file_id
        await process_voice_message(message, file_id, 'ogg')
    else:

        await message.answer("Ничего не понятно")

