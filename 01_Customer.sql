create table customers (
customer_id int primary key identity(1,1),
parent_company_id int,
customer_type varchar(30),
first_name varchar(50),
middle_name varchar(50),
last_name varchar(50),
national_id varchar(11),
birth_date date,
company_name varchar(255),
tax_id varchar(10),
country varchar(50) not null,
state_province varchar(50) not null,
county varchar(50) not null,
municipality varchar(50) not null,
city varchar(50) not null,
postal_code varchar(6) not null,
street varchar(50) not null,
house_number varchar(10) not null,
apartment_number varchar(10),
phone_number varchar(15) not null,
email varchar(255) not null,
is_active bit default(1),
kyc_status varchar(20) default('pending'),
created_at datetime default(getdate()),
updated_at datetime default(getdate()),

constraint fk_parent_company_id
foreign key (parent_company_id)
references customers(customer_id),

constraint chk_customer_data check (
    (
        customer_type = 'retail' 
        and first_name is not null 
        and last_name is not null
        and national_id is not null
    )
    or
    (
        customer_type = 'corporate' 
        and company_name is not null
        and tax_id is not null
    )
),

constraint chk_customer_type check (customer_type in ('retail', 'corporate'))

)
