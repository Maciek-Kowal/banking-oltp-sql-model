create table transactions (
transaction_id int primary key identity(1,1),
sender_account_id int,
sender_iban varchar(34) not null,
receiver_account_id int,
receiver_iban varchar(34) not null,
amount numeric(15,2) not null,
transaction_date datetime default(getdate()),
status varchar(50) not null default('PENDING'),
transaction_type varchar(50) not null,

constraint fk_sender_account
foreign key (sender_account_id)
references accounts(account_id),

constraint fk_receiver_account
foreign key (receiver_account_id)
references accounts(account_id),

constraint chk_transaction_amount check (amount > 0),

constraint chk_transaction_status check (
    status in ('PENDING', 'COMPLETED', 'FAILED', 'REJECTED', 'CANCELLED')
),

constraint chk_transaction_type check (
    transaction_type in ('INTERNAL', 'EXTERNAL_IN', 'EXTERNAL_OUT')
)
)