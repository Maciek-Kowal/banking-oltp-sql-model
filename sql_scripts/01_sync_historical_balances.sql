with money_movements as (
    select sender_account_id as account_id, -amount as value
    from transactions
    where sender_account_id is not null 
      and status = 'COMPLETED'
      
    union all
    
    select receiver_account_id as account_id, amount as value
    from transactions
    where receiver_account_id is not null 
      and status = 'COMPLETED'
),
calculated_balances as (
    select account_id, sum(value) as final_balance
    from money_movements
    group by account_id
)
update a
set a.balance = isnull(cb.final_balance, 0)
from accounts a
left join calculated_balances cb on a.account_id = cb.account_id