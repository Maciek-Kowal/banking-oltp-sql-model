create trigger trg_updatebalance
on transactions
after insert
as
begin
    -- 1. zmniejszamy saldo nadawcy
    update a
    set a.balance = a.balance - i.amount
    from accounts a
    inner join inserted i on a.account_id = i.sender_account_id
    where i.status = 'COMPLETED' 
      and i.transaction_type in ('INTERNAL', 'EXTERNAL_OUT');

    -- 2. zwiekszamy saldo odbiorcy
    update a
    set a.balance = a.balance + i.amount
    from accounts a
    inner join inserted i on a.account_id = i.receiver_account_id
    where i.status = 'COMPLETED' 
      and i.transaction_type in ('INTERNAL', 'EXTERNAL_IN');
end