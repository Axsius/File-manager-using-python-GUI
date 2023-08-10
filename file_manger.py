import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os


class FileManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("File Manager")
        self.root.configure(background='#000000')  # Red background
        self.toolbar = tk.Frame(self.root)
        self.toolbar.pack(side=tk.TOP, fill=tk.X, pady=10)  # Increased top padding
        
        self.current_path = tk.StringVar()
        self.current_path.set(os.getcwd())
        
        self.path_label = tk.Label(self.toolbar, textvariable=self.current_path, bg="#000000", anchor="w", padx=10, fg='Red')  # Green text
        self.path_label.pack(fill=tk.X)
        
        self.back_button = tk.Button(self.toolbar, text="Back", command=self.go_back, bg='#000000', fg='#00FF00')  # Black button, green text
        self.back_button.pack(side=tk.LEFT, padx=10)
        

        
        self.file_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE, bg="#000000", fg="#00FF00")
        self.file_listbox.pack(fill=tk.BOTH, expand=True)
        
        self.create_file_button = tk.Button(self.toolbar, text="Create File", command=self.create_file, bg='#000000', fg='#00FF00')  # Black button, green text
        self.create_file_button.pack(side=tk.LEFT, padx=10)
        
        self.write_file_button = tk.Button(self.toolbar, text="Write to File", command=self.write_file, bg='#000000', fg='#00FF00')  # Black button, green text
        self.write_file_button.pack(side=tk.LEFT, padx=10)
        
        self.read_file_button = tk.Button(self.toolbar, text="Read File", command=self.read_file, bg='#000000', fg='#00FF00')  # Black button, green text
        self.read_file_button.pack(side=tk.LEFT, padx=10)
        
        self.delete_file_button = tk.Button(self.toolbar, text="Delete File", command=self.delete_file, bg='#000000', fg='#00FF00')  # Black button, green text
        self.delete_file_button.pack(side=tk.LEFT)
        
        self.permission_button = tk.Button(self.toolbar, text="Set Permissions", command=self.set_permissions, bg='#000000', fg='#00FF00')  # Black button, green text
        self.permission_button.pack(side=tk.LEFT)

        self.refresh_button = tk.Button(self.toolbar, text="Hidden directory", command=self.list_hidden_files, bg='#000000', fg='#00FF00')  # Black button, green text
        self.refresh_button.pack(side=tk.LEFT)

        self.create_file_button.pack(side=tk.LEFT, padx=5)
        self.write_file_button.pack(side=tk.LEFT, padx=5)
        self.read_file_button.pack(side=tk.LEFT, padx=5)
        self.delete_file_button.pack(side=tk.LEFT, padx=5)
        self.permission_button.pack(side=tk.LEFT, padx=5)
        self.refresh_button.pack(side=tk.LEFT, padx=5)  # Adjusted padding


        self.load_current_directory()
        self.file_listbox.bind('<Double-1>', self.on_listbox_double_click)
        
        
    def load_current_directory(self):
        self.current_path.set(os.getcwd())
        self.file_listbox.delete(0, tk.END)
        
        for item in os.listdir():
            self.file_listbox.insert(tk.END, item)
        
    def go_back(self):
        current_path = self.current_path.get()
        parent_dir = os.path.dirname(current_path)
        os.chdir(parent_dir)
        self.load_current_directory()
        
    def refresh(self):
        self.load_current_directory()
        
    def on_listbox_double_click(self, event):
        selected_item = self.file_listbox.get(tk.ACTIVE)
        full_path = os.path.join(self.current_path.get(), selected_item)
        
        if os.path.isdir(full_path):
            os.chdir(full_path)
            self.load_current_directory()
        
        elif os.path.isfile(full_path):
            content = self.read_file(full_path)
            self.show_file_content(selected_item, content)

    def list_hidden_files(self):
        files = os.listdir('.')
        hidden_files = [f for f in files if f.startswith('.')]
        tk.messagebox.showinfo("Hidden Files", hidden_files)
        
    def read_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r') as f:

                content = f.read()
            tk.messagebox.showinfo("File Content", content)


    def write_file(self):
        selected_item = self.file_listbox.get(tk.ACTIVE)
        full_path = os.path.join(self.current_path.get(), selected_item)
        
        if os.path.isfile(full_path):
            content = simpledialog.askstring("Write to File", f"Enter content for '{selected_item}':")
            if content is not None:
                try:
                    with open(full_path, 'w') as f:
                        f.write(content)
                    messagebox.showinfo("Success", f"Content written to '{selected_item}'.")
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred: {e}")

    def update_file(self):
        selected_item = self.file_listbox.get(tk.ACTIVE)
        full_path = os.path.join(self.current_path.get(), selected_item)
        
        if os.path.isfile(full_path):
            content = simpledialog.askstring("update to File", f"Enter new content for '{selected_item}':")
            if content is not None:
                try:
                    with open(full_path, 'w') as f:
                        f.write(content)
                    messagebox.showinfo("Success", f"Content written to '{selected_item}'.")
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred: {e}")

    def list_hidden_files(self):

        files = os.listdir('.')

        hidden_files = [f for f in files if f.startswith('.')]

        tk.messagebox.showinfo("Hidden Files", hidden_files)

 


    def show_file_content(self, file_name, content):
        dialog = tk.Toplevel(self.root)
        dialog.title(f"File Content: {file_name}")
        
        text_widget = tk.Text(dialog)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)





    def create_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                  filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                with open(file_path, 'w'):
                    self.load_current_directory()  # Refresh the list after file creation
                    messagebox.showinfo("Success", f"File '{os.path.basename(file_path)}' created.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")


    
    def delete_file(self):
        selected_item = self.file_listbox.get(tk.ACTIVE)
        full_path = os.path.join(self.current_path.get(), selected_item)
        
        if os.path.isfile(full_path):
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{selected_item}'?"):
                os.remove(full_path)
                self.load_current_directory()  # Refresh the list after file deletion
                messagebox.showinfo("Success", f"File '{selected_item}' deleted.")
    
    def set_permissions(self):
        selected_item = self.file_listbox.get(tk.ACTIVE)
        full_path = os.path.join(self.current_path.get(), selected_item)
        
        if os.path.isfile(full_path):
            permissions = simpledialog.askstring("Set Permissions", f"Enter permissions for '{selected_item}' (e.g. 777):")
            try:
                os.chmod(full_path, int(permissions, 8))  # Convert octal string to integer
                messagebox.showinfo("Success", f"Permissions for '{selected_item}' set to {permissions}.")
            except ValueError:
                messagebox.showinfo("Error", f"Invalid permissions: {permissions}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileManagerGUI(root)
    root.mainloop()
