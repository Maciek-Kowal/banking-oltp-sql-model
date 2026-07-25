create table accounts (
account_id int primary key identity(1,1),
customer_id int not null,
account_type varchar(50) not null,
IBAN varchar(34) unique not null,
balance numeric(15,2) default(0.0) not null,
currency char(3) not null,
created_at datetime default(getdate()),
updated_at datetime default(getdate()),
status varchar(20) default('ACTIVE'),

constraint fk_customer_id
foreign key (customer_id)
references customers(customer_id),

constraint chk_account_type check(
account_type in ('CHECKING','SAVINGS','CREDIT')),

constraint chk_status check(
status in ('ACTIVE','BLOCKED','CLOSED'))

)