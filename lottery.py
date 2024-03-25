import sys
import re
import tkinter as tk
from tkinter import *
from tkinter import messagebox, scrolledtext
from ticket_operations import Ticket_Operations
from user_operations import User_Operations



ticket_operations = Ticket_Operations()
user_operations = User_Operations()
current_winning_numbers = [None] * ticket_operations.numbers_per_row
previous_winning_numbers = []
is_round_finished = False

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
        new_ticket_text_area.delete(1.0, tk.END)
        global is_round_finished
        if is_round_finished == True:
            messagebox.showerror("Error", "No new tickets can be added untill round is reset")
            return
        try:
            user_id = int(new_ticket_user_id_text_field.get())
        except ValueError:
            messagebox.showerror("Error", f"User ID can only contain digits")
            return
        try:
            amount_of_tickets = int(new_ticket_amount_entry.get())
        except ValueError:
            messagebox.showerror("Error", f"Amount of tickets must be a number")
            return

        if user_operations.does_user_exist(user_id) == False:
            messagebox.showinfo("Error", f"User id \"{user_id}\" not found")
            return
        
        if amount_of_tickets == 0:
            messagebox.showerror("Error", f"Amount of tickets must be greater than 0")
            return

        rows = row_choice.get()
        for _ in range(amount_of_tickets):
            new_ticket_id = ticket_operations.add_new_ticket(rows, user_id)
            user_operations.find_user(user_id, None, None).add_active_ticket(new_ticket_id)
            new_ticket_text_area.insert(tk.END, f"Ticket {new_ticket_id} added to user {user_id}\n")
            #print(ticket_operations.get_active_ticket(new_ticket_id).get_rows())

        new_ticket_user_id_text_field.delete(0, tk.END)
        new_ticket_amount_entry.delete(0, tk.END)

    # find ticket based on ticket ID
    def find_ticket():
        try:
            ticket_id = int(find_ticket_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Ticket ID can only be numbers")
            return
        find_ticket_area.delete(1.0, tk.END)
        if find_ticket_ticket_status.get() == 0:
            ticket = ticket_operations.get_active_ticket(ticket_id)
            if ticket == None:
                messagebox.showinfo("Not found", "Ticket-id not found. Perhaps it's archived?")
                return
        else:
            ticket = ticket_operations.get_archived_ticket(ticket_id)
            if ticket == None:
                messagebox.showinfo("Not found", "Ticket-id not found. Perhaps it's not archived?")
                return
        ticket_date = ticket.get_date()
        rows = ticket.get_rows()
        user = ticket.get_user_id()
        find_ticket_area.insert(tk.END, f"Object adress: {ticket}\nAssigned to user: {user}\nPurchased at: {ticket_date}\n")
        for i in range(len(rows)):
            for j in range(len(rows[i])):
                find_ticket_area.insert(tk.END, f"Row {j}: {rows[i][j]}\n")
        
    # list all previous winning numbers
    def list_archived_winning_numbers():
        global previous_winning_numbers
        game_options_text_area.delete(1.0, END)
        for i in range(len(previous_winning_numbers)):
            game_options_text_area.insert(tk.END, f"Game {i+1}: ")
            for j in range(len(previous_winning_numbers[i])):
                if j == len(previous_winning_numbers[i]) - 1:
                    game_options_text_area.insert(tk.END, f"{previous_winning_numbers[i][j]}")
                else:    
                    game_options_text_area.insert(tk.END, f"{previous_winning_numbers[i][j]} - ")
            game_options_text_area.insert(tk.END, "\n")
        
    # add new user
    def add_new_user():
        user_name = add_user_name_entry.get()
        email = add_user_email_entry.get()
        email_pattern = re.compile("[a-zA-Z0-9_]+@[a-zA-Z0-9_]+[.]+[a-zA-Z]{2,4}$")
        if email_pattern.search(email) == None:
            messagebox.showerror("Error", f"Email \"{email}\" is not valid - name@domain.com")
            return
        if user_operations.find_existing_email(email) == True:
            messagebox.showerror("Error", f"Email \"{email}\" allready exists in system")
            return
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
        update_game_stats()

    # draw new set of winning numbers. Can only be used if game is reset
    def draw_new_set_of_winning_numbers():
        global current_winning_numbers
        if current_winning_numbers[0] != None:
            messagebox.showerror("Oh no!", "A set of winning numbers is already drawn")
            return
        game_options_text_area.delete(1.0, END)
        current_winning_numbers = ticket_operations.generate_winning_numbers()
        game_options_text_area.insert(1.0, "Wining numbers are:\n")
        for i in range(len(current_winning_numbers)):
            if i == len(current_winning_numbers) - 1:
                game_options_text_area.insert(tk.END, f"{current_winning_numbers[i]}")
            else:
                game_options_text_area.insert(tk.END, f"{current_winning_numbers[i]} - ")

    # update game stats which can change from each time the game stats window is opened
    def update_game_stats():
        game_stats_text_area.delete(1.0, tk.END)
        total_users = len(user_operations.users)
        total_active_tickets = len(ticket_operations.active_tickets)
        total_archived_tickets = len(ticket_operations.archived_tickets)
        total_income = ticket_operations.get_income()
        current_price_pool = ticket_operations.get_current_price_pool()
        jackpot = ticket_operations.get_jackpot()
        game_stats_text_area.insert(tk.END, f"Total users: {total_users}\nCurrent active tickets: {total_active_tickets}\nTotal archived tickets: {total_archived_tickets}\nTotal income: {total_income}\nCurrent price pool: {current_price_pool}\nCurrent jackpot: {jackpot}")

    #find user
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
            try:
                userid = int(find_user_user_id_entry.get())
            except ValueError:
                messagebox.showerror("Error", "User-ID can only contain numbers")
                return

        user_found = user_operations.find_user(userid, name, email)

        if user_found == None:
            find_user_text_area.insert(1.0, "User not found")
        else:
            user_name = user_found.get_name()
            user_email = user_found.get_email()
            user_id = user_found.get_user_id()
            user_creation = user_found.get_date()
            user_active_tickets = user_found.get_active_tickets()
            user_archived_tickets = user_found.get_archived_tickets()
            find_user_text_area.insert(1.0, f"User-ID: {user_id} created at {user_creation}\nName: {user_name} \nE-mail: {user_email}\n\n")
            find_user_text_area.insert(tk.END, "Current active tickets:\n")
            
            if len(user_active_tickets) != 0:
                for i in range(len(user_active_tickets)):
                    find_user_text_area.insert(tk.END, f"Ticket nr.{i+1}: ticket-id: {user_active_tickets[i]}\n")
            else:
                find_user_text_area.insert(tk.END, f"No active tickets\n")
            find_user_text_area.insert(tk.END, "\nArchived tickets:\n")
            if len(user_archived_tickets) != 0:
                for i in range(len(user_archived_tickets)):
                    find_user_text_area.insert(tk.END, f"Ticket nr.{i+1}: ticket-id: {user_archived_tickets[i]}\n")
            else:
                find_user_text_area.insert(tk.END, f"No tickets in archive")

            find_user_name_entry.delete(0, tk.END)
            find_user_email_entry.delete(0, tk.END)
            find_user_user_id_entry.delete(0, tk.END)

    #reset game
    def game_reset():
        global current_winning_numbers, previous_winning_numbers, is_round_finished      
        user_operations.reset_game()
        ticket_operations.reset_game()
        previous_winning_numbers.append(list(current_winning_numbers))
        for i in range(len(current_winning_numbers)):
            current_winning_numbers[i] = None
        messagebox.showinfo("Reset", "Game is reset.")
        game_options_text_area.delete(1.0, END)
        is_round_finished = False
    
    # find this rounds winners
    def find_winners():
        game_options_text_area.delete(1.0, tk.END)
        global current_winning_numbers, is_round_finished
        if current_winning_numbers[0] == None:
            messagebox.showinfo("Ooops", "No winning numbers are drawn yet")
            return
        
        winners = ticket_operations.find_winning_tickets(current_winning_numbers)
        if len(winners) == 0:
            game_options_text_area.insert(1.0, f"No winners this round!\n")
            game_options_text_area.insert(tk.END, f"Jackpot for next round. {ticket_operations.get_current_price_pool()} added to jackpot.") 
        else:
            for i in range(len(winners)):
                game_options_text_area.insert(1.0, f"Ticket ID: {winners[i].get_ticket_id()} belonging to user {winners[i].get_user_id()} has won!\n")
        is_round_finished = True

    # settings for customisation
    default_text_color= "white"
    default_bg_color="#21304a"
    default_window_size = "1024x758"
    default_entry_field_width = 20
    INITIAL_VERTICAL_WIDGET_PLACEMENT = 50
    vertical_placement = INITIAL_VERTICAL_WIDGET_PLACEMENT
    INITIAL_HORIZONTAL_WIDGET_PLACEMENT = 10
    horizontal_placement = INITIAL_HORIZONTAL_WIDGET_PLACEMENT

    #main window
    main_window = tk.Tk()
    main_window.geometry(default_window_size)
    main_window.title("Lottery")
    main_window.config(background=default_bg_color)

    # Frames
    initial_frame = tk.Frame(main_window)
    game_options_frame = tk.Frame(main_window)
    new_ticket_frame = tk.Frame(main_window)
    game_stats_frame = tk.Frame(main_window)
    add_user_frame = tk.Frame(main_window)
    user_stats_frame = tk.Frame(main_window)
    find_user_frame = tk.Frame(main_window)
    find_ticket_frame = tk.Frame(main_window)
    frames = [initial_frame, game_options_frame, new_ticket_frame, game_stats_frame, add_user_frame, 
              user_stats_frame, find_user_frame, find_ticket_frame]
    
    for i in range(len(frames)):
        frames[i].config(background=default_bg_color)

    # widgets for default frame
    welcome_label = tk.Label(initial_frame, text="Use menu to start")
    welcome_label.pack()
    welcome_label.config(background=default_bg_color, fg=default_text_color)
    initial_frame.pack(fill="both", expand=1)

     
    '''
    widgets for game options frame
    '''
    # labels
    game_options_label = tk.Label(game_options_frame, text="GAME OPTIONS")
    game_options_label.pack()
    game_options_label.config(background=default_bg_color, fg=default_text_color)
    game_options_draw_winning_numbers_label = tk.Label(game_options_frame, text="Draw new winning numbers")
    game_options_reset_game_label = tk.Label(game_options_frame, text="Reset game")
    game_options_archive_label = tk.Label(game_options_frame, text="Winning numbers archive")
    game_options_find_winners_label = tk.Label(game_options_frame, text="Find this rounds winners")
    game_options_labels = [game_options_draw_winning_numbers_label, game_options_reset_game_label, game_options_archive_label, game_options_find_winners_label]
    for i in range(len(game_options_labels)):
        game_options_labels[i].config(background=default_bg_color, fg=default_text_color)
        game_options_labels[i].place(x=INITIAL_HORIZONTAL_WIDGET_PLACEMENT, y=vertical_placement)
        vertical_placement += 50
    vertical_placement = INITIAL_VERTICAL_WIDGET_PLACEMENT
    # buttons
    game_options_draw_winning_numbers_button = tk.Button(game_options_frame, text="Draw numbers", width=15, height=1, command=draw_new_set_of_winning_numbers)
    game_options_reset_game_button = tk.Button(game_options_frame, text="Reset game", width=15, height=1, command=game_reset)
    game_options_archived_winners_button = tk.Button(game_options_frame, text="Archive", width=15, height=1, command=list_archived_winning_numbers)
    game_options_draw_winners_button = tk.Button(game_options_frame, text="Draw!", width=15, height=1, command=find_winners)
    game_option_buttons = [game_options_draw_winning_numbers_button, game_options_reset_game_button, game_options_archived_winners_button, game_options_draw_winners_button]

    for i in range(len(game_option_buttons)):
        game_option_buttons[i].place(x=INITIAL_HORIZONTAL_WIDGET_PLACEMENT+160, y=vertical_placement)
        vertical_placement += 50
    vertical_placement = INITIAL_VERTICAL_WIDGET_PLACEMENT
    # text area
    game_options_text_area = scrolledtext.ScrolledText(game_options_frame, wrap=tk.WORD, width=70, height=35)
    game_options_text_area.place(x=350, y=INITIAL_VERTICAL_WIDGET_PLACEMENT)
    '''
    widgets for new ticket frame
    '''
    new_ticket_label = tk.Label(new_ticket_frame, text="NEW TICKET")
    new_ticket_label.pack()
    new_ticket_label.config(background=default_bg_color, fg=default_text_color)
    new_ticket_rows_label = tk.Label(new_ticket_frame, text="How many rows in ticket: ")
    new_ticket_user_id_label = tk.Label(new_ticket_frame, text="User ID for ticket holder")
    new_ticket_amount_label = tk.Label(new_ticket_frame, text="How many tickets")
    new_ticket_labels = [new_ticket_rows_label, new_ticket_user_id_label, new_ticket_amount_label]
    for i in range(len(new_ticket_labels)):
        new_ticket_labels[i].place(x=horizontal_placement, y=vertical_placement)
        new_ticket_labels[i].config(background=default_bg_color, fg=default_text_color)
        vertical_placement += 50
    vertical_placement = INITIAL_VERTICAL_WIDGET_PLACEMENT
    
    new_ticket_user_id_text_field = tk.Entry(new_ticket_frame, width=10)
    new_ticket_user_id_text_field.place(x=170, y=100)
    new_ticket_amount_entry = tk.Entry(new_ticket_frame, width=10)
    new_ticket_amount_entry.place(x=170, y=150)
    row_options = [1,2,3,4,5,6,7,8,9,10]
    row_choice = tk.IntVar(new_ticket_frame)
    row_choice.set(10)
    row_options_menu = tk.OptionMenu(new_ticket_frame, row_choice, *row_options)
    row_options_menu.place(x=170, y=50)
    row_options_menu.config(highlightthickness=0)
    new_ticket_button = tk.Button(new_ticket_frame, text="New ticket", width=10, height=1, command=add_new_ticket)
    new_ticket_button.place(x=10, y=200)
    
    new_ticket_text_area = scrolledtext.ScrolledText(new_ticket_frame, wrap=tk.WORD, width=70, height=35)
    new_ticket_text_area.place(x=350, y=INITIAL_VERTICAL_WIDGET_PLACEMENT)

    '''
    widgets for game stats frame
    '''
    game_stats_label = tk.Label(game_stats_frame, text="GAME STATS")
    game_stats_label.pack()
    game_stats_label.configure(background=default_bg_color, fg=default_text_color)
    game_stats_text_area = scrolledtext.ScrolledText(game_stats_frame, wrap=tk.WORD, width=70, height=35)
    game_stats_text_area.pack()
    game_stats_text_area.insert(1.0, "GAME STATS:\n")
    update_game_stats()

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
    find_user_name_label = tk.Label(find_user_frame, text="Name")
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

    '''
    widgets for find ticket frame
    '''
    find_ticket_label = tk.Label(find_ticket_frame, text="FIND TICKET")
    find_ticket_label.pack()
    find_ticket_label.config(background=default_bg_color, fg=default_text_color)
    find_ticket_ticketid_label = tk.Label(find_ticket_frame, text="Ticket ID")
    find_ticket_ticketstatus_label = tk.Label(find_ticket_frame, text="Archived")
    find_ticket_labels = [find_ticket_ticketid_label, find_ticket_ticketstatus_label]
    for i in range(len(find_ticket_labels)):
        find_ticket_labels[i].place(x=horizontal_placement, y=vertical_placement)
        find_ticket_labels[i].config(background=default_bg_color, fg=default_text_color)
        vertical_placement += 50
    vertical_placement = INITIAL_VERTICAL_WIDGET_PLACEMENT
    find_ticket_entry = tk.Entry(find_ticket_frame, width=default_entry_field_width)
    find_ticket_ticket_status = IntVar()
    find_ticket_checkbox = Checkbutton(find_ticket_frame, variable=find_ticket_ticket_status, onvalue=1, offvalue=0)
    find_ticket_checkbox.config(background=default_bg_color, activebackground=default_bg_color)
    find_ticket_widgets = [find_ticket_entry, find_ticket_checkbox]
    for i in range(len(find_ticket_widgets)):
        find_ticket_widgets[i].place(x=horizontal_placement+100, y=vertical_placement)
        vertical_placement += 50
    vertical_placement = INITIAL_VERTICAL_WIDGET_PLACEMENT
    find_ticket_button = tk.Button(find_ticket_frame, text="Find", width=10, height=1, command=find_ticket)
    find_ticket_button.place(x=INITIAL_HORIZONTAL_WIDGET_PLACEMENT, y=150)
    find_ticket_area = scrolledtext.ScrolledText(find_ticket_frame, wrap=tk.WORD, width=70, height=35)
    find_ticket_area.place(x=350, y=INITIAL_VERTICAL_WIDGET_PLACEMENT)
    #
    # TOP MENU
    #
    menu_bar = Menu(main_window)
    
    #file menu (1)
    menu_bar_file_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=menu_bar_file_menu)
    menu_bar_file_menu.add_command(label="Game options", command=lambda: frame_selection_from_menu(1))
    menu_bar_file_menu.add_command(label="Game stats", command=lambda: frame_selection_from_menu(3))
    menu_bar_file_menu.add_separator()
    menu_bar_file_menu.add_command(label="Exit", command=exit)
    
    
    #tickets menu (2.3)
    menu_bar_tickets_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Ticket", menu=menu_bar_tickets_menu)
    menu_bar_tickets_menu.add_command(label="New ticket", command=lambda: frame_selection_from_menu(2))
    menu_bar_tickets_menu.add_command(label="Find ticket", command=lambda: frame_selection_from_menu(7))
    
    

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
