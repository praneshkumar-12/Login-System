create database test;
use test;
create table login_details(
	username varchar(35) NOT NULL PRIMARY KEY,
    passphrase varchar(25),
    f_name varchar(40),
    l_name varchar(40),
    email varchar(40)
);
insert into login_details values(
	'admin',
    'admin',
    'admin',
    'admin',
    'admin@example.com'
);
use test;
select * from login_details;