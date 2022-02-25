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
