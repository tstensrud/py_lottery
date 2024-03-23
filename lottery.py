import sys
from tkinter import messagebox, scrolledtext
from ticket_operations import Ticket_Operations
from user_operations import User_Operations
from tkinter import *
import tkinter as tk

ticket_operations = Ticket_Operations()
user_operations = User_Operations()
current_winner_numbers = [None] * ticket_operations.numbers_per_row

def main():
    
    user_operations.add_new_user("A", "A@C.D", "123", "dad")
    user_operations.add_new_user("B", "B@C.D", "123", "dad")
    user_operations.add_new_user("C", "C@C.D", "123", "dad")
    user_operations.add_new_user("D", "D@C.D", "123", "dad")

    # exit-button in menu
    def exit():
        sys.exit()
    
    # add new ticket
    def add_new_ticket():
        try:
            user_id = int(new_ticket_user_id_text_field.get())
        except ValueError:
            messagebox.showerror("Error", f"User ID can only contain digits")
            return
        if user_operations.does_user_exist(user_id) == False:
            messagebox.showinfo("Error", f"User id \"{user_id}\" not found")
            return
        rows = row_choice.get()
        ticket_operations.add_new_ticket(rows, user_id)

    # add new user
    def add_new_user():
        user_name = add_user_name_entry.get()
        email = add_user_email_entry.get()
        try:
            phone_number = int(add_user_phone_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Only numbers in phonenumber")
            return
        password = add_user_password_entry.get()
        user_operations.add_new_user(user_name, email, phone_number, password)
        new_user= user_operations.find_user(None, user_name, None)
        new_user_id = new_user.get_user_id()
        messagebox.showinfo("User added", f"User {user_name} added with user-id: {new_user_id} ")
        for i in range (len(add_user_entries)):
            add_user_entries[i].delete(0, tk.END)

    # switching frames from menu options
    # hides all frames that is not menuItem.
    def frame_selection_from_menu(menu_item):
        for i in range(len(frames)):
            if i != menu_item:
                frames[i].forget()
            else:
                frames[i].pack(fill="both", expand=1)

    def draw_new_set_of_winning_numbers():
        current_winner_numbers = ticket_operations.generate_winning_numbers()

    def find_user():
        find_user_text_area.delete(1.0, END)
        name = None
        email = None
        userid = None

        if find_user_name_entry.get() != "":
            name = find_user_name_entry.get()

        if find_user_email_entry.get() != "":
            email = find_user_email_entry.get()

        if find_user_user_id_entry.get() != "":
            userid = find_user_user_id_entry.get()

        user_found = user_operations.find_user(userid, name, email)

        if user_found == None:
            find_user_text_area.insert(1.0, "User not found")
        else:
            user_name = user_found.get_name()
            user_email = user_found.get_email()
            user_id = user_found.get_user_id()
            find_user_text_area.insert(1.0, f"User-ID: {user_id}\nName: {user_name} \nE-mail: {user_email}\n")
            

        

    #main window
    main_window = tk.Tk()
    main_window.geometry("1024x768")
    main_window.title("Lottery")
    main_window.config(background="#21304a")

    # settings for customisation
    default_text_color= "white"
    default_bg_color="#21304a"
    default_entry_field_width = 20
    INITIAL_VERTICAL_WIDGET_PLACEMENT = 50
    vertical_placement = INITIAL_VERTICAL_WIDGET_PLACEMENT
    INITIAL_HORIZONTAL_WIDGET_PLACEMENT = 10
    horizontal_placement = INITIAL_HORIZONTAL_WIDGET_PLACEMENT

    # Frames
    initial_frame = tk.Frame(main_window)
    game_options_frame = tk.Frame(main_window)
    new_ticket_frame = tk.Frame(main_window)
    ticket_stats_frame = tk.Frame(main_window)
    add_user_frame = tk.Frame(main_window)
    user_stats_frame = tk.Frame(main_window)
    find_user_frame = tk.Frame(main_window)
    frames = [initial_frame, game_options_frame, new_ticket_frame, ticket_stats_frame, add_user_frame, 
              user_stats_frame, find_user_frame]
    
    for i in range(len(frames)):
        frames[i].config(background=default_bg_color)

    # widgets for default frame
    welcome_label = tk.Label(initial_frame, text="Use menu to start")
    welcome_label.pack()
    welcome_label.config(background=default_bg_color, fg=default_text_color)
    initial_frame.pack(fill="both", expand=1)

     
    '''
    widgets for game stats frame
    '''
    game_stats_label = tk.Label(game_options_frame, text="GAME OPTIONS")
    game_stats_label.pack()
    game_stats_label.config(background=default_bg_color, fg=default_text_color)

    '''
    widgets for new ticket frame
    '''
    new_ticket_label = tk.Label(new_ticket_frame, text="NEW TICKET")
    new_ticket_label.pack()
    new_ticket_label.config(background=default_bg_color, fg=default_text_color)
    new_ticket_rows_label = tk.Label(new_ticket_frame, text="How many rows in ticket: ")
    new_ticket_user_id_label = tk.Label(new_ticket_frame, text="User ID")
    new_ticket_rows_label.place(x=10, y=50)
    new_ticket_rows_label.config(background=default_bg_color, fg=default_text_color)
    new_ticket_user_id_label.place(x=10, y=100)
    new_ticket_user_id_label.config(background=default_bg_color, fg=default_text_color)
    new_ticket_user_id_text_field = tk.Entry(new_ticket_frame, width=10)
    new_ticket_user_id_text_field.place(x=170, y=100)
    row_options = [1,2,3,4,5,6,7,8,9,10]
    row_choice = tk.IntVar(new_ticket_frame)
    row_choice.set(10)
    row_options_menu = tk.OptionMenu(new_ticket_frame, row_choice, *row_options)
    row_options_menu.place(x=170, y=50)
    row_options_menu.config(highlightthickness=0)
    new_ticket_button = tk.Button(new_ticket_frame, text="New ticket", width=10, height=1, command=add_new_ticket)
    new_ticket_button.place(x=10, y=150)

    # widgets for ticket stats frame
    ticket_stats_label = tk.Label(ticket_stats_frame, text="TICKET STATS")
    ticket_stats_label.pack()
    ticket_stats_label.config(background=default_bg_color, fg=default_text_color)


    '''
    widgets for add-user frame
    '''
    # labels
    add_user_label = tk.Label(add_user_frame, text="ADD USER")
    add_user_label.pack()
    add_user_label.config(background=default_bg_color, fg=default_text_color)
    add_user_name_label = tk.Label(add_user_frame, text="Name: ")
    add_user_email_label = tk.Label(add_user_frame, text="E-mail:")
    add_user_phone_label = tk.Label(add_user_frame, text="Phone number: ")
    add_user_password_label = tk.Label(add_user_frame, text="Password: ")
    add_user_labels = [add_user_name_label, add_user_email_label, add_user_phone_label, add_user_password_label]
    
    for i in range(len(add_user_labels)):
        add_user_labels[i].place(x=horizontal_placement, y=vertical_placement)
        add_user_labels[i].config(background=default_bg_color, fg=default_text_color)
        vertical_placement += 50
    vertical_placement = INITIAL_VERTICAL_WIDGET_PLACEMENT
    
    # entry text-fields
    add_user_name_entry = tk.Entry(add_user_frame, width=default_entry_field_width+10)
    add_user_email_entry = tk.Entry(add_user_frame, width=default_entry_field_width+10)
    add_user_phone_entry = tk.Entry(add_user_frame, width=default_entry_field_width+10)
    add_user_password_entry = tk.Entry(add_user_frame, width=default_entry_field_width+10)
    add_user_entries = [add_user_name_entry, add_user_email_entry, add_user_phone_entry, add_user_password_entry]
    
    for i in range(len(add_user_entries)):
        add_user_entries[i].place(x=horizontal_placement+160, y=vertical_placement)
        vertical_placement += 50
    vertical_placement = INITIAL_VERTICAL_WIDGET_PLACEMENT
    
    # button
    add_user_button = tk.Button(add_user_frame, text="Add user", width=10, height=1, command=add_new_user)
    add_user_button.place(x=INITIAL_HORIZONTAL_WIDGET_PLACEMENT, y=250)

    '''
    widgets for user stats frame
    '''
    user_stats_label = tk.Label(user_stats_frame, text="USER STATS")
    user_stats_label.pack()
    user_stats_label.config(background=default_bg_color, fg=default_text_color)

    '''
    widgets for find user frame
    '''
    find_user_label = tk.Label(find_user_frame, text="FIND USER")
    # labels
    find_user_label.pack()
    find_user_label.config(background=default_bg_color, fg=default_text_color)
    find_user_name_label = tk.Label(find_user_frame, text="User name")
    find_user_email_label = tk.Label(find_user_frame, text="Email")
    find_user_user_id__label = tk.Label(find_user_frame, text="User-ID")
    find_user_labels = [find_user_name_label, find_user_email_label, find_user_user_id__label]
    for i in range(len(find_user_labels)):
        find_user_labels[i].place(x=horizontal_placement, y=vertical_placement)
        find_user_labels[i].config(background=default_bg_color, fg=default_text_color)
        vertical_placement += 50
    vertical_placement = INITIAL_VERTICAL_WIDGET_PLACEMENT
    #text entries
    find_user_name_entry = tk.Entry(find_user_frame, width=default_entry_field_width)
    find_user_email_entry = tk.Entry(find_user_frame, width=default_entry_field_width)
    find_user_user_id_entry = tk.Entry(find_user_frame, width=default_entry_field_width)
    find_user_entries = [find_user_name_entry, find_user_email_entry, find_user_user_id_entry]
    for i in range(len(find_user_entries)):
        find_user_entries[i].place(x=horizontal_placement+160, y=vertical_placement)
        vertical_placement += 50
    vertical_placement = INITIAL_VERTICAL_WIDGET_PLACEMENT
    #button
    find_user_button = tk.Button(find_user_frame, text="Find", width=10, height=1, command=find_user)
    find_user_button.place(x=INITIAL_HORIZONTAL_WIDGET_PLACEMENT, y=200)
    # output-text field
    find_user_text_area = scrolledtext.ScrolledText(find_user_frame, wrap=tk.WORD, width=70, height=35)
    find_user_text_area.place(x=350, y=INITIAL_VERTICAL_WIDGET_PLACEMENT)

    #
    # TOP MENU
    #
    menu_bar = Menu(main_window)
    
    #file menu (1)
    menu_bar_file_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=menu_bar_file_menu)
    menu_bar_file_menu.add_command(label="Game options", command=lambda: frame_selection_from_menu(1))
    menu_bar_file_menu.add_separator()
    menu_bar_file_menu.add_command(label="Exit", command=exit)
    
    
    #tickets menu (2.3)
    menu_bar_tickets_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Ticket", menu=menu_bar_tickets_menu)
    menu_bar_tickets_menu.add_command(label="New ticket", command=lambda: frame_selection_from_menu(2))
    menu_bar_tickets_menu.add_command(label="Ticket stats", command=lambda: frame_selection_from_menu(3))
    

    #users menu (4, 5, 6)
    menu_bar_users_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Users", menu=menu_bar_users_menu)
    menu_bar_users_menu.add_command(label="Add new user", command=lambda: frame_selection_from_menu(4))
    menu_bar_users_menu.add_command(label="User statistics", command=lambda: frame_selection_from_menu(5))
    menu_bar_users_menu.add_command(label="Find user", command=lambda: frame_selection_from_menu(6))
    

    main_window.config(menu=menu_bar)
    main_window.mainloop()

if __name__ == "__main__":
    main()























