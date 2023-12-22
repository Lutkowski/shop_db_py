CREATE
OR REPLACE FUNCTION register_user(
    p_username VARCHAR(255),
    p_email VARCHAR(255),
    p_passwd VARCHAR(255),
    p_role VARCHAR(255)
) RETURNS VOID AS
$$
DECLARE
id INT;
BEGIN
INSERT INTO users (username, email, passwd, role)
VALUES (p_username, p_email, p_passwd, p_role) RETURNING user_id
INTO id;

INSERT INTO cart (user_id)
VALUES (id);
END;
$$
LANGUAGE plpgsql;





CREATE
OR REPLACE FUNCTION authenticate_user(
    p_email VARCHAR(255),
    p_passwd VARCHAR(255)
) RETURNS BOOLEAN AS
$$
DECLARE
user_exists BOOLEAN;
BEGIN
SELECT EXISTS (SELECT 1
               FROM users
               WHERE email = p_email
                 AND passwd = p_passwd)
INTO user_exists;

RETURN user_exists;
END;
$$
LANGUAGE plpgsql;

CREATE
OR REPLACE FUNCTION get_user_id_by_email(p_email VARCHAR(255)) RETURNS INT AS
$$
DECLARE
v_user_id INT;
BEGIN
SELECT user_id
INTO v_user_id
FROM users
WHERE email = p_email;

RETURN v_user_id;
END;
$$
LANGUAGE plpgsql;


CREATE
OR REPLACE FUNCTION get_cart_id_by_user_id(p_user_id INT) RETURNS INT AS
$$
DECLARE
cart_i INT;
BEGIN
SELECT cart_id
INTO cart_i
FROM cart
WHERE user_id = p_user_id;

RETURN cart_i;
END;
$$
LANGUAGE plpgsql;

CREATE
OR REPLACE FUNCTION add_to_cart_item(p_cart_id INT, p_product_id INT, p_quantity INT)
RETURNS VOID AS $$
BEGIN
INSERT INTO cart_item (cart_id, product_id, quantity)
VALUES (p_cart_id, p_product_id, p_quantity) ON CONFLICT (cart_id, product_id) DO
UPDATE
    SET quantity = cart_item.quantity + p_quantity;
END;
$$
LANGUAGE plpgsql;

CREATE
OR REPLACE FUNCTION get_cart_items(p_cart_id INT) RETURNS TABLE (
    product_id INT,
    product_name VARCHAR(255),
    price DECIMAL(10, 2),
    quantity INT
) AS $$
BEGIN
RETURN QUERY
SELECT ci.product_id,
       p.name AS product_name,
       p.price,
       ci.quantity
FROM cart_item ci
         JOIN product p ON ci.product_id = p.product_id
WHERE ci.cart_id = p_cart_id;
END;
$$
LANGUAGE plpgsql;


CREATE
OR REPLACE FUNCTION delete_from_cart_item(p_cart_id INT, p_product_id INT) RETURNS VOID AS
$$
BEGIN
DELETE
FROM cart_item
WHERE cart_id = p_cart_id
  AND product_id = p_product_id;
END;
$$
LANGUAGE plpgsql;

CREATE
OR REPLACE FUNCTION get_cart_count(p_cart_id INT)
RETURNS DECIMAL(10, 2) AS
$$
DECLARE
v_count DECIMAL(10, 2);
BEGIN

SELECT count
INTO v_count
FROM cart
WHERE cart_id = p_cart_id;

RETURN v_count;
END;
$$
LANGUAGE plpgsql;