create table transactions (
transaction_id int primary key identity(1,1),
sender_account_id int,
sender_iban varchar(34) not null,
receiver_account_id int,
receiver_iban varchar(34) not null,
amount numeric(15,2) not null,
transaction_date datetime default(getdate()),
status varchar(50) not null default('PENDING'),
transaction_type varchar(50) not null
)