from .Reminders import Reminders, Reminder
db_file_name = "D:/telegram_bots/reminder_bot/bot/db/database"
reminders = Reminders(db_file_name=db_file_name, table_name="reminders")

__all__ = ('reminders', 'Reminders', 'Reminder')
