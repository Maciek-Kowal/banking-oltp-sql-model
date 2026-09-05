alter table accounts
add constraint chk_valid_iban check (dbo.sprawdziban_kazdykraj(IBAN) = 1)