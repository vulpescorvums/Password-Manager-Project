import tkinter as tk
from log_in import *
from PIL import Image, ImageTk
from tkinter import messagebox, ttk


def perform_login():

    # Get the username and password from the entry fields
    username = username_entry.get()
    password = password_entry.get()

    # Call the login function from the log_in module
    login_result = login(username, password)

    # If login is successful, open the main window
    if login_result[1] == 200:
        stored_accounts = login_result[0]['stored_accounts']
        key = login_result[0]['key']
        iv = login_result[0]['iv']
        master_id = login_result[0]['id']
        login_frame.pack_forget()
        # Create a main frame
        main_frame = tk.Frame(window)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Open the main window
        open_main_window(key, iv, master_id, stored_accounts, main_frame)
        
    # If login is not successful, show an error message
    else:
        messagebox.showerror("Login failed", "Invalid username or password")

def open_main_window(key, iv, id, stored_accounts, main_frame):
    
    main_frame = tk.Frame(window, bg='#645085')
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Make the row and the column containing the Treeview and buttons expand to fill the main_frame
    main_frame.grid_rowconfigure(0, weight=1)
    main_frame.grid_columnconfigure(0, weight=1)

    # Create a Scrollbar widget
    scrollbar = tk.Scrollbar(main_frame, bg='#645085')
    scrollbar.grid(row=0, column=1, sticky='ns')

    # Create a style for the Treeview widget
    style = ttk.Style()
    style.theme_use("clam")

    # Configure the style of the Treeview, Treeview.Heading, and Treeview.Row elements
    style.configure("Treeview", background="#e9e1f7", fieldbackground="#e9e1f7")
    style.configure("Treeview.Heading", background="#ccadff", fieldbackground="#2a2929")
    style.map('Treeview', background=[('selected', '#5647ae')])

    # Create a Treeview widget with the style
    tree = ttk.Treeview(main_frame, yscrollcommand=scrollbar.set, style="Treeview")
    tree.grid(row=0, column=0, sticky='new')

    # Define columns
    tree["columns"] = ("username", "password", "email")

    # Format columns
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("username", anchor=tk.W)
    tree.column("password", anchor=tk.W)
    tree.column("email", anchor=tk.W)

    # Create column headings
    tree.heading("#0", text="", anchor=tk.W)
    tree.heading("username", text="Username", anchor=tk.W)
    tree.heading("password", text="Password", anchor=tk.W)
    tree.heading("email", text="Email", anchor=tk.W)

    # Add the stored accounts to the Treeview
    for account in stored_accounts:
        tree.insert(parent="", index="end", id=str(account["accountnum"]), text="",
                     values=(account["username"], account["password"], account["email"]))

    # Configure the Scrollbar to scroll the Treeview
    scrollbar.config(command=tree.yview)

    # Load the image file
    image = Image.open("./images/refresh.png")

    # Resize the image
    image = image.resize((20, 20))

    # Convert the image to a PhotoImage
    refresh_icon = ImageTk.PhotoImage(image)

    # Create the "Refresh" button with the image
    refresh_button = tk.Button(main_frame, image=refresh_icon, bg='#e9e1f7', command=lambda: refresh_main_window(key, iv, id, main_frame))

    # Keep a reference to the image to prevent it from being garbage collected
    refresh_button.image = refresh_icon

    #Place the button using the grid method
    refresh_button.grid(row=1, column=0, pady=10, sticky='e')

    # button that opens the add account form when clicked
    add_account_button = tk.Button(main_frame, bg='#541fa8', fg='white', text="Add Account", command=lambda: open_add_account_form(key, iv, id, main_frame))
    add_account_button.grid(row=1, column=0, pady=10)

    # button that calls the open register form function when clicked
    update_button = tk.Button(main_frame, text="Edit", bg='#541fa8', fg='white', command=lambda: open_edit_account_form(tree.selection()[0], key, iv, id, main_frame))
    update_button.grid(row=3, column=0, pady = 10)

    # button that deletes the selected account when clicked
    delete_button = tk.Button(main_frame, bg='#541fa8', fg='white', text="Delete", width=10, command=lambda: delete_account(tree.selection()[0]))
    delete_button.grid(row=2, column=0, pady = 10)

    

def refresh_main_window(key, iv, id, main_frame):
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Fetch the updated stored accounts
    stored_accounts = get_stored_accounts(key, iv, id)

    scrollbar = tk.Scrollbar(main_frame, bg='#645085')
    scrollbar.grid(row=0, column=1, sticky='ns')

    # style for the Treeview widget
    style = ttk.Style()
    style.theme_use("clam")

    # Configure the style of the Treeview, Treeview.Heading, and Treeview.Row elements
    style.configure("Treeview", background="#e9e1f7", fieldbackground="#e9e1f7")
    style.configure("Treeview.Heading", background="#ccadff", fieldbackground="#2a2929")
    style.map('Treeview', background=[('selected', '#5647ae')])

    # Treeview widget with the style
    tree = ttk.Treeview(main_frame, yscrollcommand=scrollbar.set, style="Treeview")
    tree.grid(row=0, column=0, sticky='new')

    # Define columns
    tree["columns"] = ("username", "password", "email")

    # Format the columns
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("username", anchor=tk.W)
    tree.column("password", anchor=tk.W)
    tree.column("email", anchor=tk.W)

    # Create column headings
    tree.heading("#0", text="", anchor=tk.W)
    tree.heading("username", text="Username", anchor=tk.W)
    tree.heading("password", text="Password", anchor=tk.W)
    tree.heading("email", text="Email", anchor=tk.W)

    # Add the stored accounts to the Treeview
    for account in stored_accounts:
        tree.insert(parent="", index="end", id=str(account["accountnum"]), text="",
                     values=(account["username"], account["password"], account["email"]))

    # Configure the Scrollbar to scroll the Treeview
    scrollbar.config(command=tree.yview)

    # Load the image file
    image = Image.open("./images/refresh.png")

    # Resize the image
    image = image.resize((20, 20))

    # Convert the image to a PhotoImage
    refresh_icon = ImageTk.PhotoImage(image)

    # Create the "Refresh" button with the image
    refresh_button = tk.Button(main_frame, image=refresh_icon, bg='#e9e1f7', command=lambda: refresh_main_window(key, iv, id, main_frame))

    # Keep a reference to the image to prevent it from being garbage collected
    refresh_button.image = refresh_icon

    #Place the button using the grid method
    refresh_button.grid(row=1, column=0, pady=10, sticky='e')

    # button that opens the add account form when clicked
    add_account_button = tk.Button(main_frame, bg='#541fa8', fg='white', text="Add Account", command=lambda: open_add_account_form(key, iv, id, main_frame))
    add_account_button.grid(row=1, column=0, pady=10)

    # button that deletes the selected account when clicked
    delete_button = tk.Button(main_frame, bg='#541fa8', fg='white', text="Delete", width=10, command=lambda: delete_account(tree.selection()[0]))
    delete_button.grid(row=2, column=0, pady = 10)

    # button that opens the edit account form when clicked
    update_button = tk.Button(main_frame, text="Edit", bg='#541fa8', fg='white', command=lambda: open_edit_account_form(tree.selection()[0], key, iv, id, main_frame))
    update_button.grid(row=3, column=0, pady = 10)

    # Show the main frame
    main_frame.pack(fill=tk.BOTH, expand=True)

def open_add_account_form(key, iv, id, main_frame):
    # Create a new window
    add_account_window = tk.Toplevel(window)
    add_account_window.configure(bg='#645085')

    add_account_window.title("Add Account")

    # Get the screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Specify the window width and height
    window_width = 625
    window_height = 425

    # Calculate the position to center the window
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)

    # Set the position and size of the window
    add_account_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    # title label
    title_label = tk.Label(add_account_window, text="Add Account", bg='#645085', fg='white', font=('Arial', 30))
    title_label.pack(pady=50)

    # label and entry field for the new account's username
    username_label = tk.Label(add_account_window, text="Username", bg='#645085', fg='white')
    username_label.place(relx=0.5, rely=0.3, anchor='center')
    username_entry = tk.Entry(add_account_window, bg='#cfcdd1')
    username_entry.place(relx=0.5, rely=0.35, anchor='center')

    # label and entry field for the new account's password
    password_label = tk.Label(add_account_window, text="Password", bg='#645085', fg='white')
    password_label.place(relx=0.5, rely=0.45, anchor='center')
    password_entry = tk.Entry(add_account_window, bg='#cfcdd1')
    password_entry.place(relx=0.5, rely=0.5, anchor='center')

    # label and entry field for the new account's password
    email_label = tk.Label(add_account_window, text="Email", bg='#645085', fg='white')
    email_label.place(relx=0.5, rely=0.6, anchor='center')
    email_entry = tk.Entry(add_account_window, bg='#cfcdd1')
    email_entry.place(relx=0.5, rely=0.65, anchor='center')

    # button that adds the new account when clicked
    add_button = tk.Button(add_account_window, text="Save", bg='#541fa8', fg='white', command=lambda: add_new_account(username_entry.get(), password_entry.get(),email_entry.get(), key, iv, id, add_account_window))
    add_button.place(relx=0.5, rely=0.75, anchor='center')


def open_edit_account_form(accountnum, key, iv, id, mainframe):
    # Create a new window
    edit_account_window = tk.Toplevel(window)
    edit_account_window.configure(bg='#645085')
    edit_account_window.title("Edit Account")

    # Get the screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Specify the window width and height
    window_width = 625
    window_height = 425

    # Calculate the position to center the window
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)

    # Set the position and size of the window
    edit_account_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    # title label
    title_label = tk.Label(edit_account_window, text="Edit Account", bg='#645085', fg='white', font=('Arial', 30))
    title_label.pack(pady=50)

    # label and entry field for the new account's username
    username_label = tk.Label(edit_account_window, text="Username", bg='#645085', fg='white')
    username_label.place(relx=0.5, rely=0.3, anchor='center')
    username_entry = tk.Entry(edit_account_window, background='#cfcdd1')
    username_entry.place(relx=0.5, rely=0.35, anchor='center')

    # label and entry field for the new account's password
    password_label = tk.Label(edit_account_window, bg='#645085', fg='white', text="Password")
    password_label.place(relx=0.5, rely=0.45, anchor='center')
    password_entry = tk.Entry(edit_account_window, background='#cfcdd1')
    password_entry.place(relx=0.5, rely=0.5, anchor='center')

    # label and entry field for the new account's email
    email_label = tk.Label(edit_account_window, bg='#645085', fg='white', text="Email")
    email_label.place(relx=0.5, rely=0.6, anchor='center')
    email_entry = tk.Entry(edit_account_window, background='#cfcdd1')
    email_entry.place(relx=0.5, rely=0.65, anchor='center')

    # button that adds the new account when clicked
    add_button = tk.Button(edit_account_window, bg='#541fa8', fg='white', activebackground='#545151', activeforeground='#5647ae', text="Save", command=lambda: edit_account(username_entry.get(), password_entry.get(),email_entry.get(), key, iv, id, accountnum, edit_account_window))
    add_button.place(relx=0.5, rely=0.75, anchor='center')
    
def open_register_form(main_frame):
    # Create a new window
    register_window = tk.Toplevel(window)
    register_window.configure(bg='#645085')

    # Direct all events to this window
    register_window.grab_set()

    register_window.title("Register")

    # Get the screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Specify the window width and height
    window_width = 625
    window_height = 425

    # Calculate the position to center the window
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)

    # Set the position and size of the window
    register_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    # title label
    title_label = tk.Label(register_window, text="Create an Account", bg='#645085', fg='white', font=('Arial', 30))
    title_label.pack(pady=50, anchor='center')

    # label and entry field for the new account's username
    username_label = tk.Label(register_window, text="Username", bg='#645085', fg='white')
    username_label.place(relx=0.5, rely=0.3, anchor='center')
    username_entry = tk.Entry(register_window, background='#cfcdd1')
    username_entry.place(relx=0.5, rely=0.35, anchor='center')

    # label and entry field for the new account's password
    password_label = tk.Label(register_window, bg='#645085', fg='white', text="Password")
    password_label.place(relx=0.5, rely=0.45, anchor='center')
    password_entry = tk.Entry(register_window, background='#cfcdd1')
    password_entry.place(relx=0.5, rely=0.5, anchor='center')

    # button to submit the form
    register_button = tk.Button(register_window, text="Register", bg='#541fa8', fg='white', command=lambda: register(password_entry.get(), username_entry.get(), register_window))
    register_button.place(relx=0.5, rely=0.6, anchor='center')

    def create_tooltip(widget, text):
        tooltip_window = None

        def enter(event):
            nonlocal tooltip_window
            tooltip_window = tk.Toplevel(widget)
            tooltip_window.wm_overrideredirect(True)  # Remove window decorations
            tooltip_window.configure(bg='#645085')

            # label with the text
            label = tk.Label(tooltip_window, text=text, bg='#645085', fg='white')
            label.pack()

            x, y, _, _ = widget.bbox("insert")
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 25
            tooltip_window.wm_geometry(f"+{x}+{y}")

        def leave(event):
            nonlocal tooltip_window
            if tooltip_window is not None:
                widget.after(100, tooltip_window.destroy)

        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)

    # Load the image file
    image = Image.open("./images/info_icon.png")

    # Resize the image
    image = image.resize((20, 20))

    # Convert the image to a PhotoImage
    info_icon = ImageTk.PhotoImage(image)

    # Create an icon
    icon = tk.Label(register_window, bg='#645085')
    icon.image = info_icon  # Keep a reference to the PhotoImage object
    icon.config(image=info_icon)
    icon.place(x=380, y=205)

    # Create a tooltip for the icon
    create_tooltip(icon,"Password must contain at least:\n"
                        "8 characters,\n"
                        "one uppercase letter,\n"
                        "one lowercase letter,\n"
                        "and one digit")




# Create a new Tkinter window
window = tk.Tk()
window.configure(bg='#645085')
window.title("Password Manager")


# Create a frame for the login widgets
login_frame = tk.Frame(window, bg='#645085')
login_frame.pack(expand=True)
#window.geometry("600x400")

# Get the screen width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Specify the window width and height
window_width = 625
window_height = 380

# Calculate the position to center the window
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)

# Set the position and size of the window
window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

# label and entry field for the username
username_label = tk.Label(login_frame, bg='#645085', fg='white', text="Username", font=('Arial', 10))
username_label.pack(anchor='center', fill='x')
username_entry = tk.Entry(login_frame, bg='#cfcdd1')
username_entry.pack(anchor='center', pady=10)

# label and entry field for the password
password_label = tk.Label(login_frame, bg='#645085', fg='white', text="Password", font=('Arial', 10))
password_label.pack(anchor='center',  fill='both')
password_entry = tk.Entry(login_frame, show="*", bg='#cfcdd1')
password_entry.pack(anchor='center', pady=(10))

# button that calls the perform_login function when clicked
login_button = tk.Button(login_frame, bg='#541fa8', fg='white', activebackground='#853cfa', activeforeground='white', text="Login", command=perform_login)
login_button.pack(anchor='center', fill='both', pady=(10,0))

# button that calls the open register form function when clicked
register_button = tk.Button(login_frame, bg='#541fa8', fg='white', activebackground='#853cfa', activeforeground='#5647ae', text="Register", command=lambda: open_register_form(login_frame))
register_button.pack(anchor='center', fill='both', pady=(10,0))

# Create a frame for the main window widgets, but don't show it yet
main_frame = tk.Frame(window)
main_frame.pack()

# Start the Tkinter event loop
window.mainloop()