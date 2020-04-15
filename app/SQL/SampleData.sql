delete from user;
delete from owner;
delete from customer;
delete from orders;
delete from book;
delete from publisher;
delete from banking_account;
delete from author;
delete from warehouse;
delete from phone_number;
delete from joins;
delete from book_publisher;
delete from stocks;
delete from writes;
delete from warehouse_phone;
delete from author_phone;
delete from publisher_phone;

/* manually adding the admin here */
insert into user (username, name, shipping_info, billing_info) values ("Admin", "John Smith", "123 bayshore", "321 dungstreet");
insert into owner (id) values ("1");

insert into book (ISBN, title, num_pages, price) values (9780439023481, "The Hunger Games", 374, 14.99);

insert into book (ISBN, title, num_pages, price) values (9780439554930, "Harry Potter and the Philosopher's Stone", 500, 18.99);