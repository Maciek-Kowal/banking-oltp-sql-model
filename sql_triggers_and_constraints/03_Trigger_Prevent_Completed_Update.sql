create trigger trg_prevent_completed_update
on transactions
after update
as
begin
    if exists (
        select 1 
        from deleted 
        where status = 'COMPLETED'
    )
    begin
        raiserror('nie mozna modyfikowac zaksiegowanych transakcji.', 16, 1)
        rollback transaction
        return
    end
end