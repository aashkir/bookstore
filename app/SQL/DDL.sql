drop table if exists user;
drop table if exists owner;
drop table if exists customer;
drop table if exists orders;
drop table if exists genre;
drop table if exists book;
drop table if exists publisher;
drop table if exists banking_account;
drop table if exists author;
drop table if exists warehouse;
drop table if exists phone_number;
drop table if exists joins;
drop table if exists book_publisher;
drop table if exists book_genre;
drop table if exists stocks;
drop table if exists writes;
drop table if exists warehouse_phone;
drop table if exists author_phone;
drop table if exists publisher_phone;

create table user (
	id integer primary key autoincrement,
    username text unique not null,
    name text not null,
    shipping_info text not null,
    billing_info text not null
);

create table owner (
    id integer primary key,
    foreign key (id) references user (id)
);

create table customer (
    id integer primary key,
    foreign key (id) references user (id)
);

create table orders (
    order_number integer primary key autoincrement,
    user_id integer not null,
    ship_to text not null,
    bill_to text not null,
    date text not null,
    foreign key (user_id) references user (id)
);

create table book (
    ISBN integer primary key,
    title text,
    num_pages integer,
    price real
);

create table genre (
    genre text primary key
);

create table publisher (
    name text primary key,
    address text,
    email text,
    banking_account integer not null,
    foreign key (banking_account) references banking_account (id)
);

create table banking_account (
    id integer primary key autoincrement,
    real received
);

create table author (
    name text primary key,
    address text,
    email text
);

create table warehouse (
    hub_number integer primary key,
    address text
);

create table phone_number (
    phone_number text primary key,
    area integer
);

create table joins (
    ISBN integer not null,
    order_number integer not null,
    number_bought integer,
    foreign key (ISBN) references book (ISBN),
    foreign key (order_number) references orders (order_number),
    primary key (ISBN, order_number)
);

create table book_publisher (
    name text not null,
    ISBN integer not null,
    publishers_cut real,
    foreign key (ISBN) references book (ISBN),
    foreign key (name) references publisher (name),
    primary key (ISBN)
);

create table book_genre (
    genre text not null,
    ISBN integer not null,
    foreign key (ISBN) references book (ISBN),
    foreign key (genre) references genre (genre)
    primary key (genre, ISBN)
);

create table stocks (
    hub_number integer not null,
    ISBN integer not null,
    number_books integer,
    foreign key (hub_number) references warehouse (hub_number),
    foreign key (ISBN) references book (ISBN),
    primary key (ISBN)
);

create table writes (
    name text not null,
    ISBN integer not null,
    foreign key (name) references author (name),
    foreign key (ISBN) references book (ISBN),
    primary key (ISBN, name)
);

create table warehouse_phone (
    phone_number text primary key,
    hub_number text not null,
    foreign key (phone_number) references phone_number (phone_number),
    foreign key (hub_number) references warehouse (hub_number)
);

create table author_phone (
    phone_number text primary key,
    name text not null,
    foreign key (phone_number) references phone_number (phone_number),
    foreign key (name) references author (name)
);

create table publisher_phone (
    phone_number text primary key,
    name text not null,
    foreign key (phone_number) references phone_number (phone_number),
    foreign key (name) references publisher (name)
)

