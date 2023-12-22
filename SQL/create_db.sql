CREATE TABLE users
(
    user_id  SERIAL PRIMARY KEY,
    username VARCHAR(255)                                       NOT NULL,
    email    VARCHAR(255)                                       NOT NULL UNIQUE,
    passwd   VARCHAR(255)                                       NOT NULL,
    role     VARCHAR(255) CHECK (role IN ('admin', 'customer')) NOT NULL
);

CREATE TABLE category
(
    category_id SERIAL PRIMARY KEY,
    name        VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE product
(
    product_id    SERIAL PRIMARY KEY,
    name          VARCHAR(255)                            NOT NULL,
    price         DECIMAL(10, 2)                          NOT NULL,
    category_name VARCHAR(255) REFERENCES category (name) NOT NULL,
    description   TEXT
);


CREATE TABLE cart
(
    cart_id    SERIAL PRIMARY KEY,
    user_id    INT REFERENCES users (user_id) NOT NULL,
    created_at TIMESTAMP      DEFAULT CURRENT_TIMESTAMP,
    count      DECIMAL(10, 2) DEFAULT 0
);

CREATE TABLE cart_item
(
    cart_id    INT REFERENCES cart (cart_id)       NOT NULL,
    product_id INT REFERENCES product (product_id) NOT NULL,
    quantity   INT                                 NOT NULL,
    PRIMARY KEY (cart_id, product_id)
);

CREATE
OR REPLACE FUNCTION update_cart_count()
RETURNS TRIGGER AS $$
BEGIN
UPDATE cart
SET count = (SELECT COALESCE(SUM(p.price * ci.quantity), 0)
             FROM cart_item ci
                      JOIN product p ON ci.product_id = p.product_id
             WHERE ci.cart_id = NEW.cart_id)
WHERE cart_id = NEW.cart_id;

RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER cart_item_after_insert
    AFTER INSERT
    ON cart_item
    FOR EACH ROW
    EXECUTE FUNCTION update_cart_count();

CREATE INDEX idx_product_name ON product (name);


CREATE
OR REPLACE FUNCTION update_cart_count_on_delete()
RETURNS TRIGGER AS $$
BEGIN
UPDATE cart
SET count = (SELECT COALESCE(SUM(p.price * ci.quantity), 0)
             FROM cart_item ci
                      JOIN product p ON ci.product_id = p.product_id
             WHERE ci.cart_id = OLD.cart_id)
WHERE cart_id = OLD.cart_id;

RETURN OLD;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER cart_item_after_delete
    AFTER DELETE
    ON cart_item
    FOR EACH ROW
    EXECUTE FUNCTION update_cart_count_on_delete();



CREATE ROLE customer WITH LOGIN PASSWORD '123';

GRANT
CONNECT
ON DATABASE shop TO customer;
GRANT USAGE, CREATE
ON SCHEMA public TO customer;
GRANT
SELECT,
INSERT
,
UPDATE,
DELETE
ON ALL TABLES IN SCHEMA public TO customer;
GRANT
EXECUTE
ON
ALL
FUNCTIONS IN SCHEMA public TO customer;
GRANT USAGE,
SELECT
ON ALL SEQUENCES IN SCHEMA public TO customer;
