"""Cinema management GUI."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from app import db
from app.receipts import generate_receipt_xml


class CinemaApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Cinema Manager")
        self.geometry("1000x700")

        db.ensure_indexes()

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.users_tab = ttk.Frame(self.notebook)
        self.movies_tab = ttk.Frame(self.notebook)
        self.purchases_tab = ttk.Frame(self.notebook)
        self.reports_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.users_tab, text="Users")
        self.notebook.add(self.movies_tab, text="Movies")
        self.notebook.add(self.purchases_tab, text="Purchases")
        self.notebook.add(self.reports_tab, text="Reports")

        self._build_users_tab()
        self._build_movies_tab()
        self._build_purchases_tab()
        self._build_reports_tab()

        self.refresh_users()
        self.refresh_movies()
        self.refresh_purchases()

    # Users
    def _build_users_tab(self) -> None:
        form = ttk.LabelFrame(self.users_tab, text="User Details")
        form.pack(fill="x", padx=10, pady=10)

        self.user_id_var = tk.StringVar()
        self.user_name_var = tk.StringVar()
        self.user_email_var = tk.StringVar()
        self.user_pref_var = tk.StringVar()

        ttk.Label(form, text="Name").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.user_name_var, width=30).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form, text="Email").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.user_email_var, width=30).grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form, text="Preference").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.user_pref_var, width=30).grid(row=1, column=1, padx=5, pady=5)

        btns = ttk.Frame(form)
        btns.grid(row=1, column=2, columnspan=2, sticky="e", padx=5, pady=5)

        ttk.Button(btns, text="Add", command=self.add_user).pack(side="left", padx=5)
        ttk.Button(btns, text="Update", command=self.update_user).pack(side="left", padx=5)
        ttk.Button(btns, text="Delete", command=self.delete_user).pack(side="left", padx=5)
        ttk.Button(btns, text="Refresh", command=self.refresh_users).pack(side="left", padx=5)

        self.users_tree = ttk.Treeview(
            self.users_tab,
            columns=("id", "name", "email", "preference"),
            show="headings",
        )
        for col in ("id", "name", "email", "preference"):
            self.users_tree.heading(col, text=col.capitalize())
            self.users_tree.column(col, width=200)
        self.users_tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.users_tree.bind("<<TreeviewSelect>>", self.on_user_select)

    def refresh_users(self) -> None:
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        for user in db.list_users():
            self.users_tree.insert(
                "",
                "end",
                values=(str(user.get("_id")), user.get("name"), user.get("email"), user.get("preference")),
            )
        self.refresh_user_dropdown()

    def on_user_select(self, _event) -> None:
        selection = self.users_tree.selection()
        if not selection:
            return
        values = self.users_tree.item(selection[0], "values")
        self.user_id_var.set(values[0])
        self.user_name_var.set(values[1])
        self.user_email_var.set(values[2])
        self.user_pref_var.set(values[3])

    def add_user(self) -> None:
        try:
            db.create_user(self.user_name_var.get(), self.user_email_var.get(), self.user_pref_var.get())
            self.clear_user_form()
            self.refresh_users()
        except Exception as exc:
            messagebox.showerror("Error", f"Could not add user: {exc}")

    def update_user(self) -> None:
        if not self.user_id_var.get():
            messagebox.showinfo("Select", "Select a user to update.")
            return
        try:
            updated = db.update_user(
                self.user_id_var.get(),
                self.user_name_var.get(),
                self.user_email_var.get(),
                self.user_pref_var.get(),
            )
            if updated:
                self.clear_user_form()
                self.refresh_users()
        except Exception as exc:
            messagebox.showerror("Error", f"Could not update user: {exc}")

    def delete_user(self) -> None:
        if not self.user_id_var.get():
            messagebox.showinfo("Select", "Select a user to delete.")
            return
        if not messagebox.askyesno("Confirm", "Delete selected user?"):
            return
        try:
            db.delete_user(self.user_id_var.get())
            self.clear_user_form()
            self.refresh_users()
        except Exception as exc:
            messagebox.showerror("Error", f"Could not delete user: {exc}")

    def clear_user_form(self) -> None:
        self.user_id_var.set("")
        self.user_name_var.set("")
        self.user_email_var.set("")
        self.user_pref_var.set("")

    # Movies
    def _build_movies_tab(self) -> None:
        form = ttk.LabelFrame(self.movies_tab, text="Movie Details")
        form.pack(fill="x", padx=10, pady=10)

        self.movie_id_var = tk.StringVar()
        self.movie_name_var = tk.StringVar()
        self.movie_genre_var = tk.StringVar()
        self.movie_duration_var = tk.StringVar()
        self.movie_schedule_var = tk.StringVar()
        self.movie_tickets_var = tk.StringVar()
        self.movie_price_var = tk.StringVar()

        ttk.Label(form, text="Name").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.movie_name_var, width=25).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form, text="Genre").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.movie_genre_var, width=20).grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form, text="Duration (min)").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.movie_duration_var, width=25).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form, text="Schedule").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.movie_schedule_var, width=20).grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(form, text="Tickets").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.movie_tickets_var, width=25).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form, text="Price").grid(row=2, column=2, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.movie_price_var, width=20).grid(row=2, column=3, padx=5, pady=5)

        btns = ttk.Frame(form)
        btns.grid(row=3, column=0, columnspan=4, sticky="e", padx=5, pady=5)

        ttk.Button(btns, text="Add", command=self.add_movie).pack(side="left", padx=5)
        ttk.Button(btns, text="Update", command=self.update_movie).pack(side="left", padx=5)
        ttk.Button(btns, text="Delete", command=self.delete_movie).pack(side="left", padx=5)
        ttk.Button(btns, text="Refresh", command=self.refresh_movies).pack(side="left", padx=5)

        self.movies_tree = ttk.Treeview(
            self.movies_tab,
            columns=("id", "name", "genre", "duration", "schedule", "tickets", "price"),
            show="headings",
        )
        for col in ("id", "name", "genre", "duration", "schedule", "tickets", "price"):
            self.movies_tree.heading(col, text=col.capitalize())
            self.movies_tree.column(col, width=140)
        self.movies_tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.movies_tree.bind("<<TreeviewSelect>>", self.on_movie_select)

    def refresh_movies(self) -> None:
        for item in self.movies_tree.get_children():
            self.movies_tree.delete(item)
        for movie in db.list_movies():
            self.movies_tree.insert(
                "",
                "end",
                values=(
                    str(movie.get("_id")),
                    movie.get("name"),
                    movie.get("genre"),
                    movie.get("duration"),
                    movie.get("schedule"),
                    movie.get("available_tickets"),
                    f"{movie.get('price', 0):.2f}",
                ),
            )
        self.refresh_movie_dropdown()

    def on_movie_select(self, _event) -> None:
        selection = self.movies_tree.selection()
        if not selection:
            return
        values = self.movies_tree.item(selection[0], "values")
        self.movie_id_var.set(values[0])
        self.movie_name_var.set(values[1])
        self.movie_genre_var.set(values[2])
        self.movie_duration_var.set(values[3])
        self.movie_schedule_var.set(values[4])
        self.movie_tickets_var.set(values[5])
        self.movie_price_var.set(values[6])

    def add_movie(self) -> None:
        try:
            db.create_movie(
                self.movie_name_var.get(),
                self.movie_genre_var.get(),
                self.movie_duration_var.get(),
                self.movie_schedule_var.get(),
                int(self.movie_tickets_var.get()),
                float(self.movie_price_var.get()),
            )
            self.clear_movie_form()
            self.refresh_movies()
        except Exception as exc:
            messagebox.showerror("Error", f"Could not add movie: {exc}")

    def update_movie(self) -> None:
        if not self.movie_id_var.get():
            messagebox.showinfo("Select", "Select a movie to update.")
            return
        try:
            db.update_movie(
                self.movie_id_var.get(),
                self.movie_name_var.get(),
                self.movie_genre_var.get(),
                self.movie_duration_var.get(),
                self.movie_schedule_var.get(),
                int(self.movie_tickets_var.get()),
                float(self.movie_price_var.get()),
            )
            self.clear_movie_form()
            self.refresh_movies()
        except Exception as exc:
            messagebox.showerror("Error", f"Could not update movie: {exc}")

    def delete_movie(self) -> None:
        if not self.movie_id_var.get():
            messagebox.showinfo("Select", "Select a movie to delete.")
            return
        if not messagebox.askyesno("Confirm", "Delete selected movie?"):
            return
        try:
            db.delete_movie(self.movie_id_var.get())
            self.clear_movie_form()
            self.refresh_movies()
        except Exception as exc:
            messagebox.showerror("Error", f"Could not delete movie: {exc}")

    def clear_movie_form(self) -> None:
        self.movie_id_var.set("")
        self.movie_name_var.set("")
        self.movie_genre_var.set("")
        self.movie_duration_var.set("")
        self.movie_schedule_var.set("")
        self.movie_tickets_var.set("")
        self.movie_price_var.set("")

    # Purchases
    def _build_purchases_tab(self) -> None:
        form = ttk.LabelFrame(self.purchases_tab, text="Purchase")
        form.pack(fill="x", padx=10, pady=10)

        self.purchase_user_var = tk.StringVar()
        self.purchase_movie_var = tk.StringVar()
        self.purchase_quantity_var = tk.StringVar(value="1")

        ttk.Label(form, text="User").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.user_combo = ttk.Combobox(form, textvariable=self.purchase_user_var, width=40, state="readonly")
        self.user_combo.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form, text="Movie").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.movie_combo = ttk.Combobox(form, textvariable=self.purchase_movie_var, width=40, state="readonly")
        self.movie_combo.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form, text="Quantity").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.purchase_quantity_var, width=10).grid(row=1, column=1, padx=5, pady=5)

        self.total_label = ttk.Label(form, text="Total: 0.00")
        self.total_label.grid(row=1, column=2, sticky="w", padx=5, pady=5)

        btns = ttk.Frame(form)
        btns.grid(row=1, column=3, sticky="e", padx=5, pady=5)
        ttk.Button(btns, text="Check", command=self.check_total).pack(side="left", padx=5)
        ttk.Button(btns, text="Purchase", command=self.make_purchase).pack(side="left", padx=5)

        self.purchases_tree = ttk.Treeview(
            self.purchases_tab,
            columns=("id", "user", "movie", "qty", "total", "date"),
            show="headings",
        )
        for col in ("id", "user", "movie", "qty", "total", "date"):
            self.purchases_tree.heading(col, text=col.capitalize())
            self.purchases_tree.column(col, width=150)
        self.purchases_tree.pack(fill="both", expand=True, padx=10, pady=10)

    def refresh_purchases(self) -> None:
        for item in self.purchases_tree.get_children():
            self.purchases_tree.delete(item)
        for purchase in db.list_purchases():
            self.purchases_tree.insert(
                "",
                "end",
                values=(
                    str(purchase.get("_id")),
                    purchase.get("user_name"),
                    purchase.get("movie_name"),
                    purchase.get("quantity"),
                    f"{purchase.get('total', 0):.2f}",
                    purchase.get("purchased_at").strftime("%Y-%m-%d %H:%M"),
                ),
            )

    def refresh_user_dropdown(self) -> None:
        users = db.list_users()
        self.user_map = {f"{u.get('name')} ({u.get('email')})": str(u.get("_id")) for u in users}
        self.user_combo["values"] = list(self.user_map.keys())

    def refresh_movie_dropdown(self) -> None:
        movies = db.list_movies()
        self.movie_map = {f"{m.get('name')} ({m.get('schedule')})": str(m.get("_id")) for m in movies}
        self.movie_combo["values"] = list(self.movie_map.keys())

    def check_total(self) -> None:
        movie_label = self.purchase_movie_var.get()
        if movie_label not in self.movie_map:
            messagebox.showinfo("Select", "Select a movie.")
            return
        movie_id = self.movie_map[movie_label]
        movie = next((m for m in db.list_movies() if str(m.get("_id")) == movie_id), None)
        if movie is None:
            return
        try:
            qty = int(self.purchase_quantity_var.get())
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a number.")
            return
        total = float(movie.get("price", 0)) * qty
        self.total_label.configure(text=f"Total: {total:.2f}")

    def make_purchase(self) -> None:
        user_label = self.purchase_user_var.get()
        movie_label = self.purchase_movie_var.get()
        if user_label not in self.user_map or movie_label not in self.movie_map:
            messagebox.showinfo("Select", "Select a user and a movie.")
            return
        try:
            qty = int(self.purchase_quantity_var.get())
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a number.")
            return

        purchase = db.create_purchase(self.user_map[user_label], self.movie_map[movie_label], qty)
        if purchase is None:
            messagebox.showerror("Error", "Not enough tickets or missing data.")
            return

        receipt_path = generate_receipt_xml(purchase)
        messagebox.showinfo("Success", f"Purchase complete. Receipt: {receipt_path}")
        self.refresh_movies()
        self.refresh_purchases()

    # Reports
    def _build_reports_tab(self) -> None:
        controls = ttk.Frame(self.reports_tab)
        controls.pack(fill="x", padx=10, pady=10)

        ttk.Button(controls, text="All Purchases", command=self.report_all_purchases).pack(side="left", padx=5)
        ttk.Button(controls, text="User History", command=self.report_user_history).pack(side="left", padx=5)
        ttk.Button(controls, text="Available Movies", command=self.report_available_movies).pack(side="left", padx=5)

        self.report_text = tk.Text(self.reports_tab, height=20)
        self.report_text.pack(fill="both", expand=True, padx=10, pady=10)

    def report_all_purchases(self) -> None:
        self.report_text.delete("1.0", tk.END)
        for purchase in db.list_purchases():
            line = f"{purchase.get('purchased_at').strftime('%Y-%m-%d %H:%M')} | {purchase.get('user_name')} | "
            line += f"{purchase.get('movie_name')} | {purchase.get('quantity')} | {purchase.get('total'):.2f}"
            self.report_text.insert(tk.END, line + "\n")

    def report_user_history(self) -> None:
        user_label = self.purchase_user_var.get()
        if user_label not in self.user_map:
            messagebox.showinfo("Select", "Select a user in Purchases tab.")
            return
        self.report_text.delete("1.0", tk.END)
        user_id = self.user_map[user_label]
        for purchase in db.get_user_purchases(user_id):
            line = f"{purchase.get('purchased_at').strftime('%Y-%m-%d %H:%M')} | {purchase.get('movie_name')} | "
            line += f"{purchase.get('quantity')} | {purchase.get('total'):.2f}"
            self.report_text.insert(tk.END, line + "\n")

    def report_available_movies(self) -> None:
        self.report_text.delete("1.0", tk.END)
        for movie in db.list_movies():
            line = f"{movie.get('name')} | {movie.get('schedule')} | {movie.get('available_tickets')} tickets"
            self.report_text.insert(tk.END, line + "\n")


if __name__ == "__main__":
    app = CinemaApp()
    app.mainloop()
