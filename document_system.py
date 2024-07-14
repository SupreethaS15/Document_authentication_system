import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, simpledialog 
import hashlib
import os

# Simulated user database and document storage
users = {}
documents = {}
evidences = {}
current_user = None
evidence_packs = []
capacity = 3  # Maximum number of evidences per pack

class BPlusTree:
    # Implementation of B+ Tree for simplicity
    def __init__(self):
        self.keys = []

    def insert(self, key):
        self.keys.append(key)
        self.keys.sort()

    def delete(self, key):
        self.keys.remove(key)

    def get_all_keys(self):
        return self.keys

document_tree = BPlusTree()

class DocumentSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Legal Document System")
        self.root.geometry("800x600")
        self.root.configure(bg='black')

        self.pages = {}
        self.create_login_page()
        self.create_signup_page()
        self.create_main_page()

        self.show_page("login")

    def show_page(self, page_name):
        for page in self.pages.values():
            page.pack_forget()
        self.pages[page_name].pack(expand=True)

    def create_login_page(self):
        frame = tk.Frame(self.root, bg="black", padx=20, pady=20)
        self.pages["login"] = frame

        tk.Label(frame, text="User Login", font=("Arial", 24), fg="white", bg="black").pack(pady=10)
        tk.Label(frame, text="Username:", fg="white", bg="black").pack()
        self.login_username_entry = tk.Entry(frame)
        self.login_username_entry.pack()

        tk.Label(frame, text="Password:", fg="white", bg="black").pack()
        self.login_password_entry = tk.Entry(frame, show="*")
        self.login_password_entry.pack()

        tk.Button(frame, text="Login", command=self.login, bg="white", fg="black").pack(pady=10)
        tk.Button(frame, text="Signup", command=lambda: self.show_page("signup"), bg="white", fg="black").pack()

    def create_signup_page(self):
        frame = tk.Frame(self.root, bg="black", padx=20, pady=20)
        self.pages["signup"] = frame

        tk.Label(frame, text="User Signup", font=("Arial", 24), fg="white", bg="black").pack(pady=10)
        tk.Label(frame, text="Username:", fg="white", bg="black").pack()
        self.signup_username_entry = tk.Entry(frame)
        self.signup_username_entry.pack()

        tk.Label(frame, text="Password:", fg="white", bg="black").pack()
        self.signup_password_entry = tk.Entry(frame, show="*")
        self.signup_password_entry.pack()

        tk.Button(frame, text="Signup", command=self.signup, bg="white", fg="black").pack(pady=10)
        tk.Button(frame, text="Back to Login", command=lambda: self.show_page("login"), bg="white", fg="black").pack()

    def create_main_page(self):
        frame = tk.Frame(self.root, bg="black", padx=20, pady=20)
        self.pages["main"] = frame

        tk.Label(frame, text="Legal Document System", font=("Arial", 24), fg="white", bg="black").pack(pady=10)

        self.user_name_label = tk.Label(frame, text=f"User: {current_user}", fg="white", bg="black")
        self.user_name_label.pack()

        tk.Button(frame, text="Upload Document", command=self.upload_document, bg="white", fg="black").pack(pady=10)
        tk.Button(frame, text="Upload Evidence", command=self.upload_evidence_and_show_details, bg="white", fg="black").pack(pady=10)

        tk.Label(frame, text="Search:", fg="white", bg="black").pack()
        self.search_entry = tk.Entry(frame)
        self.search_entry.pack()

        tk.Button(frame, text="Search", command=self.search_documents, bg="white", fg="black").pack(pady=10)

        self.doc_listbox = tk.Listbox(frame, bg="black", fg="white")
        self.doc_listbox.pack()
        self.doc_listbox.bind('<<ListboxSelect>>', self.show_document_details)

        self.details_text = scrolledtext.ScrolledText(frame, height=10, width=50, bg="black", fg="white", insertbackground='white')
        self.details_text.pack()

        tk.Button(frame, text="View Document", command=self.view_document, bg="white", fg="black").pack(pady=10)
        tk.Button(frame, text="Download Document", command=self.download_document, bg="white", fg="black").pack(pady=10)
        tk.Button(frame, text="Delete Document", command=self.delete_document, bg="white", fg="black").pack(pady=10)
        tk.Button(frame, text="Back to Login", command=lambda: self.show_page("login"), bg="white", fg="black").pack(pady=10)


    def login(self):
        global current_user
        username = self.login_username_entry.get()
        password = self.login_password_entry.get()
        if users.get(username) == password:
            current_user = username
            self.user_name_label.config(text=f"User: {current_user}")
            messagebox.showinfo("Login Success", f"Welcome, {username}!")
            self.show_page("main")
            self.update_document_list()
        else:
            messagebox.showwarning("Login Failed", "Invalid username or password.")

    def signup(self):
        username = self.signup_username_entry.get()
        password = self.signup_password_entry.get()
        if username in users:
            messagebox.showwarning("Signup Failed", "Username already exists.")
        else:
            users[username] = password
            messagebox.showinfo("Signup Success", "User registered successfully.")
            self.show_page("login")

    def calculate_hash(self, file_path):
        hash_algo = hashlib.sha256()
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hash_algo.update(chunk)
        return hash_algo.hexdigest()

    def upload_document(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            file_name = os.path.basename(file_path)
            doc_hash = self.calculate_hash(file_path)

            if file_name in documents:
                messagebox.showwarning("Upload Status", "Document already exists.")
            else:
                documents[file_name] = {'path': file_path, 'hash': doc_hash, 'owner': current_user}
                document_tree.insert(file_name)
                messagebox.showinfo("Upload Status", "Document uploaded successfully.")
                self.update_document_list()

    def upload_evidence(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            file_name = os.path.basename(file_path)
            urgency = int(simpledialog.askstring("Input", "Enter the urgency level (1-10):"))

            if file_name in evidences:
                messagebox.showwarning("Upload Status", "Evidence already exists.")
            else:
                evidences[file_name] = {'path': file_path, 'urgency': urgency, 'owner': current_user}
                self.pack_evidences()
                messagebox.showinfo("Upload Status", "Evidence uploaded and packed successfully.")
                self.update_evidence_list()

    def pack_evidences(self):
        global evidence_packs
        evidence_packs = []
        total_capacity = capacity

        sorted_evidences = sorted(evidences.items(), key=lambda x: x[1]['urgency'], reverse=True)
        current_pack = []
        current_capacity = 0

        for evidence in sorted_evidences:
            if current_capacity < total_capacity:
                current_pack.append(evidence)
                current_capacity += 1
            else:
                evidence_packs.append(current_pack)
                current_pack = [evidence]
                current_capacity = 1

        if current_pack:
            evidence_packs.append(current_pack)

    def update_document_list(self):
        self.doc_listbox.delete(0, tk.END)
        for doc_name in document_tree.get_all_keys():
            self.doc_listbox.insert(tk.END, doc_name)

    def show_document_details(self, event):
        selected_doc = self.doc_listbox.get(self.doc_listbox.curselection())
        doc_info = documents[selected_doc]
        details = f"File Name: {selected_doc}\nPath: {doc_info['path']}\nHash: {doc_info['hash']}\nOwner: {doc_info['owner']}"
        self.details_text.delete(1.0, tk.END)
        self.details_text.insert(tk.END, details)

    def view_document(self):
        selected_doc = self.doc_listbox.get(self.doc_listbox.curselection())
        doc_info = documents[selected_doc]
        old_hash = doc_info['hash']
        os.startfile(doc_info['path'])

        messagebox.showinfo("Viewing Document", "Please close the document after viewing/editing.")

        # Check if the current user is the owner of the document
        if doc_info['owner'] != current_user:
            messagebox.showwarning("Permission Denied", "You don't have permission to save changes to this document.")
            return

        # Check for changes after viewing
        new_hash = self.calculate_hash(doc_info['path'])
        if old_hash != new_hash:
            documents[selected_doc]['hash'] = new_hash
            messagebox.showinfo("Document Modified", "Changes detected and saved.")

    def download_document(self):
        selected_doc = self.doc_listbox.get(self.doc_listbox.curselection())
        doc_info = documents[selected_doc]
        download_path = filedialog.asksaveasfilename(defaultextension=os.path.splitext(doc_info['path'])[1],
                                                     initialfile=selected_doc)
        if download_path:
            with open(doc_info['path'], 'rb') as src, open(download_path, 'wb') as dst:
                dst.write(src.read())
            messagebox.showinfo("Download Status", "Document downloaded successfully.")

    def delete_document(self):
        selected_doc = self.doc_listbox.get(self.doc_listbox.curselection())
        doc_info = documents[selected_doc]
        if doc_info['owner'] == current_user:
            document_tree.delete(selected_doc)
            del documents[selected_doc]
            self.update_document_list()
            messagebox.showinfo("Delete Status", "Document deleted successfully.")
        else:
            messagebox.showwarning("Delete Status", "You do not have permission to delete this document.")

    def search_documents(self):
        query = self.search_entry.get().lower()
        self.doc_listbox.delete(0, tk.END)
        for doc_name in document_tree.get_all_keys():
            if query in doc_name.lower():
                self.doc_listbox.insert(tk.END, doc_name)

    def upload_evidence_and_show_details(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            file_name = os.path.basename(file_path)
            urgency = int(simpledialog.askstring("Input", "Enter the urgency level (1-10):"))

            if file_name in evidences:
                messagebox.showwarning("Upload Status", "Evidence already exists.")
            else:
                evidences[file_name] = {'path': file_path, 'urgency': urgency, 'owner': current_user}
                self.pack_evidences()
                messagebox.showinfo("Upload Status", "Evidence uploaded and packed successfully.")

                # Generate evidence pack details
                pack_details = self.generate_pack_details()

                # Show evidence pack details in the details_text widget
                self.details_text.delete(1.0, tk.END)
                self.details_text.insert(tk.END, pack_details)

                self.update_evidence_list()

    def generate_pack_details(self):
        pack_details = ""
        for pack in evidence_packs:
            pack_details += f"Pack:\n"
            for evidence_name, evidence_info in pack:
                pack_details += f"\tName: {evidence_name}, Urgency: {evidence_info['urgency']}\n"
        return pack_details


if __name__ == "__main__":
    root = tk.Tk()
    app = DocumentSystemApp(root)
    root.mainloop()
