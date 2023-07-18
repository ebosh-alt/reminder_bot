import time
from asyncio import run
from contextlib import suppress
from multiprocessing import Process
import datetime

import gspread
from aiogram.methods import SendMessage
from bot.keyboards import create_keyboard
from bot.db import reminders, Reminder
from bot.config import path_to_file_by_google, bot, id_manager


class BackGroundProcess:
    def __init__(self) -> None:
        self.p0 = Process()

    def start_process(self, func, arg=None):
        if arg is not None:
            self.p0 = Process(target=func, args=(arg,))
        else:
            self.p0 = Process(target=func)
        self.p0.start()

    def stop_process(self):
        self.p0.terminate()


class GetSheet(BackGroundProcess):
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def auth() -> gspread.Client:
        gc = gspread.service_account(filename=path_to_file_by_google)
        return gc

    def get_data(self) -> list:
        gc = self.auth()
        wks = gc.open("test").sheet1.get_all_values()
        return wks

    def pars(self):
        data = self.get_data()
        for id_row in range(0, len(data)):
            row = data[id_row]
            if len(row) == 5:
                tel_id = row[0]
                text = row[1]
                date = datetime.datetime.strptime(row[2], "%d.%m.%Y") + datetime.timedelta(
                    hours=int(row[3].split(":")[0]),
                    minutes=int(row[3].split(":")[1]))

                answer_time = date + datetime.timedelta(hours=int(row[4].split(":")[0]),
                                                        minutes=int(row[4].split(":")[1]))
                if id_row not in reminders:
                    reminder = Reminder(id=id_row,
                                        tel_id=tel_id,
                                        text=text,
                                        date=date,
                                        answer_time=answer_time,
                                        send_message=False,
                                        get_answer=False,
                                        message_id=0
                                        )
                    reminders.add(reminder)
                # else:
                #     reminder = reminders.get(id_row)
                #     reminder.tel_id = tel_id
                #     reminder.text = text
                #     reminder.date = date
                #     reminder.answer_time = answer_time
                #     reminder.send_message =
                #     reminder.get_answer =
                #     reminder.message_id = 0
                #     reminders.update(reminder)

    def start_schedule(self):
        while True:
            self.pars()
            time.sleep(5)


class SendReminder(BackGroundProcess):
    def __init__(self):
        super().__init__()

    @staticmethod
    async def send_reminder():
        date_now = datetime.datetime.now()
        for reminder in reminders:
            if datetime.datetime.strptime(reminder.date, "%Y-%m-%d %H:%M:%S") <= date_now and not reminder.send_message:
                mes = await bot.send_message(
                    chat_id=reminder.tel_id,
                    text=reminder.text,
                    reply_markup=create_keyboard({
                        "выполнено": f"complete_{reminder.tel_id}",
                        "не сделано": f"no_complete_{reminder.tel_id}"
                    }))

                reminder.send_message = True
                reminder.message_id = mes.message_id
                await bot.session.close()


            if datetime.datetime.strptime(reminder.answer_time,
                                          "%Y-%m-%d %H:%M:%S") <= date_now and not reminder.get_answer:
                await bot.delete_message(chat_id=reminder.tel_id,
                                         message_id=reminder.message_id)
                await bot.send_message(
                    chat_id=id_manager,
                    text=f"Пользователь {reminder.tel_id} не ответил",
                )
                reminder.get_answer = True
                await bot.session.close()
            reminders.update(reminder)

    def start_schedule(self):
        while True:
            run(self.send_reminder())
            time.sleep(5)


if __name__ == '__main__':
    with suppress(KeyboardInterrupt):
        parser = GetSheet()
        sender = SendReminder()
        parser.start_process(func=parser.start_schedule)
        sender.start_process(func=sender.start_schedule)
