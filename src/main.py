import tkinter as tk
from tkinter import ttk, messagebox

from formatter.book_formatter import BookFormatter
from formatter.journal_formatter import JournalFormatter
from formatter.website_formatter import WebsiteFormatter
from validators.input_validator import InputValidator


class HarvardGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Harvard Referencing Tool")

        # Allow window to resize nicely
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=3)

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
        self.selected_source = None
        self.source_buttons = {}

        self.build_ui()

    def build_ui(self):
        # Source type label
        ttk.Label(self.root, text="Select Source Type:").grid(row=0, column=0, sticky="w", padx=10, pady=5)

        # Button frame
        button_frame = ttk.Frame(self.root)
        button_frame.grid(row=1, column=0, columnspan=2, pady=5)

        for i, source in enumerate(self.source_types.keys()):
            btn = ttk.Button(button_frame, text=source,
                             command=lambda s=source: self.select_source(s))
            btn.grid(row=0, column=i, padx=5)
            self.source_buttons[source] = btn

        # Dynamic fields frame
        self.fields_frame = ttk.Frame(self.root)
        self.fields_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

        # Buttons: Generate, Copy, Clear
        button_bar = ttk.Frame(self.root)
        button_bar.grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Button(button_bar, text="Generate Reference", command=self.generate_reference).grid(row=0, column=0, padx=5)
        ttk.Button(button_bar, text="Copy to Clipboard", command=self.copy_to_clipboard).grid(row=0, column=1, padx=5)
        ttk.Button(button_bar, text="Clear Fields", command=self.clear_fields).grid(row=0, column=2, padx=5)

        # Live preview panel
        ttk.Label(self.root, text="Reference Preview:").grid(row=4, column=0, sticky="w", padx=10)
        self.output_box = tk.Text(self.root, height=5, width=70)
        self.output_box.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Make preview expand with window
        self.root.rowconfigure(5, weight=1)

    def select_source(self, source):
        self.selected_source = source
        self.update_fields()
        self.highlight_selected_button()

    def highlight_selected_button(self):
        for name, btn in self.source_buttons.items():
            if name == self.selected_source:
                btn.configure(style="Selected.TButton")
            else:
                btn.configure(style="TButton")

    def update_fields(self):
        # Clear old fields
        for widget in self.fields_frame.winfo_children():
            widget.destroy()

        self.entries.clear()

        if not self.selected_source:
            return

        fields = self.source_types[self.selected_source]

        # Create new fields
        for i, field in enumerate(fields):
            ttk.Label(self.fields_frame, text=f"{field.capitalize()}:").grid(row=i, column=0, sticky="w", padx=10)
            entry = ttk.Entry(self.fields_frame, width=40)
            entry.grid(row=i, column=1, padx=10, pady=2, sticky="ew")
            self.entries[field] = entry

        self.fields_frame.columnconfigure(1, weight=1)

    def generate_reference(self):
        if not self.selected_source:
            messagebox.showerror("Error", "Please select a source type.")
            return

        # Collect data
        data = {field: entry.get().strip() for field, entry in self.entries.items()}

        # Validate
        missing = InputValidator.validate_required_fields(data, self.source_types[self.selected_source])
        if missing:
            messagebox.showerror("Missing Fields", f"Please fill in: {', '.join(missing)}")
            return

        # Format
        formatter = self.formatters[self.selected_source]
        reference = formatter.format(data)

        # Display
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, reference)

    def copy_to_clipboard(self):
        text = self.output_box.get("1.0", tk.END).strip()
        if text:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            messagebox.showinfo("Copied", "Reference copied to clipboard.")

    def clear_fields(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.output_box.delete("1.0", tk.END)


def main():
    root = tk.Tk()

    # Style for selected button
    style = ttk.Style()
    style.configure("Selected.TButton", background="#4CAF50", foreground="white")

    app = HarvardGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
