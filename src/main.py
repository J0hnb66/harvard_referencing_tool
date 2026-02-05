import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os

from formatter.book_formatter import BookFormatter
from formatter.journal_formatter import JournalFormatter
from formatter.website_formatter import WebsiteFormatter
from validators.input_validator import InputValidator


class HarvardGUI:
    def __init__(self, root: tk.Tk, style: ttk.Style):
        self.root = root
        self.style = style
        self.root.title("Harvard Referencing Tool")

        # Background and layout
        self.root.configure(bg="#F5F5F5")
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)

        self.source_types = {
            "Book": ["author", "year", "title", "publisher"],
            "Journal": ["author", "year", "title", "journal", "volume", "issue", "pages"],
            "Website": ["author", "year", "title", "url"]
        }

        self.formatters = {
            "Book": BookFormatter(),
            "Journal": JournalFormatter(),
            "Website": WebsiteFormatter()
        }

        self.entries = {}
        self.entry_vars = {}
        self.selected_source = None
        self.source_buttons = {}

        self.build_ui()
        self.center_window()

    def build_ui(self):

        # ------------------------------------------------
        # SAFE LOGO LOADING (TOP RIGHT)
        # ------------------------------------------------
        logo_path = os.path.join(os.path.dirname(__file__), "icons", "lrc_logo.png")

        if os.path.exists(logo_path):
            try:
                logo_image = Image.open(logo_path)
                logo_image = logo_image.resize((80, 80), Image.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(logo_image)

                logo_label = ttk.Label(self.root, image=self.logo_photo, background="#F5F5F5")
                logo_label.grid(row=0, column=1, sticky="e", padx=10, pady=10)

            except Exception as e:
                print("Logo failed to load:", e)
        else:
            print("Logo not found at:", logo_path)

        # ------------------------------------------------
        # HEADER (TOP LEFT)
        # ------------------------------------------------
        header = ttk.Label(self.root, text="Harvard Referencing Tool ✨", style="Header.TLabel")
        header.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))

        # ------------------------------------------------
        # SOURCE TYPE BUTTONS
        # ------------------------------------------------
        ttk.Label(self.root, text="Select Source Type:", style="SubHeader.TLabel").grid(
            row=1, column=0, sticky="w", padx=10, pady=(5, 5)
        )

        button_frame = ttk.Frame(self.root, style="Card.TFrame")
        button_frame.grid(row=2, column=0, columnspan=2, pady=5, padx=10, sticky="w")

        icon_map = {
            "Book": "📘",
            "Journal": "📰",
            "Website": "🌐"
        }

        for i, source in enumerate(self.source_types.keys()):
            btn = ttk.Button(
                button_frame,
                text=f"{icon_map[source]} {source}",
                style="Rounded.TButton",
                command=lambda s=source: self.select_source(s)
            )
            btn.grid(row=0, column=i, padx=5, pady=5)
            self.source_buttons[source] = btn

        # Separator
        ttk.Separator(self.root, orient="horizontal").grid(
            row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=10
        )

        # ------------------------------------------------
        # DYNAMIC FIELDS
        # ------------------------------------------------
        self.fields_frame = ttk.Frame(self.root, style="Card.TFrame")
        self.fields_frame.grid(row=4, column=0, columnspan=2, pady=5, padx=10, sticky="ew")

        # ------------------------------------------------
        # ACTION BUTTONS
        # ------------------------------------------------
        button_bar = ttk.Frame(self.root, style="Card.TFrame")
        button_bar.grid(row=5, column=0, columnspan=2, pady=10, padx=10, sticky="w")

        ttk.Button(button_bar, text="✨ Generate", style="Rounded.TButton",
                   command=self.generate_reference).grid(row=0, column=0, padx=5, pady=5)

        ttk.Button(button_bar, text="📋 Copy", style="Rounded.TButton",
                   command=self.copy_to_clipboard).grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(button_bar, text="🧹 Clear", style="Rounded.TButton",
                   command=self.clear_fields).grid(row=0, column=2, padx=5, pady=5)

        # ------------------------------------------------
        # PREVIEW PANEL
        # ------------------------------------------------
        ttk.Label(self.root, text="Reference Preview:", style="SubHeader.TLabel").grid(
            row=6, column=0, sticky="w", padx=10
        )

        self.output_box = tk.Text(self.root, height=5, width=70, relief="solid", borderwidth=1)
        self.output_box.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.root.rowconfigure(7, weight=1)

    def select_source(self, source: str):
        self.selected_source = source
        self.update_fields()
        self.highlight_selected_button()

    def highlight_selected_button(self):
        for name, btn in self.source_buttons.items():
            if name == self.selected_source:
                btn.configure(style="SelectedRounded.TButton")
            else:
                btn.configure(style="Rounded.TButton")

    def update_fields(self):
        for widget in self.fields_frame.winfo_children():
            widget.destroy()

        self.entries.clear()
        self.entry_vars.clear()

        if not self.selected_source:
            return

        fields = self.source_types[self.selected_source]

        for i, field in enumerate(fields):
            ttk.Label(self.fields_frame, text=f"{field.capitalize()}:", style="TLabel").grid(
                row=i, column=0, sticky="w", padx=10, pady=3
            )

            var = tk.StringVar()
            var.trace_add("write", lambda *_: self.generate_reference())

            entry = ttk.Entry(self.fields_frame, width=40, textvariable=var)
            entry.grid(row=i, column=1, padx=10, pady=3, sticky="ew")

            self.entries[field] = entry
            self.entry_vars[field] = var

        self.fields_frame.columnconfigure(1, weight=1)

    def generate_reference(self):
        if not self.selected_source:
            return

        data = {field: var.get().strip() for field, var in self.entry_vars.items()}

        if any(v == "" for v in data.values()):
            self.output_box.delete("1.0", tk.END)
            return

        formatter = self.formatters[self.selected_source]
        reference = formatter.format(data)

        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, reference)

    def copy_to_clipboard(self):
        text = self.output_box.get("1.0", tk.END).strip()
        if text:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            messagebox.showinfo("Copied", "Reference copied to clipboard.")

    def clear_fields(self):
        for var in self.entry_vars.values():
            var.set("")
        self.output_box.delete("1.0", tk.END)

    def center_window(self):
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (w // 2)
        y = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.root.geometry(f"{w}x{h}+{x}+{y}")


def main():
    root = tk.Tk()

    style = ttk.Style()
    style.theme_use("clam")

    root.configure(bg="#F5F5F5")

    # Rounded button base style
    style.configure(
        "Rounded.TButton",
        padding=10,
        font=("Segoe UI", 10),
        background="#1976D2",
        foreground="white",
        borderwidth=0,
        relief="flat"
    )

    style.map(
        "Rounded.TButton",
        background=[("active", "#1565C0")]
    )

    # Selected rounded button
    style.configure(
        "SelectedRounded.TButton",
        padding=10,
        font=("Segoe UI", 10, "bold"),
        background="#4CAF50",
        foreground="white",
        borderwidth=0,
        relief="flat"
    )

    style.map(
        "SelectedRounded.TButton",
        background=[("active", "#45A049")]
    )

    # Labels
    style.configure(
        "Header.TLabel",
        font=("Segoe UI", 14, "bold"),
        background="#F5F5F5",
        foreground="#333333"
    )

    style.configure(
        "SubHeader.TLabel",
        font=("Segoe UI", 11, "bold"),
        background="#F5F5F5",
        foreground="#333333"
    )

    style.configure(
        "TLabel",
        font=("Segoe UI", 10),
        background="#F5F5F5",
        foreground="#333333"
    )

    style.configure("Card.TFrame", background="#F5F5F5")

    app = HarvardGUI(root, style)
    root.mainloop()


if __name__ == "__main__":
    main()
