CREATE TABLE IF NOT EXISTS users(
    id CHAR(36) primary key,
    name varchar(70),
    email varchar(70),
    password varchar(50),
    status smallint
);

alter table users
    add constraint uk_email
        unique (email);

CREATE TABLE IF NOT EXISTS activity(
    id CHAR(36) primary key,
    id_user CHAR(36),
    data datetime,
    title varchar(70),
    description text,
    status smallint
);

CREATE TABLE IF NOT EXISTS note(
    id CHAR(36) primary key,
    id_user CHAR(36),
    title varchar(70),
    description text,
    created_date datetime
);
