create trigger trg_prevent_overdraft
on transactions
after insert
as
begin
    if exists (
        select 1
        from accounts a
        inner join inserted i on a.account_id = i.sender_account_id
        where (a.balance - i.amount) < 0
          and i.transaction_type in ('INTERNAL', 'EXTERNAL_OUT')
    )
    begin
        raiserror('niewystarczajace srodki na koncie. transakcja odrzucona.', 16, 1)
        rollback transaction
        return
    end
end