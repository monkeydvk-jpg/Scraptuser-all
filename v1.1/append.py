import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os

class FileUpdateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Update Tool")
        self.root.geometry("600x550")
        
        self.selected_file = None
        self.setup_ui()
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # File selection section
        file_frame = ttk.LabelFrame(main_frame, text="File Selection", padding="10")
        file_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.file_label = ttk.Label(file_frame, text="No file selected")
        self.file_label.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.browse_button = ttk.Button(file_frame, text="Browse File", command=self.browse_file)
        self.browse_button.grid(row=0, column=1)
        
        # Custom input section
        input_frame = ttk.LabelFrame(main_frame, text="Update Options", padding="10")
        input_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Line number selection (conditional display)
        self.line_label = ttk.Label(input_frame, text="Line Number:")
        self.line_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.line_var = tk.StringVar(value="1")
        self.line_entry = ttk.Entry(input_frame, textvariable=self.line_var, width=10)
        self.line_entry.grid(row=0, column=1, sticky=tk.W, pady=(0, 5))
        
        # Update mode selection
        ttk.Label(input_frame, text="Update Mode:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        self.mode_var = tk.StringVar(value="append")
        self.mode_var.trace('w', self.on_mode_change)  # Track mode changes
        
        mode_frame = ttk.Frame(input_frame)
        mode_frame.grid(row=1, column=1, sticky=tk.W, pady=(0, 5))
        
        ttk.Radiobutton(mode_frame, text="Append to specific line", variable=self.mode_var, value="append").pack(anchor=tk.W)
        ttk.Radiobutton(mode_frame, text="Replace specific line", variable=self.mode_var, value="replace").pack(anchor=tk.W)
        ttk.Radiobutton(mode_frame, text="Insert new line", variable=self.mode_var, value="insert").pack(anchor=tk.W)
        ttk.Radiobutton(mode_frame, text="Append to end of each line", variable=self.mode_var, value="append_all").pack(anchor=tk.W)
        
        # Text input
        ttk.Label(input_frame, text="Text to add:").grid(row=2, column=0, sticky=(tk.W, tk.N), pady=(10, 0))
        self.text_input = scrolledtext.ScrolledText(input_frame, width=40, height=5)
        self.text_input.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.preview_button = ttk.Button(button_frame, text="Preview Changes", command=self.preview_changes)
        self.preview_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.update_button = ttk.Button(button_frame, text="Update File", command=self.update_file)
        self.update_button.pack(side=tk.LEFT)
        
        # Preview area
        preview_frame = ttk.LabelFrame(main_frame, text="File Preview", padding="10")
        preview_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        self.preview_text = scrolledtext.ScrolledText(preview_frame, width=60, height=12)
        self.preview_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        file_frame.columnconfigure(0, weight=1)
        input_frame.columnconfigure(1, weight=1)
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(0, weight=1)
    
    def on_mode_change(self, *args):
        """Handle mode change to show/hide line number input"""
        mode = self.mode_var.get()
        if mode == "append_all":
            # Hide line number input for "append to all lines" mode
            self.line_label.grid_remove()
            self.line_entry.grid_remove()
        else:
            # Show line number input for other modes
            self.line_label.grid()
            self.line_entry.grid()
    
    def browse_file(self):
        """Open file dialog to select a file"""
        filetypes = (
            ('Text files', '*.txt'),
            ('Python files', '*.py'),
            ('All files', '*.*')
        )
        
        filename = filedialog.askopenfilename(
            title='Select file to update',
            initialdir=os.getcwd(),
            filetypes=filetypes
        )
        
        if filename:
            self.selected_file = filename
            self.file_label.config(text=f"Selected: {os.path.basename(filename)}")
            self.load_file_preview()
    
    def load_file_preview(self):
        """Load and display file contents in preview"""
        if not self.selected_file:
            return
        
        try:
            with open(self.selected_file, 'r', encoding='utf-8') as file:
                content = file.read()
            
            self.preview_text.delete('1.0', tk.END)
            
            # Add line numbers to preview
            lines = content.split('\n')
            numbered_content = '\n'.join(f"{i+1:3d}: {line}" for i, line in enumerate(lines))
            self.preview_text.insert('1.0', numbered_content)
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not read file: {str(e)}")
    
    def preview_changes(self):
        """Preview what the file will look like after changes"""
        if not self.selected_file:
            messagebox.showwarning("Warning", "Please select a file first")
            return
        
        try:
            text_to_add = self.text_input.get('1.0', tk.END).strip()
            mode = self.mode_var.get()
            
            if not text_to_add:
                messagebox.showwarning("Warning", "Please enter text to add")
                return
            
            with open(self.selected_file, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            # Create preview of changes
            preview_lines = lines.copy()
            
            if mode == "append_all":
                # Append to end of each line
                preview_lines = [line.rstrip('\n') + text_to_add + '\n' for line in lines]
                
            else:
                # Handle other modes (existing functionality)
                line_num = int(self.line_var.get())
                
                if mode == "append":
                    if 0 < line_num <= len(lines):
                        preview_lines[line_num - 1] = lines[line_num - 1].rstrip('\n') + text_to_add + '\n'
                elif mode == "replace":
                    if 0 < line_num <= len(lines):
                        preview_lines[line_num - 1] = text_to_add + '\n'
                elif mode == "insert":
                    if 0 < line_num <= len(lines) + 1:
                        preview_lines.insert(line_num - 1, text_to_add + '\n')
            
            # Display preview with line numbers
            self.preview_text.delete('1.0', tk.END)
            numbered_preview = '\n'.join(f"{i+1:3d}: {line.rstrip()}" for i, line in enumerate(preview_lines))
            self.preview_text.insert('1.0', numbered_preview)
            
            # Highlight changed lines
            if mode == "append_all":
                # Highlight all lines for append_all mode
                for i in range(1, len(preview_lines) + 1):
                    start_pos = f"{i}.0"
                    end_pos = f"{i}.end"
                    self.preview_text.tag_add("highlight", start_pos, end_pos)
            else:
                # Highlight specific line for other modes
                if mode in ["append", "replace"]:
                    highlight_line = int(self.line_var.get())
                else:  # insert
                    highlight_line = int(self.line_var.get())
                
                start_pos = f"{highlight_line}.0"
                end_pos = f"{highlight_line}.end"
                self.preview_text.tag_add("highlight", start_pos, end_pos)
            
            self.preview_text.tag_config("highlight", background="yellow")
            
        except ValueError:
            if mode != "append_all":
                messagebox.showerror("Error", "Please enter a valid line number")
        except Exception as e:
            messagebox.showerror("Error", f"Preview failed: {str(e)}")
    
    def update_file(self):
        """Update the selected file with the specified changes"""
        if not self.selected_file:
            messagebox.showwarning("Warning", "Please select a file first")
            return
        
        try:
            text_to_add = self.text_input.get('1.0', tk.END).strip()
            mode = self.mode_var.get()
            
            if not text_to_add:
                messagebox.showwarning("Warning", "Please enter text to add")
                return
            
            # Create backup
            backup_file = self.selected_file + '.backup'
            with open(self.selected_file, 'r', encoding='utf-8') as original:
                with open(backup_file, 'w', encoding='utf-8') as backup:
                    backup.write(original.read())
            
            # Read original file
            with open(self.selected_file, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            # Apply changes
            if mode == "append_all":
                # Append to end of each line
                lines = [line.rstrip('\n') + text_to_add + '\n' for line in lines]
                success_msg = f"Text appended to all {len(lines)} lines successfully!"
                
            else:
                # Handle other modes (existing functionality)
                line_num = int(self.line_var.get())
                
                if mode == "append":
                    if 0 < line_num <= len(lines):
                        lines[line_num - 1] = lines[line_num - 1].rstrip('\n') + text_to_add + '\n'
                    else:
                        raise ValueError(f"Line number {line_num} is out of range")
                elif mode == "replace":
                    if 0 < line_num <= len(lines):
                        lines[line_num - 1] = text_to_add + '\n'
                    else:
                        raise ValueError(f"Line number {line_num} is out of range")
                elif mode == "insert":
                    if 0 < line_num <= len(lines) + 1:
                        lines.insert(line_num - 1, text_to_add + '\n')
                    else:
                        raise ValueError(f"Line number {line_num} is out of range")
                
                success_msg = f"Line {line_num} updated successfully!"
            
            # Write updated content
            with open(self.selected_file, 'w', encoding='utf-8') as file:
                file.writelines(lines)
            
            messagebox.showinfo("Success", f"{success_msg}\nBackup saved as: {backup_file}")
            self.load_file_preview()
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Update failed: {str(e)}")

def main():
    root = tk.Tk()
    app = FileUpdateApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
