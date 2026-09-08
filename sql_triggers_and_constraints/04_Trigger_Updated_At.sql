create trigger trg_accounts_updated_at
on accounts
after update
as
begin
    update a
    set a.updated_at = getdate()
    from accounts a
    join inserted i on a.account_id = i.account_id
end