CREATE
OR REPLACE FUNCTION view_users() RETURNS TABLE (
    user_id INT,
    username VARCHAR(255),
    email VARCHAR(255),
    passwd VARCHAR(255),
    role VARCHAR(255)
) AS
$$
BEGIN
RETURN QUERY SELECT * FROM users;
END;
$$
LANGUAGE plpgsql;



CREATE
OR REPLACE FUNCTION view_category() RETURNS TABLE (
    category_id INT,
    name VARCHAR(255)
) AS
$$
BEGIN
RETURN QUERY SELECT * FROM category;
END;
$$
LANGUAGE plpgsql;

CREATE
OR REPLACE FUNCTION view_product() RETURNS TABLE (
    product_id INT,
    name VARCHAR(255),
    price DECIMAL(10, 2),
    category_name VARCHAR(255),
    description TEXT
) AS
$$
BEGIN
RETURN QUERY SELECT * FROM product;
END;
$$
LANGUAGE plpgsql;

CREATE
OR REPLACE FUNCTION view_cart() RETURNS TABLE (
    cart_id INT,
    user_id INT,
    created_at TIMESTAMP,
    count DECIMAL(10,2)
) AS
$$
BEGIN
RETURN QUERY SELECT * FROM cart;
END;
$$
LANGUAGE plpgsql;

CREATE
OR REPLACE FUNCTION view_cart_item() RETURNS TABLE (
    cart_id INT,
    product_id INT,
    quantity INT
) AS
$$
BEGIN
RETURN QUERY SELECT * FROM cart_item;
END;
$$
LANGUAGE plpgsql;

CREATE
OR REPLACE PROCEDURE clear_table(IN table_name VARCHAR(255))
LANGUAGE plpgsql
AS $$
BEGIN
EXECUTE 'DELETE FROM ' || table_name;
END;
$$;

CREATE
OR REPLACE FUNCTION add_category(
    p_name VARCHAR(255)
) RETURNS VOID AS
$$
BEGIN
    IF
p_name IS NOT NULL AND p_name != '' THEN
        INSERT INTO category (name)
        VALUES (p_name);
ELSE
        RAISE EXCEPTION 'Category name cannot be empty';
END IF;
END;
$$
LANGUAGE plpgsql;

CREATE
OR REPLACE FUNCTION add_product(
    p_name VARCHAR(255),
    p_price DECIMAL(10, 2),
    p_category_name VARCHAR(255),
    p_description TEXT DEFAULT NULL
) RETURNS VOID AS
$$
BEGIN
    IF
p_name IS NOT NULL AND p_name != '' AND
       p_price IS NOT NULL AND
       p_category_name IS NOT NULL AND p_category_name != '' THEN
        INSERT INTO product (name, price, category_name, description)
        VALUES (p_name, p_price, p_category_name, p_description);
ELSE
        RAISE EXCEPTION 'Invalid product data';
END IF;
END;
$$
LANGUAGE plpgsql;


CREATE
OR REPLACE FUNCTION search_data(p_table_name VARCHAR, p_column_name VARCHAR, p_value VARCHAR) RETURNS TABLE (
    result_row JSON
) AS
$$
BEGIN
EXECUTE 'SELECT row_to_json(' || p_table_name || '.*)
             FROM ' || p_table_name || '
             WHERE ' || p_column_name || ' = $1'
    INTO STRICT result_row
    USING p_value;
RETURN
NEXT;
END;
$$
LANGUAGE plpgsql;

CREATE
OR REPLACE FUNCTION update_product(
    p_product_id INT,
    p_name VARCHAR(255),
    p_price DECIMAL(10, 2),
    p_category_name VARCHAR(255),
    p_description TEXT
) RETURNS VOID AS
$$
BEGIN
UPDATE product
SET name          = p_name,
    price         = p_price,
    category_name = p_category_name,
    description   = p_description
WHERE product_id = p_product_id;
END;
$$
LANGUAGE plpgsql;


CREATE
OR REPLACE FUNCTION delete_by_value(
    p_table_name VARCHAR,
    p_column_name VARCHAR,
    p_value VARCHAR
)
RETURNS VOID AS $$
BEGIN
EXECUTE format('DELETE FROM %I WHERE %I = %L', p_table_name, p_column_name, p_value);

RETURN;
END;
$$
LANGUAGE plpgsql;





