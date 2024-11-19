-- database: accounts.db
drop table if exists passwords, usernames, reviews;

create table if not exists passwords(
    pass varchar(25) not NULL
);

create table if not EXISTS accounts(
    userID int primary key,
    uname varchar(50) not NULL,
    email varchar(50) not NULL
);

create table if not exists reviews(
    reviewID int primary KEY,
    rating int,
    foreign key (uname) REFERENCES accounts(uname),
    reviewLocation varchar(50)
);