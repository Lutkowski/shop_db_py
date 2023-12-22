from database import Database
from gui import GUI
from admin_panel import AdminPanel
from user_panel import UserPanel


def main():
    db = Database()

    db.execute_sql_file('SQL/user.sql')
    db.execute_sql_file('SQL/admin.sql')
    gui = GUI(db)
    gui.run()

    user_role = gui.user_role
    user_id = gui.user_id

    if user_role == "admin":
        admin_panel = AdminPanel(db)
        admin_panel.run()
    if user_role == "customer":
        user_panel = UserPanel(db, user_id)
        user_panel.run()

    db.close_connection()


if __name__ == "__main__":
    main()
