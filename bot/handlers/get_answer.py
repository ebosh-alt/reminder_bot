from aiogram import Router
from aiogram.methods import SendMessage, DeleteMessage
from aiogram.types import CallbackQuery
from bot.config import id_manager
from bot.db import reminders

router = Router()


@router.callback_query(lambda call: "complete_" in call.data)
async def start(call: CallbackQuery):
    id = call.from_user.id
    await DeleteMessage(chat_id=id, message_id=call.message.message_id)
    if "no_complete" in call.data:
        await SendMessage(chat_id=id_manager, text=f"Пользователь {id} не выполнил")
    else:
        await SendMessage(chat_id=id_manager, text=f"Пользователь {id} выполнил")
    reminder = reminders.get_by_tel_id(id)
    reminder.get_answer = True
    reminders.update(reminder)

main_menu = router
