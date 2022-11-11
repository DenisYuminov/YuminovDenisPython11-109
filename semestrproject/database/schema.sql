DROP table if exists users;
DROP table if exists products;
DROP table if exists cart;
DROP table if exists profiles;
DROP TABLE if exists product_parameters;
DROP TABLE if exists favourite;
drop table if exists tags;
drop table if exists posts;
drop table if exists tags_to_post;
drop table if exists product_lists;
drop table if exists carts;
drop table if exists products;
drop table if exists offer;

create table users(
    id integer primary key autoincrement ,
    login varchar(20),
    password varchar(20)
);

create table profiles
(
    id integer primary key autoincrement ,
    username varchar,
    user_id not null,
    foreign key (user_id) references users (id)
);


create table posts(
    id integer primary key autoincrement,
    text varchar(300),
    photo varchar(30),
    uploaded date,
    user_id integer,
    foreign key (user_id) references users(id)
);


create table tags(
    id integer primary key autoincrement,
    name varchar(20)
);

create table tags_to_post(
    post_id integer,
    tag_id integer,
    foreign key (post_id) references posts(id),
        foreign key (tag_id) references tags(id)
)