create table discs
(
    id              uuid    default gen_random_uuid() not null
        constraint discs_pk
            primary key,
    name            text                              not null,
    artist          text                              not null,
    year_of_release text,
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
