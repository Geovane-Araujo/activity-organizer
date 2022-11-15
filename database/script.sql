CREATE TABLE IF NOT EXISTS users(
    id CHAR(36) primary key,
    name varchar(70),
    email varchar(70),
    password varchar(50),
    status smallint
);

CREATE TABLE IF NOT EXISTS activity(
    id CHAR(36) primary key,
    id_user CHAR(36),
    data timestamp,
    title varchar(70),
    description text,
    status smallint
);