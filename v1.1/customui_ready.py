import tkinter as tk
from tkinter import ttk, scrolledtext, BooleanVar, font, messagebox
import random
import string
from datetime import datetime
import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import os
import subprocess
import threading
import math

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraper.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()

# Define color themes
THEMES = {
    "dark": {
        "bg": "#2e2e2e",
        "fg": "#ffffff",
        "frame_bg": "#3d3d3d",
        "button_bg": "#555555",
        "button_fg": "#ffffff",
        "entry_bg": "#4d4d4d",
        "entry_fg": "#ffffff",
        "label_fg": "#cccccc",
        "highlight": "#4d94ff",
        "success": "#4CAF50",
        "warning": "#FF9800",
        "error": "#f44336"
    },
    "light": {
        "bg": "#f0f0f0",
        "fg": "#000000",
        "frame_bg": "#ffffff",
        "button_bg": "#e0e0e0",
        "button_fg": "#000000",
        "entry_bg": "#ffffff",
        "entry_fg": "#000000",
        "label_fg": "#333333",
        "highlight": "#0066cc",
        "success": "#4CAF50",
        "warning": "#FF9800",
        "error": "#f44336"
    },
    "cyberpunk": {
        "bg": "#0d1117",
        "fg": "#c9d1d9",
        "frame_bg": "#161b22",
        "button_bg": "#21262d",
        "button_fg": "#f0f6fc",
        "entry_bg": "#0d1117",
        "entry_fg": "#c9d1d9",
        "label_fg": "#58a6ff",
        "highlight": "#1f6feb",
        "success": "#3fb950",
        "warning": "#d29922",
        "error": "#f85149"
    },
    "monokai": {
        "bg": "#272822",
        "fg": "#F8F8F2",
        "frame_bg": "#383830",
        "button_bg": "#49483E",
        "button_fg": "#F8F8F2",
        "entry_bg": "#3E3D32",
        "entry_fg": "#F8F8F2",
        "label_fg": "#A6E22E",
        "highlight": "#66D9EF",
        "success": "#A6E22E",
        "warning": "#FD971F",
        "error": "#F92672"
    },
    "dracula": {
        "bg": "#282a36",
        "fg": "#f8f8f2",
        "frame_bg": "#44475a",
        "button_bg": "#6272a4",
        "button_fg": "#f8f8f2",
        "entry_bg": "#44475a",
        "entry_fg": "#f8f8f2",
        "label_fg": "#50fa7b",
        "highlight": "#8be9fd",
        "success": "#50fa7b",
        "warning": "#ffb86c",
        "error": "#ff5555"
    },
    "nord": {
        "bg": "#2E3440",
        "fg": "#D8DEE9",
        "frame_bg": "#3B4252",
        "button_bg": "#4C566A",
        "button_fg": "#ECEFF4",
        "entry_bg": "#434C5E",
        "entry_fg": "#D8DEE9",
        "label_fg": "#88C0D0",
        "highlight": "#5E81AC",
        "success": "#A3BE8C",
        "warning": "#EBCB8B",
        "error": "#BF616A"
    },
    "gruvbox": {
        "bg": "#282828",
        "fg": "#ebdbb2",
        "frame_bg": "#3c3836",
        "button_bg": "#504945",
        "button_fg": "#fbf1c7",
        "entry_bg": "#3c3836",
        "entry_fg": "#ebdbb2",
        "label_fg": "#fabd2f",
        "highlight": "#83a598",
        "success": "#b8bb26",
        "warning": "#fe8019",
        "error": "#fb4934"
    },
    "tokyo_night": {
        "bg": "#1a1b26",
        "fg": "#c0caf5",
        "frame_bg": "#24283b",
        "button_bg": "#414868",
        "button_fg": "#c0caf5",
        "entry_bg": "#1f2335",
        "entry_fg": "#c0caf5",
        "label_fg": "#7aa2f7",
        "highlight": "#bb9af7",
        "success": "#9ece6a",
        "warning": "#e0af68",
        "error": "#f7768e"
    },
    "material": {
        "bg": "#212121",
        "fg": "#ffffff",
        "frame_bg": "#303030",
        "button_bg": "#424242",
        "button_fg": "#ffffff",
        "entry_bg": "#424242",
        "entry_fg": "#ffffff",
        "label_fg": "#81C784",
        "highlight": "#2196F3",
        "success": "#4CAF50",
        "warning": "#FF9800",
        "error": "#F44336"
    },
    "solarized_dark": {
        "bg": "#002b36",
        "fg": "#839496",
        "frame_bg": "#073642",
        "button_bg": "#586e75",
        "button_fg": "#93a1a1",
        "entry_bg": "#073642",
        "entry_fg": "#839496",
        "label_fg": "#b58900",
        "highlight": "#268bd2",
        "success": "#859900",
        "warning": "#cb4b16",
        "error": "#dc322f"
    },
    "solarized_light": {
        "bg": "#fdf6e3",
        "fg": "#657b83",
        "frame_bg": "#eee8d5",
        "button_bg": "#93a1a1",
        "button_fg": "#002b36",
        "entry_bg": "#eee8d5",
        "entry_fg": "#586e75",
        "label_fg": "#b58900",
        "highlight": "#268bd2",
        "success": "#859900",
        "warning": "#cb4b16",
        "error": "#dc322f"
    },
    "ocean": {
        "bg": "#1b2631",
        "fg": "#a7b7c7",
        "frame_bg": "#263947",
        "button_bg": "#34495e",
        "button_fg": "#ecf0f1",
        "entry_bg": "#2c3e50",
        "entry_fg": "#bdc3c7",
        "label_fg": "#3498db",
        "highlight": "#2980b9",
        "success": "#27ae60",
        "warning": "#f39c12",
        "error": "#e74c3c"
    },
    "vampire": {
        "bg": "#1e1e1e",
        "fg": "#f8f8f2",
        "frame_bg": "#2d2d2d",
        "button_bg": "#3c3c3c",
        "button_fg": "#f8f8f2",
        "entry_bg": "#1a1a1a",
        "entry_fg": "#f8f8f2",
        "label_fg": "#ff79c6",
        "highlight": "#bd93f9",
        "success": "#50fa7b",
        "warning": "#f1fa8c",
        "error": "#ff5555"
    },
    "cherry_blossom": {
        "bg": "#fdf2f8",
        "fg": "#831843",
        "frame_bg": "#fce7f3",
        "button_bg": "#f9a8d4",
        "button_fg": "#831843",
        "entry_bg": "#ffffff",
        "entry_fg": "#831843",
        "label_fg": "#be185d",
        "highlight": "#ec4899",
        "success": "#10b981",
        "warning": "#f59e0b",
        "error": "#ef4444"
    }
}

class GlassButton(tk.Button):
    """Custom glass-effect button with hover animations"""
    def __init__(self, parent, text="", command=None, color="#4d94ff", **kwargs):
        super().__init__(parent, text=text, command=command, **kwargs)
        self.default_color = color
        self.hover_color = self._lighten_color(color, 30)
        
        self.configure(
            bg=self.default_color,
            fg="white",
            font=("Segoe UI", 12, "bold"),
            relief="flat",
            bd=0,
            padx=25,
            pady=12,
            cursor="hand2"
        )
        
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
        
    def _lighten_color(self, color, percent):
        """Lighten a hex color by a percentage"""
        try:
            color = color.lstrip('#')
            rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
            rgb = tuple(min(255, int(c + (255-c)*percent/100)) for c in rgb)
            return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
        except:
            return color
            
    def _on_enter(self, e):
        self.configure(bg=self.hover_color)
        
    def _on_leave(self, e):
        self.configure(bg=self.default_color)
        
    def _on_click(self, e):
        self.configure(bg=self._lighten_color(self.default_color, -20))
        self.after(100, lambda: self.configure(bg=self.hover_color))

class ModernCard(tk.Frame):
    """Modern card component with shadow effect"""
    def __init__(self, parent, title="", theme=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.theme = theme or THEMES["cyberpunk"]
        
        self.configure(
            bg=self.theme["frame_bg"],
            relief="flat",
            bd=0
        )
        
        # Title bar
        if title:
            title_frame = tk.Frame(self, bg=self.theme["highlight"], height=40)
            title_frame.pack(fill="x")
            title_frame.pack_propagate(False)
            
            title_label = tk.Label(
                title_frame, 
                text=title,
                bg=self.theme["highlight"],
                fg="white",
                font=("Segoe UI", 12, "bold"),
                pady=10
            )
            title_label.pack()
            
        # Content area
        self.content_frame = tk.Frame(self, bg=self.theme["frame_bg"])
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)

class AnimatedProgressBar(tk.Canvas):
    """Custom animated progress bar with smooth animations"""
    def __init__(self, parent, width=400, height=25, theme=None, **kwargs):
        super().__init__(parent, width=width, height=height, **kwargs)
        self.theme = theme or THEMES["cyberpunk"]
        self.width = width
        self.height = height
        self.progress = 0
        self.max_value = 100
        
        self.configure(
            bg=self.theme["entry_bg"],
            highlightthickness=0,
            relief="flat"
        )
        
        self._draw_progress()
        
    def _draw_progress(self):
        self.delete("all")
        
        # Background
        self.create_rectangle(
            0, 0, self.width, self.height,
            fill=self.theme["entry_bg"],
            outline=""
        )
        
        # Progress fill
        if self.progress > 0:
            progress_width = (self.progress / self.max_value) * self.width
            self.create_rectangle(
                0, 0, progress_width, self.height,
                fill=self.theme["success"],
                outline=""
            )
                
        # Border
        self.create_rectangle(
            0, 0, self.width, self.height,
            fill="",
            outline=self.theme["highlight"],
            width=2
        )
        
    def set_progress(self, value):
        self.progress = max(0, min(value, self.max_value))
        self._draw_progress()
        
    def set_max(self, value):
        self.max_value = value
        self._draw_progress()

class ModernUI:
    def __init__(self, root):
        self.root = root
        self.current_theme = "cyberpunk"
        self.theme = THEMES[self.current_theme]
        self.is_scraping = False
        
        # Setup fonts
        self.setup_fonts()
        
        # Initialize UI
        self.setup_modern_ui()
        
    def setup_fonts(self):
        """Setup custom fonts for the application"""
        self.title_font = font.Font(family="Segoe UI", size=24, weight="bold")
        self.subtitle_font = font.Font(family="Segoe UI", size=14, weight="normal")
        self.body_font = font.Font(family="Segoe UI", size=11)
        
    def setup_modern_ui(self):
        """Create the modern UI"""
        self.root.title("✨ Adobe Stock Prompt Generator Pro")
        self.root.geometry("1200x750")  # Better size for layout
        self.root.configure(bg=self.theme["bg"])
        self.root.resizable(True, True)
        
        # Create scrollable main canvas
        self.main_canvas = tk.Canvas(self.root, bg=self.theme["bg"], highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.main_canvas.yview)
        self.scrollable_frame = tk.Frame(self.main_canvas, bg=self.theme["bg"])
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        )
        
        self.main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.main_canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack canvas and scrollbar
        self.main_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Main container (now inside scrollable frame)
        self.main_container = tk.Frame(self.scrollable_frame, bg=self.theme["bg"])
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Bind mouse wheel to canvas
        self._bind_mousewheel()
        
        # Header
        self.create_header()
        
        # Main content
        self.create_main_content()
        
        # Footer
        self.create_footer()
        
    def create_header(self):
        """Create header with theme selector"""
        header_frame = tk.Frame(self.main_container, bg=self.theme["bg"], height=100)
        header_frame.pack(fill="x", pady=(0, 15))
        header_frame.pack_propagate(False)
        
        # Top row with title and theme selector
        top_row = tk.Frame(header_frame, bg=self.theme["bg"])
        top_row.pack(fill="x", pady=(10, 5))
        
        # Title (left side)
        self.title_label = tk.Label(
            top_row,
            text="🚀 Adobe Stock Prompt Generator Pro",
            bg=self.theme["bg"],
            fg=self.theme["highlight"],
            font=font.Font(family="Segoe UI", size=18, weight="bold")
        )
        self.title_label.pack(side="left")
        
        # Theme selector (right side)
        theme_frame = tk.Frame(top_row, bg=self.theme["bg"])
        theme_frame.pack(side="right")
        
        tk.Label(
            theme_frame,
            text="🎨 Theme:",
            bg=self.theme["bg"],
            fg=self.theme["label_fg"],
            font=font.Font(family="Segoe UI", size=10, weight="bold")
        ).pack(side="left", padx=(0, 5))
        
        self.theme_var = tk.StringVar(value=self.current_theme)
        theme_list = list(THEMES.keys())
        
        self.theme_dropdown = ttk.Combobox(
            theme_frame,
            textvariable=self.theme_var,
            values=theme_list,
            state="readonly",
            font=("Segoe UI", 9),
            width=15
        )
        self.theme_dropdown.pack(side="left")
        self.theme_dropdown.bind("<<ComboboxSelected>>", self.change_theme)
        
        # Subtitle
        self.subtitle_label = tk.Label(
            header_frame,
            text="AI-Powered Content Scraping with Modern UI • Use mouse wheel to scroll",
            bg=self.theme["bg"],
            fg=self.theme["label_fg"],
            font=font.Font(family="Segoe UI", size=10)
        )
        self.subtitle_label.pack(pady=(0, 10))
        
    def create_main_content(self):
        """Create main content area with better column layout"""
        content_frame = tk.Frame(self.main_container, bg=self.theme["bg"])
        content_frame.pack(fill="both", expand=True)
        
        # Left column - Main controls (60% width)
        left_column = tk.Frame(content_frame, bg=self.theme["bg"])
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 15))
        
        # Right column - Preview and controls (40% width)
        right_column = tk.Frame(content_frame, bg=self.theme["bg"], width=350)
        right_column.pack(side="right", fill="y")
        right_column.pack_propagate(False)
        
        # Left column content
        self.create_url_card(left_column)
        self.create_format_card(left_column)
        self.create_control_card(left_column)
        
        # Right column content
        self.create_preview_section(right_column)
        self.create_stats_section(right_column)
        
    def create_url_card(self, parent):
        """Create URL configuration card"""
        url_card = ModernCard(parent, "🌐 URL Configuration", self.theme)
        url_card.pack(fill="x", pady=(0, 15))
        
        # URL input
        url_label = tk.Label(
            url_card.content_frame,
            text="Adobe Stock URL:",
            bg=self.theme["frame_bg"],
            fg=self.theme["label_fg"],
            font=self.body_font
        )
        url_label.pack(anchor="w", pady=(0, 5))
        
        self.url_entry = tk.Entry(
            url_card.content_frame,
            bg=self.theme["entry_bg"],
            fg=self.theme["entry_fg"],
            font=self.body_font,
            relief="flat",
            bd=0,
            insertbackground=self.theme["entry_fg"]
        )
        self.url_entry.pack(fill="x", ipady=8, pady=(0, 10))
        self.url_entry.insert(0, "https://stock.adobe.com/vn/search?creator_id=206854500&filters%5Bcontent_type%3Aphoto%5D=1")
        
        # Page range
        page_frame = tk.Frame(url_card.content_frame, bg=self.theme["frame_bg"])
        page_frame.pack(fill="x", pady=(0, 10))
        
        # Start page
        start_frame = tk.Frame(page_frame, bg=self.theme["frame_bg"])
        start_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        tk.Label(
            start_frame,
            text="Start Page:",
            bg=self.theme["frame_bg"],
            fg=self.theme["label_fg"],
            font=self.body_font
        ).pack(anchor="w")
        
        self.start_page_entry = tk.Entry(
            start_frame,
            bg=self.theme["entry_bg"],
            fg=self.theme["entry_fg"],
            font=self.body_font,
            relief="flat",
            bd=0,
            justify="center"
        )
        self.start_page_entry.pack(fill="x", ipady=5)
        self.start_page_entry.insert(0, "1")
        
        # End page
        end_frame = tk.Frame(page_frame, bg=self.theme["frame_bg"])
        end_frame.pack(side="left", fill="x", expand=True)
        
        tk.Label(
            end_frame,
            text="End Page:",
            bg=self.theme["frame_bg"],
            fg=self.theme["label_fg"],
            font=self.body_font
        ).pack(anchor="w")
        
        self.end_page_entry = tk.Entry(
            end_frame,
            bg=self.theme["entry_bg"],
            fg=self.theme["entry_fg"],
            font=self.body_font,
            relief="flat",
            bd=0,
            justify="center"
        )
        self.end_page_entry.pack(fill="x", ipady=5)
        self.end_page_entry.insert(0, "5")
        
    def create_format_card(self, parent):
        """Create format settings card"""
        format_card = ModernCard(parent, "⚙️ Format Settings", self.theme)
        format_card.pack(fill="x", pady=(0, 15))
        
        # Boolean variables
        self.include_prefix_var = BooleanVar(value=True)
        self.include_suffix_var = BooleanVar(value=True)
        self.include_date_var = BooleanVar(value=True)
        self.include_params_var = BooleanVar(value=True)
        self.include_ar_var = BooleanVar(value=True)
        self.lowercase_var = BooleanVar(value=False)
        
        # Checkboxes
        checkbox_frame = tk.Frame(format_card.content_frame, bg=self.theme["frame_bg"])
        checkbox_frame.pack(fill="x", pady=(0, 15))
        
        options = [
            ("📝 Include Prefix", self.include_prefix_var),
            ("📎 Include Suffix", self.include_suffix_var),
            ("📅 Include Date", self.include_date_var),
            ("⚡ Include Parameters", self.include_params_var),
            ("📐 Include Aspect Ratio", self.include_ar_var),
            ("🔤 Convert to Lowercase", self.lowercase_var)
        ]
        
        for i, (text, var) in enumerate(options):
            row = i // 2
            col = i % 2
            
            cb = tk.Checkbutton(
                checkbox_frame,
                text=text,
                variable=var,
                bg=self.theme["frame_bg"],
                fg=self.theme["label_fg"],
                selectcolor=self.theme["highlight"],
                font=self.body_font,
                relief="flat",
                command=self.update_preview
            )
            cb.grid(row=row, column=col, sticky="w", padx=(0, 20), pady=2)
        
        # Input fields
        inputs_frame = tk.Frame(format_card.content_frame, bg=self.theme["frame_bg"])
        inputs_frame.pack(fill="x")
        
        # Create prefix field with generate button
        self._create_prefix_field(inputs_frame)
        self._create_input_field(inputs_frame, "Suffix:", "custom_suffix_entry", "dumnaf")
        self._create_input_field(inputs_frame, "Aspect Ratio:", "aspect_ratio_entry", "16:9")
        self._create_input_field(inputs_frame, "Parameters:", "additional_params_entry", "--no dust --p 5y3izqx")
        self._create_input_field(inputs_frame, "Filename:", "filename_entry", "output")
        
    def _create_prefix_field(self, parent):
        """Create prefix field with generate button"""
        field_frame = tk.Frame(parent, bg=self.theme["frame_bg"])
        field_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(
            field_frame,
            text="Prefix:",
            bg=self.theme["frame_bg"],
            fg=self.theme["label_fg"],
            font=self.body_font
        ).pack(anchor="w")
        
        # Container for entry and button
        entry_frame = tk.Frame(field_frame, bg=self.theme["frame_bg"])
        entry_frame.pack(fill="x")
        
        # Prefix entry field
        self.prefix_entry = tk.Entry(
            entry_frame,
            bg=self.theme["entry_bg"],
            fg=self.theme["entry_fg"],
            font=self.body_font,
            relief="flat",
            bd=0,
            insertbackground=self.theme["entry_fg"]
        )
        self.prefix_entry.pack(side="left", fill="x", expand=True, ipady=5, padx=(0, 10))
        self.prefix_entry.insert(0, self.generate_random_prefix())
        
        # Generate Prefix button
        self.generate_prefix_button = GlassButton(
            entry_frame,
            text="🎲 Generate",
            command=self.generate_new_prefix,
            color=self.theme["warning"]
        )
        self.generate_prefix_button.configure(
            padx=15,
            pady=8,
            font=("Segoe UI", 10, "bold")
        )
        self.generate_prefix_button.pack(side="right")
        
    def _create_input_field(self, parent, label, attr_name, default_value):
        """Create input field"""
        field_frame = tk.Frame(parent, bg=self.theme["frame_bg"])
        field_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(
            field_frame,
            text=label,
            bg=self.theme["frame_bg"],
            fg=self.theme["label_fg"],
            font=self.body_font
        ).pack(anchor="w")
        
        entry = tk.Entry(
            field_frame,
            bg=self.theme["entry_bg"],
            fg=self.theme["entry_fg"],
            font=self.body_font,
            relief="flat",
            bd=0,
            insertbackground=self.theme["entry_fg"]
        )
        entry.pack(fill="x", ipady=5)
        entry.insert(0, default_value)
        
        setattr(self, attr_name, entry)
        
    def create_control_card(self, parent):
        """Create control panel card"""
        control_card = ModernCard(parent, "🎮 Control Panel", self.theme)
        control_card.pack(fill="x")
        
        # Progress bar
        progress_frame = tk.Frame(control_card.content_frame, bg=self.theme["frame_bg"])
        progress_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(
            progress_frame,
            text="Progress:",
            bg=self.theme["frame_bg"],
            fg=self.theme["label_fg"],
            font=self.body_font
        ).pack(anchor="w", pady=(0, 5))
        
        self.progress_bar = AnimatedProgressBar(
            progress_frame, 
            width=400, 
            height=25, 
            theme=self.theme
        )
        self.progress_bar.pack(fill="x")
        
        # Control buttons
        button_frame = tk.Frame(control_card.content_frame, bg=self.theme["frame_bg"])
        button_frame.pack(fill="x", pady=(10, 0))
        
        # Start button
        self.start_button = GlassButton(
            button_frame,
            text="🚀 START SCRAPING",
            command=self.start_scraping_threaded,
            color=self.theme["success"]
        )
        self.start_button.pack(side="left", padx=(0, 10))
        
        # Preview button
        preview_button = GlassButton(
            button_frame,
            text="👁️ Update Preview",
            command=self.update_preview,
            color=self.theme["highlight"]
        )
        preview_button.pack(side="left", padx=(0, 10))
        
        # Folder button
        folder_button = GlassButton(
            button_frame,
            text="📁 Open Folder",
            command=self.open_current_folder,
            color=self.theme["warning"]
        )
        folder_button.pack(side="left")
        
    def create_preview_section(self, parent):
        """Create preview section"""
        preview_card = ModernCard(parent, "👁️ Live Preview", self.theme)
        preview_card.pack(fill="both", expand=True, pady=(0, 15))
        
        self.preview_area = tk.Text(
            preview_card.content_frame,
            bg=self.theme["entry_bg"],
            fg=self.theme["entry_fg"],
            height=12,
            relief="flat",
            bd=0,
            font=self.body_font,
            wrap="word"
        )
        self.preview_area.pack(fill="both", expand=True)
        
    def create_stats_section(self, parent):
        """Create statistics section"""
        stats_card = ModernCard(parent, "📊 Statistics", self.theme)
        stats_card.pack(fill="x")
        
        # Add some placeholder stats
        stats_frame = tk.Frame(stats_card.content_frame, bg=self.theme["frame_bg"])
        stats_frame.pack(fill="x", pady=10)
        
        # Status info
        status_info = tk.Label(
            stats_frame,
            text="📋 Ready to scrape\n⏱️ 0 pages processed\n📄 0 prompts generated",
            bg=self.theme["frame_bg"],
            fg=self.theme["label_fg"],
            font=self.body_font,
            justify="left"
        )
        status_info.pack(anchor="w")
        
        # Hidden log area for compatibility
        self.log_area = tk.Text(
            parent,
            height=1,
            width=1,
            bg=self.theme["entry_bg"],
            fg=self.theme["entry_fg"],
            relief="flat",
            bd=0,
            font=self.body_font,
            wrap="word"
        )
    
    def create_footer(self):
        """Create footer"""
        footer_frame = tk.Frame(self.main_container, bg=self.theme["frame_bg"], height=50)
        footer_frame.pack(side="bottom", fill="x", pady=(20, 0))
        footer_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            footer_frame,
            text="✨ Ready to scrape - Window is scrollable!",
            bg=self.theme["frame_bg"],
            fg=self.theme["label_fg"],
            font=self.body_font,
            anchor="w"
        )
        self.status_label.pack(side="left", padx=10, pady=15)
        
        version_label = tk.Label(
            footer_frame,
            text="v2.0 Pro",
            bg=self.theme["frame_bg"],
            fg=self.theme["label_fg"],
            font=self.body_font
        )
        version_label.pack(side="right", padx=10, pady=15)
    
    def _bind_mousewheel(self):
        """Bind mouse wheel events for scrolling"""
        def _on_mousewheel(event):
            self.main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_to_mousewheel(event):
            self.main_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbind_from_mousewheel(event):
            self.main_canvas.unbind_all("<MouseWheel>")
        
        self.main_canvas.bind('<Enter>', _bind_to_mousewheel)
        self.main_canvas.bind('<Leave>', _unbind_from_mousewheel)
    
    def generate_random_prefix(self):
        prefix = ''.join(random.choice(string.digits) for _ in range(7))
        logger.info(f"Generated random prefix: {prefix}")
        return prefix
        
    def generate_new_prefix(self):
        """Generate new prefix and update the entry field"""
        new_prefix = self.generate_random_prefix()
        self.prefix_entry.delete(0, tk.END)
        self.prefix_entry.insert(0, new_prefix)
        self.update_preview()  # Update preview with new prefix
        self.status_label.config(text=f"🎲 New prefix generated: {new_prefix}")
        
    def update_preview(self):
        prefix = self.prefix_entry.get() or self.generate_random_prefix() if self.include_prefix_var.get() else ""
        custom_suffix = self.custom_suffix_entry.get() or "dumnaf" if self.include_suffix_var.get() else ""
        aspect_ratio = self.aspect_ratio_entry.get() if self.include_ar_var.get() else ""
        additional_params = self.additional_params_entry.get() or "--no dust --p 5y3izqx" if self.include_params_var.get() else ""
        
        current_date = datetime.now().strftime('%d%m%Y') if self.include_date_var.get() else ""
        
        sample_text = "A cheerful real estate agent exhibits a spacious, empty office with large windows. The setting radiates opportunity and potential, ideal for businesses ready to move forward."
        
        if self.lowercase_var.get():
            sample_text = sample_text.lower()
        
        preview_text = ""
        if self.include_prefix_var.get():
            preview_text += f"{prefix} 01 "
        
        preview_text += sample_text
        
        if self.include_date_var.get():
            preview_text += f" {current_date}"
        
        if self.include_suffix_var.get():
            preview_text += custom_suffix
        
        if self.include_params_var.get():
            preview_text += f" {additional_params}"
        
        if self.include_ar_var.get():
            preview_text += f" --ar {aspect_ratio}"
        
        self.preview_area.delete(1.0, tk.END)
        self.preview_area.insert(tk.END, preview_text)
        logger.info("Preview updated")
        
    def open_current_folder(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if os.name == 'nt':
            os.startfile(current_dir)
        else:
            subprocess.call(['open', current_dir])
    
    def change_theme(self, event=None):
        new_theme = self.theme_var.get()
        if new_theme in THEMES:
            self.current_theme = new_theme
            self.theme = THEMES[self.current_theme]
            self.apply_theme()
            self.status_label.config(
                text=f"🎨 Theme changed to {self.current_theme.title()}"
            )
    
    def apply_theme(self):
        """Apply theme to all elements"""
        self.root.configure(bg=self.theme["bg"])
        self.main_canvas.configure(bg=self.theme["bg"])
        self.scrollable_frame.configure(bg=self.theme["bg"])
        self.main_container.configure(bg=self.theme["bg"])
        
        # Update header elements
        try:
            self.title_label.configure(bg=self.theme["bg"], fg=self.theme["highlight"])
            self.subtitle_label.configure(bg=self.theme["bg"], fg=self.theme["label_fg"])
            self.status_label.configure(bg=self.theme["frame_bg"], fg=self.theme["label_fg"])
        except:
            pass
        
        # Update cards and components recursively
        self._update_widget_theme(self.main_container)
    
    def _update_widget_theme(self, widget):
        """Recursively update theme for all child widgets"""
        try:
            # Update frames
            if isinstance(widget, tk.Frame):
                if "card" in str(widget).lower() or "content" in str(widget).lower():
                    widget.configure(bg=self.theme["frame_bg"])
                else:
                    widget.configure(bg=self.theme["bg"])
            
            # Update labels
            elif isinstance(widget, tk.Label):
                current_bg = widget.cget("bg")
                if current_bg == self.theme.get("highlight", ""):
                    # Keep highlight backgrounds
                    pass
                elif "frame" in str(widget.master).lower():
                    widget.configure(bg=self.theme["frame_bg"], fg=self.theme["label_fg"])
                else:
                    widget.configure(bg=self.theme["bg"], fg=self.theme["label_fg"])
            
            # Update text widgets
            elif isinstance(widget, tk.Text):
                widget.configure(
                    bg=self.theme["entry_bg"],
                    fg=self.theme["entry_fg"],
                    insertbackground=self.theme["entry_fg"],
                    selectbackground=self.theme["highlight"]
                )
            
            # Update entry widgets
            elif isinstance(widget, tk.Entry):
                widget.configure(
                    bg=self.theme["entry_bg"],
                    fg=self.theme["entry_fg"],
                    insertbackground=self.theme["entry_fg"]
                )
                
            # Update checkbuttons
            elif isinstance(widget, tk.Checkbutton):
                widget.configure(
                    bg=self.theme["frame_bg"],
                    fg=self.theme["label_fg"],
                    selectcolor=self.theme["highlight"]
                )
            
            # Recursively update children
            for child in widget.winfo_children():
                self._update_widget_theme(child)
                
        except Exception as e:
            pass  # Ignore theme update errors
    
    def start_scraping_threaded(self):
        """Start scraping in thread"""
        if not self.is_scraping:
            self.is_scraping = True
            self.start_button.configure(text="🛑 Stop Scraping")
            threading.Thread(target=self.start_scraping, daemon=True).start()
        else:
            self.is_scraping = False
            self.start_button.configure(text="🚀 START SCRAPING")
    
    def start_scraping(self):
        """Main scraping function with improved error handling and validation"""
        driver = None
        try:
            # Input validation
            url = self.url_entry.get().strip()
            if not url:
                raise ValueError("Please enter a valid URL")
            
            try:
                start_page = int(self.start_page_entry.get())
                end_page = int(self.end_page_entry.get())
            except ValueError:
                raise ValueError("Please enter valid page numbers")
            
            if start_page < 1 or end_page < 1:
                raise ValueError("Page numbers must be positive")
            
            if start_page > end_page:
                raise ValueError("Start page cannot be greater than end page")
                
            base_filename = self.filename_entry.get().strip() or "output"
            
            self.status_label.config(text=f"🔍 Scraping pages {start_page} to {end_page}...")
            logger.info(f"Starting scraping from page {start_page} to {end_page}")
            
            # Set up Chrome options with better configuration
            options = Options()
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--disable-gpu')
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-web-security')
            options.add_argument('--allow-running-insecure-content')
            options.add_argument('--disable-extensions')
            options.add_argument('--window-size=1920,1080')
            options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            
            try:
                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
                driver.set_page_load_timeout(30)
            except Exception as e:
                raise RuntimeError(f"Failed to initialize Chrome driver: {str(e)}")
            
            all_titles = []
            total_pages = end_page - start_page + 1
            self.progress_bar.set_max(total_pages)
            successful_pages = 0
            failed_pages = 0
            
            for i, page in enumerate(range(start_page, end_page + 1)):
                if not self.is_scraping:
                    logger.info("Scraping stopped by user")
                    break
                    
                self.progress_bar.set_progress(i)
                page_url = f"{url}&search_page={page}"
                
                try:
                    self.status_label.config(text=f"🔍 Scraping page {page} of {end_page}...")
                    driver.get(page_url)
                    
                    # Wait for page to load with better error handling
                    time.sleep(3)
                    
                    # Check if page loaded successfully
                    if "error" in driver.current_url.lower() or "404" in driver.page_source:
                        logger.warning(f"Page {page} might have failed to load properly")
                        failed_pages += 1
                        continue
                    
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    titles = soup.find_all('meta', itemprop='name')
                    page_titles = [title.get('content', '').strip() for title in titles if title.get('content', '').strip()]
                    
                    if page_titles:
                        all_titles.extend(page_titles)
                        successful_pages += 1
                        logger.info(f"Page {page}: Found {len(page_titles)} titles")
                    else:
                        logger.warning(f"Page {page}: No titles found")
                        failed_pages += 1
                    
                    time.sleep(1)  # Be respectful to the server
                    
                except Exception as page_error:
                    logger.error(f"Error scraping page {page}: {str(page_error)}")
                    failed_pages += 1
                    continue
            
            # Process and save
            unique_titles = list(dict.fromkeys(all_titles))
            formatted_prompts = []
            
            prefix = self.prefix_entry.get() if self.include_prefix_var.get() else ""
            current_date = datetime.now().strftime('%d%m%Y') if self.include_date_var.get() else ""
            
            for count, title in enumerate(unique_titles, 1):
                if not self.is_scraping:
                    break
                    
                if title:
                    prompt = ""
                    if self.include_prefix_var.get():
                        prompt += f"{prefix} {count:02d} "
                    
                    formatted_title = title.lower() if self.lowercase_var.get() else title
                    prompt += formatted_title
                    
                    if self.include_date_var.get():
                        prompt += f" {current_date}"
                    
                    if self.include_suffix_var.get():
                        prompt += self.custom_suffix_entry.get()
                    
                    if self.include_params_var.get():
                        prompt += f" {self.additional_params_entry.get()}"
                    
                    if self.include_ar_var.get():
                        prompt += f" --ar {self.aspect_ratio_entry.get()}"
                    
                    formatted_prompts.append(prompt)
            
            # Save to file
            formatted_date = datetime.now().strftime('%d%m%Y%H%M%S')
            filename = f"{base_filename}{formatted_date}tic.txt"
            
            with open(filename, 'w', encoding='utf-8') as file:
                for prompt in formatted_prompts:
                    file.write(prompt + '\n')
            
            self.status_label.config(text=f"✅ Completed! Saved {len(formatted_prompts)} prompts to {filename}")
            self.progress_bar.set_progress(0)
            
            driver.quit()
            messagebox.showinfo("Success", f"Scraping completed!\nSaved {len(formatted_prompts)} prompts to {filename}")
            
        except Exception as e:
            self.status_label.config(text=f"⚠️ Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
        finally:
            self.is_scraping = False
            self.start_button.configure(text="🚀 START SCRAPING")

# Create and run the application
if __name__ == "__main__":
    print("Starting Adobe Stock Prompt Generator Pro...")
    
    root = tk.Tk()
    
    # Force window to appear
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(lambda: root.attributes('-topmost', False))
    
    app = ModernUI(root)
    
    print("UI initialized. Starting main loop...")
    root.mainloop()
    print("Application closed.")
