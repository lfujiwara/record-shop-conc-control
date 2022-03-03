TRUNCATE public.customers CASCADE;
INSERT INTO public.customers (id, document, name, birth_date, email, phone, is_active)
VALUES ('0e92cf1e-7bc4-4f9e-8eb6-3c88627efecb', '12345678911', 'John Doe', '2000-01-01', 'johndoe@gmail.com',
        '5511123456789',
        true);

TRUNCATE public.discs CASCADE;
INSERT INTO public.discs (id, name, artist, year_of_release, genre, quantity)
VALUES ('bcd8a0e9-dc0a-4ae7-a783-458542e2cc39', 'We are Reactive', 'Hohpe', 2022, 'Indie', 500);

TRUNCATE public.purchase_orders CASCADE;