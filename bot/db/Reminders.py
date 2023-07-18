from dataclasses import dataclass
from collections import namedtuple
from .SQLite import Sqlite3_Database


class Reminder:
    def __init__(self, id, **kwargs):
        self.id: int = id
        if len(kwargs):
            self.tel_id = kwargs["tel_id"]
            self.text = kwargs["text"]
            self.date = kwargs["date"]
            self.answer_time = kwargs["answer_time"]
            self.send_message = bool(kwargs["send_message"])
            self.get_answer = bool(kwargs["get_answer"])
            self.message_id = kwargs["message_id"]

        else:
            self.tel_id = 0
            self.text = ""
            self.date = None
            self.answer_time = None
            self.send_message = False
            self.get_answer = False
            self.message_id = 0

    def __iter__(self):
        dict_class = self.__dict__
        result = namedtuple("result", ["name", "value"])
        for attr in dict_class:
            if not attr.startswith("__"):
                if attr != "flag":
                    yield result(attr, dict_class[attr])
                else:
                    yield result(attr, dict_class[attr].value)


class Reminders(Sqlite3_Database):
    def __init__(self, db_file_name, table_name, *args) -> None:
        Sqlite3_Database.__init__(self, db_file_name, table_name, *args)
        self.len = len(self.get_keys())

    def __len__(self):
        return self.len

    def add(self, obj: Reminder) -> None:
        self.add_row(obj)
        self.len += 1

    def __delitem__(self, key) -> None:
        self.del_instance(key)
        self.len -= 1

    def __iter__(self) -> Reminder:
        keys = self.get_keys()
        for id in keys:
            reminder = self.get(id)
            yield reminder

    def get(self, key: int) -> Reminder | bool:
        if key in self:
            obj_tuple = self.get_elem_sqllite3(key)
            obj = Reminder(
                id=obj_tuple[0],
                tel_id=obj_tuple[1],
                text=obj_tuple[2],
                date=obj_tuple[3],
                answer_time=obj_tuple[4],
                send_message=bool(obj_tuple[5]),
                get_answer=bool(obj_tuple[6]),
                message_id=obj_tuple[6],
            )
            return obj
        return False

    def get_by_tel_id(self, id: int):
        obj_tuple = self.get_by_other_field(id, field="tel_id", attr="*")[0]
        obj = Reminder(
            id=obj_tuple[0],
            tel_id=obj_tuple[1],
            text=obj_tuple[2],
            date=obj_tuple[3],
            answer_time=obj_tuple[4],
            send_message=bool(obj_tuple[5]),
            get_answer=bool(obj_tuple[6]),
            message_id=obj_tuple[6],
        )
        return obj

