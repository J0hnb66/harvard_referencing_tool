import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os

# macOS native clipboard (required for formatted paste into Word)
from AppKit import NSPasteboard, NSPasteboardTypeRTF
from Foundation import NSData

from formatter.book_formatter import BookFormatter
from formatter.journal_formatter import JournalFormatter
from formatter.website_formatter import WebsiteFormatter


class HarvardGUI:
    def __init__(self, root: tk.Tk, style: ttk.Style):
        self.root = root
        self.style = style
        self.root.title("Harvard Referencing Tool")

        self.root.configure(bg="#F5F5F5")
        self.root.update_idletasks()
        self.root.minsize(900, 650)

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(4, weight=1)
        self.root.rowconfigure(7, weight=1)

        self.source_types = {
            "Book": ["authors", "year", "title", "edition", "place", "publisher"],
            "Journal": ["authors", "year", "title", "journal", "volume", "issue", "pages"],
            "Website": ["authors", "organisation", "year", "title", "website_name", "url", "accessed"]
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

        header = ttk.Label(self.root, text="Harvard Referencing Tool ✨", style="Header.TLabel")
        header.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))

        ttk.Label(self.root, text="Select Source Type:", style="SubHeader.TLabel").grid(
            row=1, column=0, sticky="w", padx=10, pady=(5, 5)
        )

        button_frame = ttk.Frame(self.root, style="Card.TFrame")
        button_frame.grid(row=2, column=0, columnspan=2, pady=5, padx=10, sticky="w")

        icon_map = {"Book": "📘", "Journal": "📰", "Website": "🌐"}

        for i, source in enumerate(self.source_types.keys()):
            btn = ttk.Button(
                button_frame,
                text=f"{icon_map[source]} {source}",
                style="Rounded.TButton",
                command=lambda s=source: self.select_source(s)
            )
            btn.grid(row=0, column=i, padx=5, pady=5)
            self.source_buttons[source] = btn

        ttk.Separator(self.root, orient="horizontal").grid(
            row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=10
        )

        self.fields_frame = ttk.Frame(self.root, style="Card.TFrame")
        self.fields_frame.grid(row=4, column=0, columnspan=2, pady=5, padx=10, sticky="nsew")
        self.fields_frame.columnconfigure(1, weight=1)

        button_bar = ttk.Frame(self.root, style="Card.TFrame")
        button_bar.grid(row=5, column=0, columnspan=2, pady=10, padx=10, sticky="w")

        ttk.Button(button_bar, text="✨ Generate", style="Rounded.TButton",
                   command=self.generate_reference).grid(row=0, column=0, padx=5, pady=5)

        ttk.Button(button_bar, text="📋 Copy (Formatted)", style="Rounded.TButton",
                   command=self.copy_formatted).grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(button_bar, text="🧹 Clear", style="Rounded.TButton",
                   command=self.clear_fields).grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(self.root, text="Reference Preview:", style="SubHeader.TLabel").grid(
            row=6, column=0, sticky="w", padx=10
        )

        self.output_box = tk.Text(self.root, height=6, width=70, relief="solid", borderwidth=1,
                                  font=("Calibri", 11))
        self.output_box.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        italic_font = ("Calibri", 11, "italic")
        self.output_box.tag_configure("italic", font=italic_font)

    def select_source(self, source: str):
        self.selected_source = source
        self.update_fields()
        self.highlight_selected_button()

    def highlight_selected_button(self):
        for name, btn in self.source_buttons.items():
            btn.configure(style="SelectedRounded.TButton" if name == self.selected_source else "Rounded.TButton")

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

    def generate_reference(self):
        if not self.selected_source:
            return

        data = {field: var.get().strip() for field, var in self.entry_vars.items()}

        if "authors" in data:
            data["authors"] = [a.strip() for a in data["authors"].split(",") if a.strip()]

        if any(v == "" for v in data.values()):
            self.output_box.delete("1.0", tk.END)
            return

        formatter = self.formatters[self.selected_source]
        reference = formatter.format(data)

        self.output_box.delete("1.0", tk.END)

        if self.selected_source == "Book":
            title = data["title"]
            before, after = reference.split(title, 1)
            self.output_box.insert("end", before)
            self.output_box.insert("end", title, "italic")
            self.output_box.insert("end", after)

        elif self.selected_source == "Journal":
            journal = data["journal"]
            before, after = reference.split(journal, 1)
            self.output_box.insert("end", before)
            self.output_box.insert("end", journal, "italic")
            self.output_box.insert("end", after)

        else:
            self.output_box.insert("end", reference)

    def copy_formatted(self):
        text_widget = self.output_box

        # RTF header with Calibri font
        rtf = (
            "{\\rtf1\\ansi\n"
            "{\\fonttbl{\\f0 Calibri;}}\n"
            "\\f0\\fs22 "
        )

        index = "1.0"
        in_italic = False

        while True:
            char = text_widget.get(index)
            if char == "":
                break

            tags = text_widget.tag_names(index)
            is_italic = "italic" in tags

            if is_italic and not in_italic:
                rtf += "{\\i "
                in_italic = True

            if not is_italic and in_italic:
                rtf += "}"
                in_italic = False

            if char in ["\\", "{", "}"]:
                char = "\\" + char

            rtf += char
            index = text_widget.index(f"{index}+1c")

        if in_italic:
            rtf += "}"

        rtf += "}"

        pb = NSPasteboard.generalPasteboard()
        pb.clearContents()

        data = NSData.dataWithBytes_length_(rtf.encode("utf-8"), len(rtf.encode("utf-8")))
        pb.setData_forType_(data, NSPasteboardTypeRTF)

        messagebox.showinfo("Copied", "Formatted reference copied to clipboard.")

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

    style.configure("Rounded.TButton", padding=10, font=("Calibri", 11),
                    background="#1976D2", foreground="white", borderwidth=0, relief="flat")
    style.map("Rounded.TButton", background=[("active", "#1565C0")])

    style.configure("SelectedRounded.TButton", padding=10, font=("Calibri", 11, "bold"),
                    background="#4CAF50", foreground="white", borderwidth=0, relief="flat")
    style.map("SelectedRounded.TButton", background=[("active", "#45A049")])

    style.configure("Header.TLabel", font=("Calibri", 16, "bold"),
                    background="#F5F5F5", foreground="#333333")

    style.configure("SubHeader.TLabel", font=("Calibri", 13, "bold"),
                    background="#F5F5F5", foreground="#333333")

    style.configure("TLabel", font=("Calibri", 11),
                    background="#F5F5F5", foreground="#333333")

    style.configure("Card.TFrame", background="#F5F5F5")

    app = HarvardGUI(root, style)
    root.mainloop()


if __name__ == "__main__":
    main()
