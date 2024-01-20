import json
import os
from datetime import datetime

class Note:
    def __init__(self, note_id, title, body, timestamp):
        self.note_id = note_id
        self.title = title
        self.body = body
        self.timestamp = timestamp

class NotesApp:
    def __init__(self, storage_file="notes.json"):
        self.storage_file = storage_file
        self.notes = []
        self.load_notes()

    def load_notes(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, "r") as file:
                data = json.load(file)
                self.notes = [Note(**note_data) for note_data in data]

    def save_notes(self):
        data = [{"note_id": note.note_id, "title": note.title, "body": note.body, "timestamp": note.timestamp}
                for note in self.notes]
        with open(self.storage_file, "w") as file:
            json.dump(data, file, indent=2)

    def add_note(self, title, body):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_note = Note(len(self.notes) + 1, title, body, timestamp)
        self.notes.append(new_note)
        self.save_notes()
        print(f"Note added successfully:\n{new_note.__dict__}")

    def view_notes(self):
        if not self.notes:
            print("No notes available.")
        else:
            for note in self.notes:
                print(note.__dict__)

    def edit_note(self, note_id, new_title, new_body):
        for note in self.notes:
            if note.note_id == note_id:
                note.title = new_title
                note.body = new_body
                note.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.save_notes()
                print(f"Note {note_id} edited successfully:\n{note.__dict__}")
                return
        print(f"Note with ID {note_id} not found.")

    def delete_note(self, note_id):
        self.notes = [note for note in self.notes if note.note_id != note_id]
        self.save_notes()
        print(f"Note {note_id} deleted successfully.")

    def filter_notes_by_date(self, start_date, end_date):
        start_datetime = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
        end_datetime = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")

        filtered_notes = [note for note in self.notes if start_datetime <= datetime.strptime(note.timestamp, "%Y-%m-%d %H:%M:%S") <= end_datetime]

        if not filtered_notes:
            print("No notes found within the specified date range.")
        else:
            for note in filtered_notes:
                print(note.__dict__)

if __name__ == "__main__":
    app = NotesApp()

    while True:
        print("\nCommands:")
        print("1. Add Note")
        print("2. View Notes")
        print("3. Edit Note")
        print("4. Delete Note")
        print("5. Search")
        print("6. Exit")
        
        choice = input("Enter the command number: ")

        if choice == "1":
            title = input("Enter note title: ")
            body = input("Enter note body: ")
            app.add_note(title, body)
        elif choice == "2":
            app.view_notes()
        elif choice == "3":
            note_id = int(input("Enter the ID of the note to edit: "))
            new_title = input("Enter new title: ")
            new_body = input("Enter new body: ")
            app.edit_note(note_id, new_title, new_body)
        elif choice == "4":
            note_id = int(input("Enter the ID of the note to delete: "))
            app.delete_note(note_id)
        elif choice == "5":
            start_date = input("Enter the start date (YYYY-MM-DD HH:MM:SS): ")
            end_date = input("Enter the end date (YYYY-MM-DD HH:MM:SS): ")
            app.filter_notes_by_date(start_date, end_date)
        elif choice == "6":
            print("Exiting the Notes App. Goodbye!")
            break
        else:
            print("Invalid command. Please choose a valid option.")
