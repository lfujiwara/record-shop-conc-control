create table discs
(
    id              uuid    default gen_random_uuid() not null
        constraint discs_pk
            primary key,
    name            text                              not null,
    artist          text                              not null,
    year_of_release integer,
    genre           text                              not null,
    quantity        integer default 0                 not null
);

create table customers
(
    id         uuid    default gen_random_uuid() not null
        constraint customers_pk
            primary key,
    document   text                              not null,
    name       text                              not null,
    birth_date date                              not null,
    email      text                              not null,
    phone      text                              not null,
    is_active  boolean default true              not null
);

create table purchase_orders
(
    id            uuid default gen_random_uuid() not null
        constraint purchase_orders_pk
            primary key,
    customer_id   uuid                           not null
        constraint purchase_orders_customers_id_fk
            references customers
            on update cascade on delete cascade,
    disc_id       uuid                           not null
        constraint purchase_orders_discs_id_fk
            references discs
            on update cascade on delete cascade,
    quantity      integer                        not null,
    timestamp     timestamp                      not null,
    customer_json jsonb,
    disc_json     jsonb
);