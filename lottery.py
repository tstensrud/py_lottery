import sys
import re
import tkinter as tk
import os
from tkinter import *
from tkinter import messagebox, scrolledtext
from ticket_operations import Ticket_Operations
from user_operations import User_Operations
from classes import Operations

operations = Operations()
ticket_operations = Ticket_Operations()
user_operations = User_Operations()

winning_numbers = [None] * ticket_operations.numbers_per_row
previous_winning_numbers = []


def main():

    # loading all previous and current set of winning numbers. first in list index 0 is always current.
    # set loadup to True when method is called upon program start. set update to True when it is to update with
    # new set of winning numbers. new_set is the new set if winning numbers
    def load_all_winning_numbers(loadup, update, new_set):
        global winning_numbers, previous_winning_numbers

        if loadup == True:
            
            # if no numbers have been drawn yet, add an empty set of 0s
            file_size = os.path.getsize("./data/oldwinners.pkl")
            if file_size == 0:
                start_list = [[0,0,0,0,0,0,0,0]]
                operations.write_to_database(start_list, "w")

            number_sets = operations.read_database("w")
            for i in range(len(number_sets)):
                if i == 0:
                    winning_numbers = number_sets[i]
                else:
                    previous_winning_numbers.append(number_sets[i])
            
        if update == True:
            number_sets = operations.read_database("w")
            winning_numbers = number_sets[0]
            number_sets.insert(0,new_set)
            operations.write_to_database(number_sets, "w")
            load_all_winning_numbers(True, False, None)

    # add new ticket
    def add_new_ticket():
        new_ticket_text_area.delete(1.0, tk.END)
        game_info = operations.read_gameinfo_json()

        global is_round_finished
        if game_info["game"]["round_finished"] == False:
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
            new_ticket_id = int(ticket_operations.add_new_ticket(rows, user_id))
            user_operations.find_user(user_id, None, None).add_ticket(new_ticket_id)
            new_ticket_text_area.insert(tk.END, f"Ticket {new_ticket_id} added to user {user_id}\n")
            user_operations.add_ticketid_to_user(new_ticket_id, user_id)
        
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
        
        game_options_text_area.insert(tk.END, f"Game : {previous_winning_numbers}\n")
        
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
        new_user = user_operations.add_new_user(user_name, email, phone_number, password)
        new_user_id = new_user.get_user_id()
        messagebox.showinfo("User added", f"User {user_name} added with user-id: {new_user_id} ")
        for i in range (len(add_user_entries)):
            add_user_entries[i].delete(0, tk.END)

    # switching frames from menu options
    # hides all frames that is not menuItem.
    def frame_selection_from_menu(menu_item):
        if menu_item == 3:
            update_game_stats()
        for i in range(len(frames)):
            if i != menu_item:
                frames[i].forget()
            else:
                frames[i].pack(fill="both", expand=1)

    # draw new set of winning numbers. Can only be used if game is reset
    def draw_new_set_of_winning_numbers():
        game_status = operations.read_gameinfo_json()
        if game_status["game"]["round_finished"] == False:
            messagebox.showerror("Error", "Round is not finished and no new numbers can be drawn")
            return
        game_options_text_area.delete(1.0, END)
        new_set_winning_numbers = ticket_operations.generate_winning_numbers()
        game_options_text_area.insert(1.0, "Wining numbers are:\n")
        for i in range(len(new_set_winning_numbers)):
            if i == len(new_set_winning_numbers) - 1:
                game_options_text_area.insert(tk.END, f"{new_set_winning_numbers[i]}")
            else:
                game_options_text_area.insert(tk.END, f"{new_set_winning_numbers[i]} - ")
        
        load_all_winning_numbers(False, True, new_set_winning_numbers)
        
    # update game stats which can change from each time the game stats window is opened
    def update_game_stats():
        global winning_numbers
        game_stats_text_area.delete(1.0, tk.END)
        total_users = user_operations.total_users
        total_active_tickets = ticket_operations.active_tickets
        total_archived_tickets = ticket_operations.archived_tickets
        total_income = ticket_operations.get_income()
        current_price_pool = ticket_operations.get_current_price_pool()
        jackpot = ticket_operations.get_jackpot()
        game_status = operations.read_gameinfo_json()
        game_stats_text_area.insert(tk.END, f"Total users: {total_users}\n"
                                    f"Current active tickets: {total_active_tickets}\n"
                                    f"Total archived tickets: {total_archived_tickets}\n"
                                    f"Total income: {total_income}\n"
                                    f"Current price pool: {current_price_pool}\n"
                                    f"Current jackpot: {jackpot}\n"
                                    f"Current winning numbers: {winning_numbers}\n"
                                    f"Round finished: {game_status['game']['round_finished']}")

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
            find_user_text_area.insert(1.0, f"User-ID: {user_id} created at {user_creation}\nName: {user_name} \nE-mail: {user_email}\n\n")
            find_user_text_area.insert(tk.END, "Current active tickets:\n")
            
            if len(user_active_tickets) != 0:
                for i in range(len(user_active_tickets)):
                    find_user_text_area.insert(tk.END, f"Ticket nr.{i+1}: ticket-id: {user_active_tickets[i]}\n")
            else:
                find_user_text_area.insert(tk.END, f"No active tickets\n")
            find_user_text_area.insert(tk.END, "\nArchived tickets:\n")

            find_user_text_area.insert(tk.END, f"No tickets in archive")

            find_user_name_entry.delete(0, tk.END)
            find_user_email_entry.delete(0, tk.END)
            find_user_user_id_entry.delete(0, tk.END)
    
    # reset Json-file
    def reset_json():
        game_info = operations.read_gameinfo_json()
        game_info["ticket_data"]["numbers_per_row"] = 8
        game_info["ticket_data"]["cost_per_row"] = 10
        game_info["ticket_data"]["max_playable_numbers"] = 40
        game_info["game"]["total_income"] = 0
        game_info["game"]["current_price_pool"] = 0
        game_info["game"]["jackpot"] = 0
        game_info["game"]["round_finished"] = True
        operations.write_to_json(game_info)
        print("Json-file reset")

    # find this rounds winners
    def find_winners():
        game_options_text_area.delete(1.0, tk.END)
        global winning_numbers
        game_info = operations.read_gameinfo_json()

        active_ticket_list = operations.read_database("t")
        if len(active_ticket_list) == 0:
            messagebox.showerror("Error", "There are no active tickets yet.")
            return
        
        #find tickets with winning set of numbers
        winners = ticket_operations.find_winning_tickets(winning_numbers)

        if len(winners) == 0:
            game_options_text_area.insert(1.0, f"No winners this round!\n")
            game_options_text_area.insert(tk.END, f"Jackpot for next round. {ticket_operations.get_current_price_pool()} added to jackpot.") 
            game_info["game"]["jackpot"] += ticket_operations.get_current_price_pool() # add current price pool to jackpot
            game_info["game"]["current_price_pool"] == 0 # reset current price pool to 0 for next round
        else:
            total_winnings = game_info['game']['current_price_pool'] + game_info['game']['jackpot']
            for i in range(len(winners)):
                game_options_text_area.insert(1.0, f"Ticket ID: {winners[i].get_ticket_id()} belonging to user {winners[i].get_user_id()} has won!\n")
            game_options_text_area.insert(tk.END, f"Prize money is {game_info['game']['current_price_pool']}")
            if game_info['game']['jackpot'] != 0:
                game_options_text_area.insert(tk.END, f"Jackpot is {game_info['game']['jackpot']}\n",
                                                f"Total prize: {total_winnings}")
            winnings_per_player = total_winnings / len(winners)
            game_options_text_area.insert(tk.END, f"Prize per winner: {winnings_per_player}")

        game_info["game"]["round_finished"] == False
        operations.write_to_json(game_info)
        ticket_operations.reset_game()

    #reset ticket-db
    def reset_ticket_db():
        ticket_operations.reset_database("t")
        ticket_operations.reset_database("a")
        ticket_operations.reset_database("w")
        print("ticket-dbs reset")
    
    #reset user-db
    def reset_user_db():
        user_operations.reset_database("u")
        print("user-db reset")
    
    # list all users
    def list_all_users():
        find_user_text_area.delete(1.0, tk.END)
        users = user_operations.read_database("u")
        for i in range(len(users)):
            find_user_text_area.insert(tk.END, f"User id: {users[i].get_user_id()}. Name: {users[i].get_name()}\n")
    
    # list all tickets
    def list_all_tickets():
        find_ticket_area.delete(1.0, tk.END)
        tickets = ticket_operations.read_database("t")
        for i in range(len(tickets)):
            if tickets[i].get_active() == True:
                find_ticket_area.insert(tk.END, f"Ticket ID: {tickets[i].get_ticket_id()} to user {tickets[i].get_user_id()}. Active: {tickets[i].get_active()} \n")
    
    # exit-button in menu
    def exit():
        sys.exit()

    load_all_winning_numbers(True, False, None)

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

    # buttons
    game_options_draw_winning_numbers_button = tk.Button(game_options_frame, text="Draw winning numbers", width=20, height=1, command=draw_new_set_of_winning_numbers)
    game_options_archived_winners_button = tk.Button(game_options_frame, text="List previous winners", width=20, height=1, command=list_archived_winning_numbers)
    game_options_draw_winners_button = tk.Button(game_options_frame, text="Weekly draw", width=20, height=1, command=find_winners)
    game_options_empty_ticketdb_button = tk.Button(game_options_frame, text="Reset ticket db", width=20, height=1, command=reset_ticket_db)
    game_options_empty_userdb_button = tk.Button(game_options_frame, text="Reset user db", width=20, height=1, command=reset_user_db)
    game_options_reset_json_button = tk.Button(game_options_frame, text="Reset JSON", width=20, height=1, command=reset_json)
    game_option_buttons = [game_options_draw_winning_numbers_button, game_options_archived_winners_button, game_options_draw_winners_button, game_options_empty_ticketdb_button, game_options_empty_userdb_button, game_options_reset_json_button]
    
    for i in range(len(game_option_buttons)):
        game_option_buttons[i].place(x=INITIAL_HORIZONTAL_WIDGET_PLACEMENT, y=vertical_placement)
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
    find_user_findall_button = tk.Button(find_user_frame, text="Print all users", width=10, height=1, command=list_all_users)
    find_user_findall_button.place(x=INITIAL_HORIZONTAL_WIDGET_PLACEMENT, y=250)
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
    find_ticket_listall_button = tk.Button(find_ticket_frame, text="List all tickets", width=10, height=1, command=list_all_tickets)
    find_ticket_button.place(x=INITIAL_HORIZONTAL_WIDGET_PLACEMENT, y=150)
    find_ticket_listall_button.place(x=INITIAL_HORIZONTAL_WIDGET_PLACEMENT, y=200)
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
