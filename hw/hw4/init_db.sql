drop table if exists products;
create table products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uploaded TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    name varchar(30) NOT NULL,
    description varchar(200) NOT NULL,
    price int NOT NULL
)