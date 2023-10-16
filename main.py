import tkinter as tk
from tkinter import messagebox, simpledialog
import smtplib
from email.mime.text import MIMEText

class Candidate:
    def __init__(self, name):
        self.name = name

class AddCandidateWindow(tk.Toplevel):
    def __init__(self, app):
        super().__init__(app.root)
        self.app = app
        self.title("Добавить кандидата")

        self.label = tk.Label(self, text="Имя кандидата:")
        self.label.pack(pady=10)

        self.entry = tk.Entry(self)
        self.entry.pack(pady=10)

        self.add_button = tk.Button(self, text="Добавить", command=self.add_candidate)
        self.add_button.pack(pady=10)

    def add_candidate(self):
        candidate_name = self.entry.get().strip()
        if candidate_name:
            new_candidate = Candidate(candidate_name)
            self.app.add_candidate(new_candidate)
            self.destroy()
        else:
            messagebox.showwarning("Внимание", "Введите имя кандидата")

class SendInvitationWindow(tk.Toplevel):
    def __init__(self, app):
        super().__init__(app.root)
        self.app = app
        self.title("Отправить приглашение")

        self.label = tk.Label(self, text="Выберите кандидата:")
        self.label.pack(pady=10)

        self.candidates_var = tk.StringVar(self)
        self.candidates_var.set(app.get_candidate_names()[0] if app.get_candidate_names() else "")
        self.candidates_menu = tk.OptionMenu(self, self.candidates_var, *app.get_candidate_names())
        self.candidates_menu.pack(pady=10)

        self.email_label = tk.Label(self, text="Введите email:")
        self.email_label.pack(pady=10)

        self.email_entry = tk.Entry(self)
        self.email_entry.pack(pady=10)

        self.send_button = tk.Button(self, text="Отправить", command=self.send_invitation)
        self.send_button.pack(pady=10)

    def send_invitation(self):
        selected_candidate_name = self.candidates_var.get()
        email = self.email_entry.get().strip()

        if not selected_candidate_name or not email:
            messagebox.showwarning("Внимание", "Выберите кандидата и введите email")
            return

        selected_candidate = self.app.get_candidate_by_name(selected_candidate_name)
        subject = "Приглашение на собеседование"
        body = f"Уважаемый {selected_candidate.name}, приглашаем вас на собеседование. Мы ждем вас!"

        try:
            self.app.send_email(email, subject, body)
            messagebox.showinfo("Успех", "Приглашение успешно отправлено")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при отправке письма: {e}")

class CandidateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Список кандидатов")

        self.candidates = []

        # Элементы интерфейса
        self.label = tk.Label(root, text="Список кандидатов:")
        self.label.pack(pady=10)

        self.listbox = tk.Listbox(root)
        self.listbox.pack(pady=10)

        self.add_button = tk.Button(root, text="Добавить кандидата", command=self.open_add_candidate_window)
        self.add_button.pack(pady=10)

        self.remove_button = tk.Button(root, text="Удалить выбранного кандидата", command=self.remove_candidate)
        self.remove_button.pack(pady=10)

        self.email_button = tk.Button(root, text="Отправить приглашение", command=self.open_send_invitation_window)
        self.email_button.pack(pady=10)

    def add_candidate(self, candidate):
        self.candidates.append(candidate)
        self.listbox.insert(tk.END, candidate.name)

    def remove_candidate(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            index = selected_index[0]
            removed_candidate = self.candidates.pop(index)
            self.listbox.delete(index)
            messagebox.showinfo("Успех", f"Кандидат {removed_candidate.name} удален")
        else:
            messagebox.showwarning("Внимание", "Выберите кандидата для удаления")

    def open_add_candidate_window(self):
        add_candidate_window = AddCandidateWindow(self)

    def open_send_invitation_window(self):
        if not self.candidates:
            messagebox.showwarning("Внимание", "Список кандидатов пуст. Добавьте кандидата.")
            return

        send_invitation_window = SendInvitationWindow(self)

    def get_candidate_names(self):
        return [candidate.name for candidate in self.candidates]

    def get_candidate_by_name(self, name):
        for candidate in self.candidates:
            if candidate.name == name:
                return candidate

    def send_email(self, to_email, subject, body):
        # Здесь введите параметры для вашего SMTP-сервера
        smtp_server = 'smtp.example.com'
        smtp_port = 587
        smtp_username = 'your_username'
        smtp_password = 'your_password'

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = smtp_username
        msg['To'] = to_email

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(smtp_username, to_email, msg.as_string())

if __name__ == "__main__":
    root = tk.Tk()
    app = CandidateApp(root)
    root.mainloop()
