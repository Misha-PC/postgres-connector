CREATE TABLE public.sources
(
	id serial,
    name text,
    url text,
    context text,
    PRIMARY KEY (id)

);


ALTER TABLE public.sources
	OWNER to postgres;

CREATE TABLE users (
	id Serial,
	join_date date,
    tg_id varchar(10),
	PRIMARY KEY (id)
);


CREATE TABLE public.subscription
(
    id serial,
    source_id int,
    user_id int,
    date date,
    PRIMARY KEY (id),

	CONSTRAINT fk_source FOREIGN KEY (source_id)
	REFERENCES public.sources (id)MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE
    NOT VALID,

	CONSTRAINT fk_users FOREIGN KEY (user_id)
    REFERENCES public.users (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE
    NOT VALID
);

ALTER TABLE public.subscription
    OWNER to postgres;
