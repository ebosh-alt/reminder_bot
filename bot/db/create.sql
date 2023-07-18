create table reminders(
    id int primary key,
    tel_id int not null,
    text text not null,
    date datetime not null,
    answer_time datetime not null,
    send_message bool default false,
    get_answer bool default false,
    message_id int not null
);

