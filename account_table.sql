CREATE TABLE accounts (
    account_id serial,
    display_name varchar(100),
    phash text,
    active_email text,
    created_date timestamp with time zone DEFAULT now() NOT NULL,
    PRIMARY KEY (account_id)
);