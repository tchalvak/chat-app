CREATE TABLE chat (
    chat_id serial,
    account_id integer DEFAULT 0 references accounts(account_id),
    chat character varying(255) NOT NULL,
    date_created timestamp with time zone DEFAULT now() NOT NULL
);
