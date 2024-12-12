import tkinter as tk
import json
import os
from tkinter import ttk
import tkinter.messagebox as messagebox
import random 



# File to store user accounts and study sets
USER_DATA_FILE = "user_data.json"

# Function to load user data from the JSON file
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    return {}

# Function to save user data to the JSON file
def save_user_data(data):
    with open(USER_DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Function to create a new account
def create_account(username, password):
    user_data = load_user_data()
    if username in user_data:
        messagebox.showerror("Error", "Username already exists. Please choose a different username.")
        return False
    user_data[username] = {"password": password, "study_sets": []}  # Store study sets under the username
    save_user_data(user_data)
    messagebox.showinfo("Success", "Account created successfully!")
    return True

# Function to log in to an existing account
def login(username, password):
    user_data = load_user_data()
    if username in user_data and user_data[username]["password"] == password:
        return True
    else:
        return False
    

# QuizMaster GUI Application (Login Window)
class QuizMasterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QuizMaster")
        self.root.geometry("650x650")
        self.root.resizable(False, False)
        self.root.config(bg="#f8f9fa")

        # Header
        self.header = tk.Label(root, text="Login", font=("Arial", 24, "bold"), bg="#f8f9fa", fg="#495057")
        self.header.pack(pady=20)

        # Username field
        self.label_username = tk.Label(root, text="Username:", font=("Arial", 12), bg="#f8f9fa")
        self.label_username.pack(padx=20, anchor="w")

        self.entry_username = tk.Entry(root, font=("Arial", 14), bg="#ffffff", bd=2, relief="solid")
        self.entry_username.pack(padx=20, pady=5, fill="x")

        # Password field
        self.label_password = tk.Label(root, text="Password:", font=("Arial", 12), bg="#f8f9fa")
        self.label_password.pack(padx=20, anchor="w")

        self.entry_password = tk.Entry(root, font=("Arial", 14), bg="#ffffff", bd=2, relief="solid", show="*")
        self.entry_password.pack(padx=20, pady=5, fill="x")

        # Buttons
        self.button_login = ttk.Button(root, text="Login", command=self.handle_login, width=20, style="TButton")
        self.button_login.pack(pady=30)

        self.button_create = ttk.Button(root, text="Create Account", command=self.open_create_account_window, width=20, style="TButton")
        self.button_create.pack(pady=10)

    def handle_login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        if not username or not password:
            messagebox.showwarning("Warning", "Please enter both username and password.")
        else:
            if login(username, password):
                messagebox.showinfo("Welcome", f"Welcome, {username}!")
                self.open_main_window(username)  # Open the main window
                self.root.withdraw()  # Hide login window
            else:
                messagebox.showerror("Error", "Invalid username or password.")

    def open_create_account_window(self):
        self.new_window = tk.Toplevel(self.root)
        self.create_account_window = CreateAccountWindow(self.new_window, self.root)

    def open_main_window(self, username):
        self.new_window = tk.Toplevel(self.root)
        self.main_window = MainWindow(self.new_window, username, self.root)
     



# Main Window after login
class MainWindow:
    def __init__(self, root, username, login_window):
        self.root = root
        self.root.title("QuizMaster")
        self.root.geometry("650x650")
        self.root.resizable(False, False)
        self.root.config(bg="#f8f9fa")
        self.username = username
        self.login_window = login_window

        # Create custom styles for buttons
        self.style = ttk.Style()

        # Set style for main buttons (blue)
        self.style.configure("BlueButton.TButton", background="#007bff", foreground="Black", font=("Arial", 12), padding=(10, 10))

        # Set style for logout button (red)
        self.style.configure("RedButton.TButton", background="#dc3545", foreground="Black", font=("Arial", 12), padding=(10, 10))
        
        # Create a frame for the main content
        self.main_frame = tk.Frame(self.root, bg="#f8f9fa")  
        self.main_frame.pack(fill="both", expand=True)

        # Home button (upper left)
        self.home_button = ttk.Button(self.main_frame, text="Home", command=self.go_home, style="BlueButton.TButton", width=10)
        self.home_button.place(x=10, y=10)

        # Logout button (upper right)
        self.logout_button = ttk.Button(self.main_frame, text="Logout", command=self.logout, style="RedButton.TButton", width=10)
        self.logout_button.place(x=520, y=10)

        # Welcome message
        self.welcome_label = tk.Label(self.main_frame, text="Welcome to QuizMaster!", font=("Arial", 18), bg="#f8f9fa", fg="Black")
        self.welcome_label.pack(pady=40)

        # Create a Frame for Buttons (center part)
        self.button_frame = tk.Frame(self.main_frame, bg="#f8f9fa")
        self.button_frame.pack(pady=20)

        # "Your Library" button (left center)
        self.library_button = ttk.Button(self.button_frame, text="Your Library", command=self.open_library, style="BlueButton.TButton", width=10)
        self.library_button.grid(row=0, column=0, padx=85, pady=100)

        # Add the background image
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)  # Set to fill the window

        # Create custom styles for 

        # "Practice Test" button (right center)
    
    def go_home(self):
        messagebox.showinfo("Home", "You are already on the Home Page!")

    def logout(self):
        self.root.destroy()
        self.login_window.deiconify()  # Show the login window again

    def open_library(self):
        self.new_window = tk.Toplevel(self.root)
        self.library_window = LibraryWindow(self.new_window, self.username, self.login_window)

    
class LibraryWindow:
    def __init__(self, root, username, main_window):
        self.root = root
        self.root.title("QuizMaster")
        self.root.geometry("650x650")
        self.root.resizable(False, False)
        self.root.config(bg="#f8f9fa")
        self.username = username
        self.main_window = main_window  # Pass MainWindow reference

        # Create a frame for the main content
        self.main_frame = tk.Frame(self.root, bg="#f8f9fa")
        self.main_frame.pack(fill="both", expand=True)
        

        # Home button (upper left)
        self.home_button = ttk.Button(self.main_frame, text="Home", command=self.go_home, style="BlueButton.TButton", width=10)
        self.home_button.place(x=10, y=10)

        # History button (bottom left)
        self.history_button = ttk.Button(self.main_frame, text="History", command=self.show_history, style="BlueButton.TButton", width=10)
        self.history_button.place(x=250, y=350)

        # Welcome message
        self.welcome_label = tk.Label(self.main_frame, text="Library", font=("Arial", 20), bg="#f8f9fa", fg="Black")
        self.welcome_label.pack(pady=40)

        # Create Study Set Button (plus sign) in lower-right corner
        self.create_study_set_button = ttk.Button(self.main_frame, text="+ create a study set", command=self.open_create_study_set_window, style="BlueButton.TButton", width=17)
        self.create_study_set_button.place(x=450, y=500)  # Positioned at the bottom-right corner

        # Remove Study Set Button (minus sign) in lower-left corner
        self.remove_study_set_button = ttk.Button(self.main_frame, text="- remove study set(s)", command=self.toggle_remove_mode, style="BlueButton.TButton", width=17)
        self.remove_study_set_button.place(x=10, y=500)  # Positioned at the bottom-left corner

        # Take Quiz Button (upper-right corner)
        self.take_quiz_button = ttk.Button(self.main_frame, text="Take a Quiz", command=self.take_quiz, style="BlueButton.TButton", width=17)
        self.take_quiz_button.place(x=450, y=10)

        # Frame for the Listbox and scrollbar
        self.study_sets_frame = tk.Frame(self.main_frame, bg="#f8f9fa")
        self.study_sets_frame.pack(pady=20)

        # Create a Listbox with a scrollbar
        self.study_sets_listbox = tk.Listbox(self.study_sets_frame, selectmode=tk.SINGLE, width=50, height=10, font=("Arial", 12))
        self.study_sets_listbox.grid(row=0, column=0, padx=10, pady=5)

        self.scrollbar = ttk.Scrollbar(self.study_sets_frame, orient="vertical", command=self.study_sets_listbox.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.study_sets_listbox.config(yscrollcommand=self.scrollbar.set)

        # Load and display study sets
        self.load_study_sets()

        # A button to confirm deletion after selecting multiple sets
        self.delete_button = ttk.Button(self.main_frame, text="Delete Selected", command=self.delete_selected_study_sets, state="disabled", style="BlueButton.TButton", width=17)
        self.delete_button.place(x=200, y=500)

        # Flag to check if remove mode is active
        self.remove_mode_active = False

        # Bind the listbox selection event to open the study set details on double-click
        self.study_sets_listbox.bind("<Double-1>", self.on_study_set_double_click)


    def show_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("Quiz History")
        history_window.geometry("650x650")
        self.root.resizable(False, False)
        history_window.config(bg="#f8f9fa")

        # Frame for the history listbox and scrollbar
        history_frame = tk.Frame(history_window, bg="#f8f9fa")
        history_frame.pack(pady=20)

        # Create a Listbox with a scrollbar and single selection (default)
        history_listbox = tk.Listbox(history_frame, width=60, height=15, font=("Arial", 12), selectmode=tk.SINGLE)  # Initially SINGLE selection
        history_listbox.grid(row=0, column=0, padx=10, pady=10)

        history_scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=history_listbox.yview)
        history_scrollbar.grid(row=0, column=1, sticky="ns")

        history_listbox.config(yscrollcommand=history_scrollbar.set)

        # Update the listbox with the history data after it's been initialized
        self.update_history_listbox(history_listbox)

        # Flag to track if multi-selection mode is active
        self.multi_select_active = False  

        # Function to toggle between single and multiple selection modes
        def toggle_multi_select():
            if self.multi_select_active:
                history_listbox.config(selectmode=tk.SINGLE)  # Switch to single selection
                self.multi_select_active = False
                delete_button.config(state="disabled")  # Disable delete button when in single select mode
            else:
                history_listbox.config(selectmode=tk.MULTIPLE)  # Switch to multiple selection
                self.multi_select_active = True
                delete_button.config(state="normal")  # Enable delete button when in multi select mode

        # Delete button to remove selected scores
        def delete_score():
            selected_items = history_listbox.curselection()  # Get all selected items
            if not selected_items:
                messagebox.showwarning("Warning", "Please select scores to delete.")
                return

            # Sort selected items in reverse order to avoid index shifting during deletion
            selected_items = sorted(selected_items, reverse=True)

            user_data = self.load_user_data()
            history = user_data.get(self.username, {}).get("history", [])

            # Remove the selected items from the history
            for index in selected_items:
                del history[index]

            # Update user data file with the modified history
            user_data[self.username]["history"] = history
            self.save_user_data(user_data)

            # Refresh the listbox after deletion
            self.update_history_listbox(history_listbox)

            # Switch back to single selection mode after deletion
            history_listbox.config(selectmode=tk.SINGLE)
            self.multi_select_active = False
            delete_button.config(state="disabled")

        # Create a Toggle Selection button
        toggle_button = ttk.Button(history_window, text="Select Multiple", command=toggle_multi_select, style="BlueButton.TButton", width=12)
        toggle_button.place(x=500, y=400)

        # Create a Delete button to delete selected scores (initially disabled)
        delete_button = ttk.Button(history_window, text="Delete", command=delete_score, style="BlueButton.TButton", width=10, state="disabled")
        delete_button.place(x=500, y=350)

        # Home button to navigate back to the main window
        def return_to_home():
            history_window.destroy()  # Close the history window

        home_button = ttk.Button(history_window, text="Home", command=return_to_home, style="BlueButton.TButton", width=10)
        home_button.place(x=40, y=350)

    # Other existing methods (load_user_data, save_user_data, etc.) go here...

    def go_home(self):
        """Returns to the home window."""
        self.main_frame.pack_forget()
        self.__init__(self.root, self.username, self.main_window)
        self.root.destroy()  # Close the current window
        

    def take_quiz(self):
        """Starts the quiz based on the selected study set."""
        selected_items = self.study_sets_listbox.curselection()

        if not selected_items:
            messagebox.showwarning("Warning", "Please select a study set to take the quiz.")
            return

        # Get the selected study set name
        study_set_text = self.study_sets_listbox.get(selected_items[0])
        study_set_name = study_set_text.split(" ")[0]  # Assuming name is the first word

        # Fetch the questions for the selected study set
        user_data = self.load_user_data()
        study_sets = user_data.get(self.username, {}).get("study_sets", [])
        questions = []

        for study_set in study_sets:
            if study_set["name"] == study_set_name:
                questions = study_set.get("questions", [])

        if not questions:
            messagebox.showwarning("Warning", "This study set has no questions.")
            return
        
        random.shuffle(questions)
        # Start the quiz
        self.start_quiz(study_set_name, questions)

    def start_quiz(self, study_set_name, questions):
        """Displays questions and takes the quiz."""
        self.quiz_window = tk.Toplevel(self.root)
        self.quiz_window.title(f"Quiz - {study_set_name}")
        self.quiz_window.geometry("650x650")
        self.root.resizable(False, False)
        self.quiz_window.config(bg="#f8f9fa")

        question_index = 0
        score = 0

        def return_to_home():
         self.quiz_window.destroy()
         self.go_home()


        # Show the first question
        def next_question():
            nonlocal question_index, score

            # Get the user's answer
            answer = answer_entry.get()

            if answer.strip().lower() == questions[question_index]["answer"].strip().lower():
                score += 1

            question_index += 1

            if question_index < len(questions):
                # Show the next question
                question_label.config(text=f"Q{question_index + 1}: {questions[question_index]['question']}")
                answer_entry.delete(0, tk.END)
            else:
                # Quiz is over, show the score
                messagebox.showinfo("Quiz Complete", f"Your score: {score}/{len(questions)}")
                self.save_score(study_set_name, score)

                # Close the quiz window
                self.quiz_window.destroy()

                # After the quiz window is closed, go back to the main window
                self.quiz_window.after(100, self.go_home)

        # Display question and answer entry
        question_label = tk.Label(self.quiz_window, text=f"Q1: {questions[question_index]['question']}", font=("Arial", 14), bg="#f8f9fa")
        question_label.pack(pady=50)

        answer_entry = tk.Entry(self.quiz_window, font=("Arial", 12), width=40)
        answer_entry.pack(pady=10)

        # Next question button
        next_button = ttk.Button(self.quiz_window, text="Next", command=next_question, style="BlueButton.TButton", width=10)
        next_button.pack(pady=20)
       
        home_button = ttk.Button(self.quiz_window, text="Home", command=return_to_home, style="BlueButton.TButton", width=10)
        home_button.place(x=10, y=10)
        
    def save_score(self, study_set_name, score):
       """Save the score to the user's history and update the history listbox."""
       user_data = self.load_user_data()
       history = user_data.get(self.username, {}).get("history", [])

       total_questions = len([q for q in self.load_user_data().get(self.username, {}).get("study_sets", []) if q['name'] == study_set_name][0].get('questions', []))

    # Save score and total questions to history
       history.append({
        "study_set": study_set_name,
        "score": score,
        "total_questions": total_questions
    })

       user_data[self.username]["history"] = history
       self.save_user_data(user_data)

    # Update the history listbox with the new score
       self.update_history_listbox()

    def load_user_data(self):
        """Load user data from file (for demonstration purposes)."""
        try:
            with open(f'{self.username}_data.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_user_data(self, user_data):
        """Save the user data to file."""
        with open(f'{self.username}_data.json', 'w') as file:
            json.dump(user_data, file, indent=4)

    def update_history_listbox(self, history_listbox):
        """Update the history listbox with history data."""
        history_listbox.delete(0, tk.END)

        user_data = self.load_user_data()
        history = user_data.get(self.username, {}).get("history", [])

        for idx, entry in enumerate(history, start=1):
        # Format each entry as number. (Studyset) - (Score/Items)
           study_set_name = entry['study_set']
           score = entry['score']
           total_questions = entry['total_questions']
           history_listbox.insert(tk.END, f"{idx}.({study_set_name}) - ({score}/{total_questions})")
       

    def on_study_set_double_click(self, event):
        """Handles double-clicking a study set in the listbox."""
        # Get the selected study set name
        selection = self.study_sets_listbox.curselection()
        if selection:
            study_set_text = self.study_sets_listbox.get(selection[0])
            study_set_name = study_set_text.split(" ")[0]  # Assuming name is the first word
            self.open_study_set_window(study_set_name)
        
    def open_create_study_set_window(self):
        """Opens a new window to create a study set."""
        self.new_window = tk.Toplevel(self.root)
        self.create_study_set_window = CreateStudySetWindow(self.new_window, self.username, self)

    def load_study_sets(self):
        """Loads and displays the user's study sets."""
        # Load user data to get the list of study sets
        user_data = load_user_data()
        study_sets = user_data.get(self.username, {}).get("study_sets", [])

        # Clear the previous list of study sets (if any)
        self.study_sets_listbox.delete(0, tk.END)

        # Display each study set in the Listbox
        for study_set in study_sets:
            study_set_name = study_set.get("name", "Unnamed")
            study_set_subject = study_set.get("subject", "No subject")
            self.study_sets_listbox.insert(tk.END, f"{study_set_name} ({study_set_subject})")

        # If no study sets are found, display a message
        if not study_sets:
            self.study_sets_listbox.insert(tk.END,)
    def toggle_remove_mode(self):
        """Toggles the removal mode where users can select multiple study sets to remove."""
        if self.remove_mode_active:
            # Disable removal mode (return to single selection)
            self.study_sets_listbox.config(selectmode=tk.SINGLE)
            self.delete_button.config(state="disabled")  # Disable the Delete button
        else:
            # Enable removal mode (allow multiple selection)
            self.study_sets_listbox.config(selectmode=tk.MULTIPLE)
            self.delete_button.config(state="normal")  # Enable the Delete button

        # Toggle the flag
        self.remove_mode_active = not self.remove_mode_active

    def delete_selected_study_sets(self):
        """Deletes the selected study sets after confirmation."""
        selected_items = self.study_sets_listbox.curselection()

        if not selected_items:
            messagebox.showwarning("Warning", "Please select at least one study set to remove.")
            return

        # Ask for confirmation before deleting
        selected_names = [self.study_sets_listbox.get(i).split(" ")[0] for i in selected_items]
        confirm_message = "Are you sure you want to remove the following study sets?\n" + "\n".join(selected_names)

        if messagebox.askyesno("Confirm Removal", confirm_message):
            # Remove the selected study sets from user data
            study_sets = load_user_data().get(self.username, {}).get("study_sets", [])
            study_sets_to_remove = [ss for ss in study_sets if ss["name"] in selected_names]

            # Remove each selected study set from the file system
            for study_set in study_sets_to_remove:
                study_set_name = study_set["name"]
                study_set_folder = os.path.join("Library", self.username, study_set_name)

                if os.path.exists(study_set_folder):
                    for root, dirs, files in os.walk(study_set_folder, topdown=False):
                        for file in files:
                            os.remove(os.path.join(root, file))
                        for dir in dirs:
                            os.rmdir(os.path.join(root, dir))
                    os.rmdir(study_set_folder)

            # Remove the study sets from user data
            user_data = load_user_data()
            user_data[self.username]["study_sets"] = [ss for ss in user_data[self.username]["study_sets"] if ss["name"] not in selected_names]
            save_user_data(user_data)

            # Refresh the library window
            self.refresh_study_sets()
            messagebox.showinfo("Success", "Selected study set(s) removed successfully!")

            # Disable the Delete button and revert listbox selection mode
            self.delete_button.config(state="disabled")
            self.study_sets_listbox.config(selectmode=tk.SINGLE)
            self.remove_mode_active = False
        else:
            messagebox.showinfo("Cancelled", "Study set removal cancelled.")

    def refresh_study_sets(self):
        """Refreshes the study sets list after a new set is added or removed."""
        self.load_study_sets()  # Reload the list of study sets

    def open_study_set_window(self, study_set_name):
        """Open a window that displays the study set information and allows adding/removing reviewers."""
        # Create a new window to display the study set information
        study_set_window = tk.Toplevel(self.root)
        study_set_window.title("QuizMaster")
        study_set_window.geometry("650x650")
        self.root.resizable(False, False)
        study_set_window.config(bg="#f8f9fa")

        # Add a Home button to return to the library
        home_button = ttk.Button(study_set_window, text="Home", command=study_set_window.destroy, style="BlueButton.TButton", width=10)
        home_button.place(x=10, y=10)

        # Display the study set details (name and subject)
        study_set_label = tk.Label(study_set_window, text="Reviewer List", font=("Arial", 18), bg="#f8f9fa")
        study_set_label.pack(pady=50)

        # Load the study set details from user data
        user_data = self.load_user_data()
        study_sets = user_data.get(self.username, {}).get("study_sets", [])
        questions = []

        for study_set in study_sets:
            if study_set["name"] == study_set_name:
                questions = study_set.get("questions", [])

        # Frame to hold the listbox and scrollbar
        listbox_frame = tk.Frame(study_set_window, bg="#f8f9fa")
        listbox_frame.pack(pady=20)

        # Create the Listbox for reviewers
        self.reviewer_listbox = tk.Listbox(listbox_frame, height=15, width=60, selectmode=tk.SINGLE, font=("Arial", 12))
        self.reviewer_listbox.grid(row=0, column=0, padx=10, pady=5)

        # Create a vertical scrollbar linked to the listbox
        self.scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical", command=self.reviewer_listbox.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # Link the scrollbar to the listbox
        self.reviewer_listbox.config(yscrollcommand=self.scrollbar.set)



        # Insert questions and answers into the listbox in the desired format
        for idx, qa in enumerate(questions, 1):
            self.reviewer_listbox.insert(tk.END, f"{idx}. Question: {qa['question']}")
            self.reviewer_listbox.insert(tk.END, f"   Answer: {qa['answer']}")
           

        # Add "Add Reviewer" button
        add_reviewer_button = ttk.Button(study_set_window, text="+ Add Reviewer", command=lambda: self.add_reviewer(study_set_name), style="BlueButton.TButton", width=17)
        add_reviewer_button.place(x=450, y=500)

        # Add "Remove Reviewer" button
        remove_reviewer_button = ttk.Button(study_set_window, text="- Remove Reviewer", command=lambda: self.remove_reviewer(study_set_name), style="BlueButton.TButton", width=17)
        remove_reviewer_button.place(x=10, y=500)

    def remove_reviewer(self, study_set_name):
        """Toggle multiple selection mode to allow removing multiple questions and answers."""
        if not hasattr(self, 'remove_mode_active'):
            self.remove_mode_active = False  # Initialize the flag if not present

        if self.remove_mode_active:
            # Remove selected questions and answers
            selected_items = self.reviewer_listbox.curselection()

            if not selected_items:
                messagebox.showwarning("Warning", "Please select at least one question-answer pair to remove.")
                return

            # Determine indices of the selected question-answer pairs
            selected_indices = sorted(set(i // 4 for i in selected_items))  # Groups of 4 rows per Q&A

            # Load user data and find the study set
            user_data = self.load_user_data()
            study_sets = user_data.get(self.username, {}).get("study_sets", [])

            for study_set in study_sets:
                if study_set["name"] == study_set_name:
                    # Remove the selected question-answer pairs
                    if "questions" in study_set:
                        for index in sorted(selected_indices, reverse=True):
                            if 0 <= index < len(study_set["questions"]):
                                removed_question = study_set["questions"].pop(index)

                        # Save updated data back to the database
                        self.save_user_data(user_data)

                        # Refresh the Listbox
                        self.reviewer_listbox.delete(0, tk.END)
                        for idx, qa in enumerate(study_set["questions"], 1):
                            self.reviewer_listbox.insert(tk.END, f"{idx}. Question:")
                            self.reviewer_listbox.insert(tk.END, f"   {qa['question']}")
                            self.reviewer_listbox.insert(tk.END, "   Answer:")
                            self.reviewer_listbox.insert(tk.END, f"   {qa['answer']}")

                        messagebox.showinfo("Success", "Selected questions removed successfully!")
                        break
            else:
                messagebox.showerror("Error", "Could not find the study set or remove selected questions.")

            # Revert to single selection mode
            self.reviewer_listbox.config(selectmode=tk.SINGLE)
            self.remove_mode_active = False
        else:
            # Activate multiple selection mode
            self.reviewer_listbox.config(selectmode=tk.MULTIPLE)
            self.remove_mode_active = True
            messagebox.showinfo("Info", "Click again the remove reviewer button if you selected .")


    def add_reviewer(self, study_set_name):
        """Handles adding a list of questions and answers directly, with copy-paste functionality."""
        # Create a new window for adding questions and answers
        add_window = tk.Toplevel(self.root)
        add_window.title("Quiz Master")
        add_window.geometry("650x650")
        self.root.resizable(False, False)
        add_window.config(bg="#f8f9fa")

        # Title label
        tk.Label(add_window, text=f"Add Questions and Answers for '{study_set_name}'", font=("Arial", 14), bg="#f8f9fa").pack(pady=10)

        # Frame for input fields
        input_frame = tk.Frame(add_window, bg="#f8f9fa")
        input_frame.pack(pady=10, fill="x")

        # Question input (large text box)
        tk.Label(input_frame, text="Question:", bg="#f8f9fa").grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        question_text = tk.Text(input_frame, width=60, height=5, wrap="word")
        question_text.grid(row=0, column=1, padx=5, pady=5)

        # Answer input (large text box)
        tk.Label(input_frame, text="Answer:", bg="#f8f9fa").grid(row=1, column=0, padx=5, pady=5, sticky="nw")
        answer_text = tk.Text(input_frame, width=60, height=5, wrap="word")
        answer_text.grid(row=1, column=1, padx=5, pady=5)

        # Add right-click menu for copy-paste
        def create_context_menu(widget):
            context_menu = tk.Menu(widget, tearoff=0)
            context_menu.add_command(label="Cut", command=lambda: widget.event_generate("<<Cut>>"))
            context_menu.add_command(label="Copy", command=lambda: widget.event_generate("<<Copy>>"))
            context_menu.add_command(label="Paste", command=lambda: widget.event_generate("<<Paste>>"))
            context_menu.add_command(label="Select All", command=lambda: widget.tag_add("sel", "1.0", "end"))

            def show_context_menu(event):
                context_menu.post(event.x_root, event.y_root)

            widget.bind("<Button-3>", show_context_menu)  # Right-click to open the menu

        # Attach the context menu to the Text widgets
        create_context_menu(question_text)
        create_context_menu(answer_text)

        # Frame for buttons
        button_frame = tk.Frame(add_window, bg="#f8f9fa")
        button_frame.pack(pady=20)

        # Function to add the current Q&A
        def add_question_answer():
            question = question_text.get("1.0", tk.END).strip()
            answer = answer_text.get("1.0", tk.END).strip()

            if question and answer:
                # Update the study set with the new Q&A data
                user_data = self.load_user_data()
                study_sets = user_data.get(self.username, {}).get("study_sets", [])

                for study_set in study_sets:
                    if study_set["name"] == study_set_name:
                        if "questions" not in study_set:
                            study_set["questions"] = []  # Initialize the questions list if not present
                        study_set["questions"].append({"question": question, "answer": answer})

                # Save the updated user data back to the file
                self.save_user_data(user_data)

                # Clear the input fields for the next question
                question_text.delete("1.0", tk.END)
                answer_text.delete("1.0", tk.END)

                # Refresh the reviewer listbox in the parent window
                self.reviewer_listbox.delete(0, tk.END)  # Clear the Listbox
                updated_questions = [
                    q for s in study_sets if s["name"] == study_set_name for q in s.get("questions", [])
                ]
                for idx, qa in enumerate(updated_questions, 1):
                    self.reviewer_listbox.insert(tk.END, f"{idx}. Question:")
                    self.reviewer_listbox.insert(tk.END, f"   {qa['question']}")
                    self.reviewer_listbox.insert(tk.END, "   Answer:")
                    self.reviewer_listbox.insert(tk.END, f"   {qa['answer']}")

                # Show confirmation for each addition
                messagebox.showinfo("Success", "Question and answer added successfully!")
            else:
                messagebox.showwarning("Warning", "Both question and answer are required!")

        # Add button to add the Q&A
        add_button = ttk.Button(button_frame, text="Add", command=add_question_answer, style="BlueButton.TButton", width=10)
        add_button.grid(row=0, column=0, padx=10)

        # Close button to finish adding Q&A
        close_button = ttk.Button(button_frame, text="Close", command=add_window.destroy, style="BlueButton.TButton", width=10)
        close_button.grid(row=0, column=1, padx=10)


    def load_user_data(self):
        try:
            with open("user_data.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_user_data(self, data):
        with open("user_data.json", "w") as f:
            json.dump(data, f, indent=4)

    def on_study_set_double_click(self, event):
        """Handles double-clicking a study set in the listbox."""
        # Get the selected study set name
        selection = self.study_sets_listbox.curselection()
        if selection:
            study_set_text = self.study_sets_listbox.get(selection[0])
            study_set_name = study_set_text.split(" ")[0]  # Assuming name is the first word
            self.open_study_set_window(study_set_name)


class CreateAccountWindow:
    def __init__(self, root, login_window):
        self.root = root
        self.login_window = login_window
        self.root.title("Quiz Master")
        self.root.geometry("650x650")
        self.root.resizable(False, False)
        self.root.config(bg="#f8f9fa")

        # Header
        self.header = tk.Label(root, text="Create Account", font=("Arial", 24, "bold"), bg="#f8f9fa", fg="#495057")
        self.header.pack(pady=20)

        # Username field
        self.label_username = tk.Label(root, text="Username:", font=("Arial", 12), bg="#f8f9fa")
        self.label_username.pack(padx=20, anchor="w")

        self.entry_username = tk.Entry(root, font=("Arial", 14), bg="#ffffff", bd=2, relief="solid")
        self.entry_username.pack(padx=20, pady=5, fill="x")

        # Password field
        self.label_password = tk.Label(root, text="Password:", font=("Arial", 12), bg="#f8f9fa")
        self.label_password.pack(padx=20, anchor="w")

        self.entry_password = tk.Entry(root, font=("Arial", 14), bg="#ffffff", bd=2, relief="solid", show="*")
        self.entry_password.pack(padx=20, pady=5, fill="x")

        # Create button
        self.button_create = ttk.Button(root, text="Create", command=self.create_account, width=20)
        self.button_create.pack(pady=30)

        # Back to login button
        self.button_back = ttk.Button(root, text="Back", command=self.go_back, width=10)
        self.button_back.pack(pady=10)

    def create_account(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        if not username or not password:
            messagebox.showwarning("Warning", "Please enter both username and password.")
        else:
            if create_account(username, password):
                self.root.destroy()  # Close the create account window
                self.login_window.deiconify()  # Show login window again

    def go_back(self):
        self.root.destroy()
        self.login_window.deiconify()  # Show the login window again

# Create Study Set Window
class CreateStudySetWindow:
    def __init__(self, root, username, library_window):
        self.root = root
        self.root.title("Quiz Master")
        self.root.geometry("650x650")
        self.root.resizable(False, False)
        self.root.config(bg="#f8f9fa")
        self.username = username
        self.library_window = library_window

        # Study Set Name
        self.label_name = tk.Label(root, text="Subject:", font=("Arial", 12), bg="#f8f9fa")
        self.label_name.pack(padx=20, anchor="w")

        self.entry_name = tk.Entry(root, font=("Arial", 14), bg="#ffffff", bd=2, relief="solid")
        self.entry_name.pack(padx=20, pady=5, fill="x")

        # Subject
        self.label_subject = tk.Label(root, text="Topic:", font=("Arial", 12), bg="#f8f9fa")
        self.label_subject.pack(padx=20, anchor="w")

        self.entry_subject = tk.Entry(root, font=("Arial", 14), bg="#ffffff", bd=2, relief="solid")
        self.entry_subject.pack(padx=20, pady=5, fill="x")

        # Create Button
        self.create_button = ttk.Button(root, text="Create", command=self.create_study_set, style="BlueButton.TButton", width=20)
        self.create_button.pack(pady=30)

        # Back Button
        self.button_back = ttk.Button(root, text="Back", command=self.go_back, style="BlueButton.TButton", width=10)
        self.button_back.pack(pady=10)

    def create_study_set(self):
        name = self.entry_name.get().strip()
        subject = self.entry_subject.get().strip()

        if not name or not subject:
            messagebox.showwarning("Warning", "Please fill in all fields.")
        else:
            # Create folder and save study set data
            study_set_folder = os.path.join("Library", self.username, name)
            if not os.path.exists(study_set_folder):
                os.makedirs(study_set_folder)

            study_set_data = {
                "name": name,
                "subject": subject
            }

            study_set_file = os.path.join(study_set_folder, "study_set.json")
            with open(study_set_file, "w") as file:
                json.dump(study_set_data, file, indent=4)

            # Update user data
            user_data = load_user_data()
            if self.username not in user_data:
                messagebox.showerror("Error", "User not found.")
                return
            user_data[self.username]["study_sets"].append({"name": name, "subject": subject})
            save_user_data(user_data)

            # Refresh the LibraryWindow to show the newly added study set
            self.library_window.refresh_study_sets()

            messagebox.showinfo("Success", "Study set created successfully!")
            self.root.destroy()

    def go_back(self):
        self.root.destroy()



if __name__ == "__main__":
    root = tk.Tk()
    app = QuizMasterApp(root)
    root.mainloop() 