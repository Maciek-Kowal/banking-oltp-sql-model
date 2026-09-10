create table audit_logs (
    log_id int identity(1,1) primary key,
    table_name varchar(50) not null,
    record_id int not null,
    column_name varchar(50) not null,
    old_value varchar(255) not null,
    new_value varchar(255) not null,
    changed_at datetime not null default getdate()
)