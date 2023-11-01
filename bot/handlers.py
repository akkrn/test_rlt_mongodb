from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from utils import aggregate_salaries
from validators import is_valid_json

router = Router()

re_patttern = r'{\s*"dt_from":\s*"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}",\s*"dt_upto":\s*"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}",\s*"group_type":\s*"(day|month|hour)"\s*}\s*'


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(f"Hi {message.from_user.full_name}!")


@router.message(F.text.regexp(re_patttern))
async def process_main(message: Message):
    if is_valid_json(message.text):
        await message.answer(await aggregate_salaries(message.text))
    else:
        await message.answer(
            "Допустимо отправлять только следующие запросы:"
            '{"dt_from": "2022-09-01T00:00:00", "dt_upto": "2022-12-31T23:59:00", "group_type": "month"}'
            '{"dt_from": "2022-10-01T00:00:00", "dt_upto": "2022-11-30T23:59:00", "group_type": "day"}'
            '{"dt_from": "2022-02-01T00:00:00", "dt_upto": "2022-02-02T00:00:00", "group_type": "hour"}'
        )


@router.message(F.text)
async def wrong_request(message: Message):
    await message.answer(
        "Невалидный запрос. Пример запроса:"
        '{"dt_from": "2022-09-01T00:00:00", "dt_upto": '
        '"2022-12-31T23:59:00", "group_type": "month"})'
    )
