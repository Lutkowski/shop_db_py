import psycopg2


class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="shop",
            user='customer',
            password='123',
            host="localhost",
            port="5432"
        )
        self.cur = self.conn.cursor()
        self.schema = database_schema = {
            'users': ['user_id', 'username', 'email', 'passwd', 'role'],
            'category': ['category_id', 'name'],
            'product': ['product_id', 'name', 'price', 'category_name', 'description'],
            'cart': ['cart_id', 'user_id', 'created_at', 'count'],
            'cart_item': ['cart_id', 'product_id', 'quantity']
        }

    def get_table_names(self):
        return self.schema.keys()

    def get_table_columns(self, table_name):
        return self.schema[table_name]

    def execute_sql_file(self, file_path):
        with open(file_path, 'r') as file:
            sql_script = file.read()
            self.cur.execute(sql_script)
            self.conn.commit()

    def authenticate_user(self, email, password):
        self.cur.execute("SELECT authenticate_user(%s, %s)", (email, password))
        return self.cur.fetchone()[0]

    def register_user(self, username, email, password, role):
        try:
            self.cur.execute("SELECT register_user(%s, %s, %s, %s)", (username, email, password, role))
            self.conn.commit()
        except Exception as e:
            print(e)

    def view_users(self):
        self.cur.execute("SELECT * FROM view_users()")
        return self.cur.fetchall()

    def view_category(self):
        self.cur.execute("SELECT * FROM view_category()")
        return self.cur.fetchall()

    def view_product(self):
        self.cur.execute("SELECT * FROM view_product()")
        return self.cur.fetchall()

    def view_cart(self):
        self.cur.execute("SELECT * FROM view_cart()")
        return self.cur.fetchall()

    def view_cart_item(self):
        self.cur.execute("SELECT * FROM view_cart_item()")
        return self.cur.fetchall()

    def clear_table(self, table_name):
        self.cur.execute("CALL clear_table(%s)", (table_name,))
        self.conn.commit()

    def add_category(self, name):
        try:
            self.cur.execute("SELECT add_category(%s)", (name,))
            self.conn.commit()
        except Exception as e:
            print(f"Error adding category: {e}")

    def add_product(self, name, price, category, description=None):
        try:
            self.cur.execute("SELECT add_product(%s, %s, %s, %s)",
                             (name, price, category, description))
            self.conn.commit()
        except Exception as e:
            print(f"Error adding product: {e}")

    def search_data(self, table_name, column, value):
        try:
            self.cur.execute("SELECT * FROM search_data(%s, %s, %s)", (table_name, column, value))
            return self.cur.fetchall()
        except Exception as e:
            print(f"Error searching data: {e}")
            return []

    def update_product(self, product_id, name, price, category_name, description):
        try:
            self.cur.execute("SELECT update_product(%s, %s, %s, %s, %s)",
                             (product_id, name, price, str(category_name), description))
            self.conn.commit()
            print(f"Product with ID {product_id} updated successfully.")
        except Exception as e:
            print(f"Error updating product: {e}")

    def delete_by_value(self, table_name, column_name, value):
        try:
            self.cur.execute("SELECT delete_by_value(%s, %s, %s)", (table_name, column_name, value))
            self.conn.commit()
            print(f"Rows with {column_name} = {value} deleted successfully from {table_name}.")
        except Exception as e:
            print(f"Error deleting rows: {e}")

    def get_user_id_by_email(self, email):
        try:
            self.cur.execute("SELECT get_user_id_by_email(%s)", (email,))
            result = self.cur.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Error getting user_id by email: {e}")
            return None

    def get_cart_id_by_user_id(self, user_id):
        try:
            self.cur.execute("SELECT get_cart_id_by_user_id(%s)", (user_id,))
            result = self.cur.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Error getting cart_id: {e}")
            return None

    def add_to_cart(self, cart_id, product_id, quantity=1):
        try:
            if cart_id is not None:
                self.cur.execute("SELECT add_to_cart_item(%s, %s, %s)", (cart_id, product_id, quantity))
                self.conn.commit()
                print(f"Product with ID {product_id} added to cart successfully.")
            else:
                print("Error: User has no cart.")
        except Exception as e:
            print(f"Error adding product to cart: {e}")

    def get_cart_items(self, cart_id):
        try:
            self.cur.execute("SELECT * FROM get_cart_items(%s);", (cart_id,))

            cart_items = self.cur.fetchall()

            return cart_items
        except Exception as e:
            print(f"Error getting cart items: {e}")
            return []

    def delete_from_cart(self, cart_id, product_id):
        try:
            self.cur.execute("SELECT delete_from_cart_item(%s, %s)", (cart_id, product_id))
            self.conn.commit()
        except Exception as e:
            raise RuntimeError(f"Error deleting product from cart: {e}")

    def get_cart_count(self, cart_id):
        try:
            self.cur.execute("SELECT get_cart_count(%s)", (cart_id,))
            result = self.cur.fetchone()

            return result[0] if result else None
        except Exception as e:
            print(f"Error getting cart count: {e}")
            return None

    def close_connection(self):
        self.cur.close()
        self.conn.close()
