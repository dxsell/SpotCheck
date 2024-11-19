drop table if exists accounts, passwords, reviews;

create table accounts(
    userID int primary key not null,
    username varchar(20)
);

create table passwords(
    pass varchar(25),
    userID int,
    FOREIGN KEY (userID) REFERENCES accounts(userID)
);

create table reviews(
    reviewID int primary key,
    review int
);

insert into accounts(userID, username) 
values 
    (1, 'Jerry');
insert into passwords(userID, pass) values (1, 'Jerry123');
SELECT * FROM accounts, passwords