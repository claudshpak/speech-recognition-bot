import os
import uuid
import aiofiles
import asyncio
import logging
import speech_recognition as sr
from aiogram import Router, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, ContentType
from logger import setup_logger

setup_logger()

language = 'ru-RU'
r = sr.Recognizer()
router = Router()



def recognise(filename):
    with sr.AudioFile(filename) as source:
        audio_text = r.record(source)
        try:
            text = r.recognize_google(audio_text, language=language)
            logging.info('Конвертирую')
            return text
        except Exception as e:
            logging.exception('Ошибка при распознавании: %s', e)
            return "Не получилось, попробуйте еще раз"

@router.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer("Перешли мне голосовое сообщение, и я его расшифрую.")

@router.message(ContentType.VOICE)
async def voice_processing(message: Message):
    logging.info('Получено голосовое сообщение от %s', message.from_user.username)
    filename = str(uuid.uuid4())
    file_name_full = f"./voice/{filename}.ogg"
    file_name_full_converted = f"./ready/{filename}.wav"

    file_info = await message.voice.get_file()
    downloaded_file = await message.bot.download_file(file_info.file_path)

    async with aiofiles.open(file_name_full, 'wb') as new_file:
        await new_file.write(downloaded_file.getvalue())

    process = await asyncio.create_subprocess_exec(
        'ffmpeg', '-i', file_name_full, file_name_full_converted
    )
    await process.communicate()

    text = recognise(file_name_full_converted)

    await message.reply(text)
    logging.info('Отправлено сообщение')

    os.remove(file_name_full)
    os.remove(file_name_full_converted)

