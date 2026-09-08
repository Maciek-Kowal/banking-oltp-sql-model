alter table accounts
add is_active bit not null default 1
go
create trigger trg_soft_delete_customers
on customers
instead of delete
as
begin
    update c
    set c.is_active = 0
    from customers c
    join deleted d on c.customer_id = d.customer_id
end
go

create trigger trg_soft_delete_accounts
on accounts
instead of delete
as
begin
    update a
    set a.is_active = 0
    from accounts a
    join deleted d on a.account_id = d.account_id
end
go