import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class AdminPanel:
    def __init__(self, database):
        self.db = database
        self.root = tk.Tk()
        self.root.title("Admin Panel")

        btn_view_users = tk.Button(self.root, text="View Users",
                                   command=lambda: self.show_results("View Users", self.db.view_users()))
        btn_view_users.grid(row=0, column=0, padx=5, pady=5)

        btn_view_category = tk.Button(self.root, text="View Category",
                                      command=lambda: self.show_results("View Category", self.db.view_category()))
        btn_view_category.grid(row=0, column=1, padx=5, pady=5)

        btn_view_product = tk.Button(self.root, text="View Product",
                                     command=lambda: self.show_results("View Product", self.db.view_product()))
        btn_view_product.grid(row=0, column=2, padx=5, pady=5)

        btn_view_cart = tk.Button(self.root, text="View Cart",
                                  command=lambda: self.show_results("View Cart", self.db.view_cart()))
        btn_view_cart.grid(row=1, column=0, padx=5, pady=5)

        btn_view_cart_item = tk.Button(self.root, text="View Cart Item",
                                       command=lambda: self.show_results("View Cart Item", self.db.view_cart_item()))
        btn_view_cart_item.grid(row=1, column=1, padx=5, pady=5)

        # Кнопки для очистки таблиц
        btn_clear_table = tk.Button(self.root, text="Clear Table", command=self.clear_table)
        btn_clear_table.grid(row=1, column=2, padx=5, pady=5)

        btn_clear_all = tk.Button(self.root, text="Clear All Tables", command=self.clear_all_tables)
        btn_clear_all.grid(row=2, column=0, padx=5, pady=5)

        # Остальные кнопки
        btn_add_category = tk.Button(self.root, text="Add Category", command=self.show_add_category_form)
        btn_add_category.grid(row=2, column=1, padx=5, pady=5)

        btn_add_product = tk.Button(self.root, text="Add Product", command=self.show_add_product_form)
        btn_add_product.grid(row=2, column=2, padx=5, pady=5)

        btn_search = tk.Button(self.root, text="Search", command=self.search_data)
        btn_search.grid(row=3, column=0, padx=5, pady=5)

        btn_update_product = tk.Button(self.root, text="Update Product", command=self.show_update_product_form)
        btn_update_product.grid(row=3, column=1, padx=5, pady=5)

        btn_delete_row = tk.Button(self.root, text="Delete Row", command=self.show_delete_row_form)
        btn_delete_row.grid(row=3, column=2, padx=5, pady=5)

        # Select
        self.table_var = tk.StringVar(self.root)
        table_names = ("users", "category", "product", "cart", "cart_item")
        self.table_var.set(table_names[0] if table_names else "")
        table_select = ttk.Combobox(self.root, textvariable=self.table_var, values=table_names)
        table_select.grid(row=4, column=0, padx=5, pady=5)

    def clear_all_tables(self):
        table_names = ("cart_item", "cart", "users", "product", "category")
        for name in table_names:
            self.db.clear_table(name)

        messagebox.showinfo("Tables Cleared", "All tables have been cleared.")

    def clear_table(self):
        table_name = self.table_var.get()
        if not table_name:
            messagebox.showerror("Error", "Please select a table to clear.")
            return

        confirmed = messagebox.askyesno("Confirmation", f"Are you sure you want to clear the table '{table_name}'?")
        if confirmed:
            self.db.clear_table(table_name)
            messagebox.showinfo("Table Cleared", f"The table '{table_name}' has been cleared.")
        else:
            messagebox.showinfo("Operation Cancelled", "Table clearing operation has been cancelled.")

    def show_results(self, title, data):
        # Новое окно для результатов
        result_window = tk.Toplevel(self.root)
        result_window.title(title)

        if data:
            column_names = [desc[0] for desc in self.db.cur.description]

            # Таблица результатов
            tree = ttk.Treeview(result_window, columns=column_names, show="headings")
            # Заголовки столбцов
            for field in column_names:
                tree.heading(field, text=field.capitalize())

            for row in data:
                tree.insert("", "end", values=row)

            tree.pack()
        else:
            messagebox.showinfo("No Data", "No data available for display.")

    def show_add_category_form(self):
        add_category_window = tk.Toplevel(self.root)
        add_category_window.title("Add Category")

        label_name = tk.Label(add_category_window, text="Category Name:")
        label_name.pack()

        entry_name = tk.Entry(add_category_window)
        entry_name.pack()

        btn_add_category = tk.Button(add_category_window, text="Add",
                                     command=lambda: self.add_category(entry_name.get(), add_category_window))
        btn_add_category.pack()

    def show_add_product_form(self):
        add_product_window = tk.Toplevel(self.root)
        add_product_window.title("Add Product")

        label_name = tk.Label(add_product_window, text="Product Name:")
        label_name.pack()

        entry_name = tk.Entry(add_product_window)
        entry_name.pack()

        label_price = tk.Label(add_product_window, text="Product Price:")
        label_price.pack()

        entry_price = tk.Entry(add_product_window)
        entry_price.pack()

        label_category = tk.Label(add_product_window, text="Category Name:")
        label_category.pack()

        entry_category = tk.Entry(add_product_window)
        entry_category.pack()

        label_description = tk.Label(add_product_window, text="Product Description:")
        label_description.pack()

        entry_description = tk.Entry(add_product_window)
        entry_description.pack()

        btn_add_product = tk.Button(add_product_window, text="Add",
                                    command=lambda: self.add_product(entry_name.get(), entry_price.get(),
                                                                     entry_category.get(), entry_description.get(),
                                                                     add_product_window))

        btn_add_product.pack()

    def add_category(self, name, window):
        if name:
            self.db.add_category(name)
            messagebox.showinfo("Success", "Category added successfully")
            window.destroy()
        else:
            messagebox.showerror("Error", "Category name cannot be empty")

    def add_product(self, name, price, category, description, window):
        if name and price and category:
            self.db.add_product(name, price, category, description)
            messagebox.showinfo("Success", "Product added successfully")
            window.destroy()
        else:
            messagebox.showerror("Error", "Product name, price, and category are required")

    def search_data(self):

        table_names = list(self.db.schema.keys())

        search_window = tk.Toplevel(self.root)
        search_window.title("Search Data")

        table_combobox = ttk.Combobox(search_window, values=table_names)
        table_combobox.set(table_names[0])
        table_combobox.pack()

        def on_table_select(event):

            selected_table = table_combobox.get()
            columns = self.db.get_table_columns(selected_table)

            column_combobox = ttk.Combobox(search_window, values=columns)
            column_combobox.set(columns[0])
            column_combobox.pack()

            def on_search():

                value = value_entry.get()

                if value is not None:

                    search_result = self.db.search_data(selected_table, column_combobox.get(), value)

                    result_window = tk.Toplevel(search_window)
                    result_window.title("Search Result")

                    result_text = tk.Text(result_window)
                    result_text.pack()

                    for row in search_result:
                        result_text.insert(tk.END, str(row) + '\n')

            value_entry = ttk.Entry(search_window)
            value_entry.pack()

            search_button = ttk.Button(search_window, text="Search", command=on_search)
            search_button.pack()

        table_combobox.bind("<<ComboboxSelected>>", on_table_select)

    def show_update_product_form(self):

        update_product_window = tk.Toplevel(self.root)
        update_product_window.title("Update Product")

        label_product_id = tk.Label(update_product_window, text="Product ID:")
        label_product_id.pack()

        entry_product_id = tk.Entry(update_product_window)
        entry_product_id.pack()

        label_name = tk.Label(update_product_window, text="Product Name:")
        label_name.pack()

        entry_name = tk.Entry(update_product_window)
        entry_name.pack()

        label_price = tk.Label(update_product_window, text="Product Price:")
        label_price.pack()

        entry_price = tk.Entry(update_product_window)
        entry_price.pack()

        label_category = tk.Label(update_product_window, text="Category Name:")
        label_category.pack()

        entry_category = tk.Entry(update_product_window)
        entry_category.pack()

        label_description = tk.Label(update_product_window, text="Product Description:")
        label_description.pack()

        entry_description = tk.Entry(update_product_window)
        entry_description.pack()

        # Добавляем кнопку "Изменить"
        btn_update_product = tk.Button(update_product_window, text="Update",
                                       command=lambda: self.update_product(entry_product_id.get(), entry_name.get(),
                                                                           entry_price.get(), entry_category.get(),
                                                                           entry_description.get(),
                                                                           update_product_window))
        btn_update_product.pack()

    def update_product(self, product_id, name, price, category, description, window):
        try:
            product_id = int(product_id)
            price = float(price)
            self.db.update_product(product_id, name, price, category, description)
            messagebox.showinfo("Success", f"Product with ID {product_id} updated successfully.")
            window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid numeric values.")

    def show_delete_row_form(self):
        # Создаем новое окно для формы удаления строки
        delete_row_window = tk.Toplevel(self.root)
        delete_row_window.title("Delete Row")

        table_names = list(self.db.get_table_names())
        table_var = tk.StringVar(delete_row_window)
        table_var.set(table_names[0] if table_names else "")
        table_combobox = ttk.Combobox(delete_row_window, textvariable=table_var, values=table_names)
        table_combobox.pack()

        def on_table_select(event):
            selected_table = table_combobox.get()
            columns = self.db.get_table_columns(selected_table)

            column_var = tk.StringVar(delete_row_window)
            column_var.set(columns[0] if columns else "")
            column_combobox = ttk.Combobox(delete_row_window, textvariable=column_var, values=columns)
            column_combobox.pack()

            value_entry = ttk.Entry(delete_row_window)
            value_entry.pack()

            def on_delete():

                selected_table = table_combobox.get()
                selected_column = column_combobox.get()
                value = value_entry.get()

                if selected_table and selected_column and value:

                    self.db.delete_by_value(selected_table, selected_column, value)
                    messagebox.showinfo("Success", "Row deleted successfully.")
                    delete_row_window.destroy()
                else:
                    messagebox.showerror("Error", "Please select table, column, and enter value.")

            btn_delete = tk.Button(delete_row_window, text="Delete", command=on_delete)
            btn_delete.pack()

        # Обработчик соыбтия
        table_combobox.bind("<<ComboboxSelected>>", on_table_select)

    def run(self):
        self.root.mainloop()
