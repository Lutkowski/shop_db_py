import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class UserPanel:
    def __init__(self, database, user_id):
        self.db = database
        self.user_id = user_id
        self.cart_id = self.db.get_cart_id_by_user_id(user_id)
        self.root = tk.Tk()
        self.root.title("User Panel")

        self.product_frame = ttk.Frame(self.root)
        self.product_frame.pack()

        self.cart_count_var = tk.StringVar()
        self.cart_count_var.set("Cart Count: " + str(self.db.get_cart_count(self.cart_id)))

        cart_count_label = tk.Label(self.root, textvariable=self.cart_count_var, font=("Arial", 10, "italic"))
        cart_count_label.pack(side=tk.RIGHT, padx=10, pady=10)

        view_cart_button = ttk.Button(self.root, text="View cart", command=self.view_cart)
        view_cart_button.pack(side=tk.RIGHT, padx=10, pady=10)

        self.load_products()

    def load_products(self):
        products = self.db.view_product()

        for widget in self.product_frame.winfo_children():
            widget.destroy()

        for product in products:
            product_block = tk.Frame(self.product_frame, padx=10, pady=10, relief=tk.GROOVE, borderwidth=2)
            product_block.grid(row=products.index(product) // 4, column=products.index(product) % 4, padx=10, pady=10)

            # Название продукта
            label_name = tk.Label(product_block, text=product[1], font=("Arial", 12, "bold"))
            label_name.pack()

            # Цена продукта
            label_price = tk.Label(product_block, text=f"Price: ${product[2]:.2f}", font=("Arial", 10))
            label_price.pack()

            # Категория продукта
            label_category = tk.Label(product_block, text=f"Category: {product[3]}", font=("Arial", 10))
            label_category.pack()

            # Описание продукта
            if product[4]:
                label_description = tk.Label(product_block, text=f"Description: {product[4]}",
                                             font=("Arial", 10, "italic"))
                label_description.pack()

            # Ввод количества
            quantity_entry = ttk.Entry(product_block, width=5)
            quantity_entry.insert(0, "1")
            quantity_entry.pack()

            add_to_cart_button = ttk.Button(product_block, text="Add to Cart",
                                            command=lambda p=product, q=quantity_entry: self.add_to_cart(p, q))
            add_to_cart_button.pack()

    def add_to_cart(self, product, quantity_entry):
        try:
            product_id = product[0]

            quantity = int(quantity_entry.get())


            self.db.add_to_cart(self.cart_id, product_id, quantity=quantity)

            self.cart_count_var.set("Cart Count: " + str(self.db.get_cart_count(self.cart_id)))

            messagebox.showinfo("Success", f"{quantity} {product[1]} added to cart successfully.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid quantity.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def view_cart(self):
        # Новое окно для корзины
        cart_window = tk.Toplevel(self.root)
        cart_window.title("Cart")

        cart_items = self.db.get_cart_items(self.cart_id)

        for cart_item in cart_items:
            product_id, product_name, price, quantity = cart_item

            product_frame = ttk.Frame(cart_window, padding=(10, 10), relief=tk.GROOVE, borderwidth=2)
            product_frame.pack(padx=10, pady=10, fill=tk.X)

            # Название продукта
            label_name = tk.Label(product_frame, text=f"Product: {product_name}", font=("Arial", 12, "bold"))
            label_name.pack(anchor=tk.W)

            # Цена продукта
            label_price = tk.Label(product_frame, text=f"Price: ${price:.2f}", font=("Arial", 10))
            label_price.pack(anchor=tk.W)

            # Количество продукта
            label_quantity = tk.Label(product_frame, text=f"Quantity: {quantity}", font=("Arial", 10))
            label_quantity.pack(anchor=tk.W)

            delete_button = ttk.Button(product_frame, text="Удалить",
                                       command=lambda p=product_id: self.delete_from_cart(p))
            delete_button.pack(anchor=tk.W)

        if not cart_items:
            empty_label = tk.Label(cart_window, text="Your cart is empty.", font=("Arial", 12, "italic"))
            empty_label.pack(pady=20)

    def delete_from_cart(self, product_id):
        try:
            self.db.delete_from_cart(self.cart_id, product_id)

            # Обновление суммы заказа
            self.cart_count_var.set("Cart Count: " + str(self.db.get_cart_count(self.cart_id)))
            self.view_cart()

            messagebox.showinfo("Success", "Product deleted from cart successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run(self):
        self.root.mainloop()
