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
from PIL import Image, ImageTk, ImageDraw, ImageFilter
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
    "sunset": {
        "bg": "#2d1b2e",
        "fg": "#f4e4c1",
        "frame_bg": "#3e2d40",
        "button_bg": "#5c4356",
        "button_fg": "#f9f1e4",
        "entry_bg": "#4a3548",
        "entry_fg": "#f4e4c1",
        "label_fg": "#e67e80",
        "highlight": "#d699b6",
        "success": "#a7c080",
        "warning": "#dbbc7f",
        "error": "#e67e80"
    },
    "forest": {
        "bg": "#1e2d2f",
        "fg": "#c7d1cc",
        "frame_bg": "#2a3d3f",
        "button_bg": "#3e5c5e",
        "button_fg": "#e8f2ed",
        "entry_bg": "#2e4244",
        "entry_fg": "#c7d1cc",
        "label_fg": "#7fb069",
        "highlight": "#52a085",
        "success": "#7fb069",
        "warning": "#d4a574",
        "error": "#cc7a88"
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
    "neon_synthwave": {
        "bg": "#0d0221",
        "fg": "#f8f8f2",
        "frame_bg": "#1a0b3d",
        "button_bg": "#2d1b69",
        "button_fg": "#ffffff",
        "entry_bg": "#0f0a1f",
        "entry_fg": "#f8f8f2",
        "label_fg": "#ff006e",
        "highlight": "#8338ec",
        "success": "#06ffa5",
        "warning": "#ffbe0b",
        "error": "#fb5607"
    },
    "amoled_black": {
        "bg": "#000000",
        "fg": "#ffffff",
        "frame_bg": "#111111",
        "button_bg": "#1f1f1f",
        "button_fg": "#ffffff",
        "entry_bg": "#0a0a0a",
        "entry_fg": "#ffffff",
        "label_fg": "#cccccc",
        "highlight": "#007acc",
        "success": "#00ff41",
        "warning": "#ffa500",
        "error": "#ff1744"
    },
    "rose_pine": {
        "bg": "#191724",
        "fg": "#e0def4",
        "frame_bg": "#1f1d2e",
        "button_bg": "#26233a",
        "button_fg": "#e0def4",
        "entry_bg": "#191724",
        "entry_fg": "#e0def4",
        "label_fg": "#908caa",
        "highlight": "#c4a7e7",
        "success": "#31748f",
        "warning": "#f6c177",
        "error": "#eb6f92"
    },
    "catppuccin_mocha": {
        "bg": "#1e1e2e",
        "fg": "#cdd6f4",
        "frame_bg": "#313244",
        "button_bg": "#45475a",
        "button_fg": "#cdd6f4",
        "entry_bg": "#1e1e2e",
        "entry_fg": "#cdd6f4",
        "label_fg": "#b4befe",
        "highlight": "#89b4fa",
        "success": "#a6e3a1",
        "warning": "#f9e2af",
        "error": "#f38ba8"
    },
    "deep_ocean": {
        "bg": "#0f1419",
        "fg": "#b3b1ad",
        "frame_bg": "#1b2936",
        "button_bg": "#273747",
        "button_fg": "#d9d7ce",
        "entry_bg": "#0e1419",
        "entry_fg": "#b3b1ad",
        "label_fg": "#4d5566",
        "highlight": "#39bae6",
        "success": "#7fd962",
        "warning": "#ffb454",
        "error": "#f51818"
    },
    "arctic_frost": {
        "bg": "#e8f4f8",
        "fg": "#2e3440",
        "frame_bg": "#f0f8ff",
        "button_bg": "#d8ecf3",
        "button_fg": "#2e3440",
        "entry_bg": "#ffffff",
        "entry_fg": "#2e3440",
        "label_fg": "#5e81ac",
        "highlight": "#5e81ac",
        "success": "#a3be8c",
        "warning": "#ebcb8b",
        "error": "#bf616a"
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
    "matrix_green": {
        "bg": "#0d1117",
        "fg": "#00ff41",
        "frame_bg": "#161b22",
        "button_bg": "#21262d",
        "button_fg": "#00ff41",
        "entry_bg": "#0d1117",
        "entry_fg": "#00ff41",
        "label_fg": "#39ff14",
        "highlight": "#00ff00",
        "success": "#00ff41",
        "warning": "#ffff00",
        "error": "#ff0000"
    },
    "coral_reef": {
        "bg": "#002635",
        "fg": "#ffffff",
        "frame_bg": "#003847",
        "button_bg": "#004a5c",
        "button_fg": "#ffffff",
        "entry_bg": "#001e2a",
        "entry_fg": "#ffffff",
        "label_fg": "#ff6b6b",
        "highlight": "#4ecdc4",
        "success": "#51cf66",
        "warning": "#ffd93d",
        "error": "#ff6b6b"
    },
    "midnight_purple": {
        "bg": "#2d1b69",
        "fg": "#ffffff",
        "frame_bg": "#3c2689",
        "button_bg": "#4b31a9",
        "button_fg": "#ffffff",
        "entry_bg": "#251653",
        "entry_fg": "#ffffff",
        "label_fg": "#b794f6",
        "highlight": "#9f7aea",
        "success": "#68d391",
        "warning": "#f6e05e",
        "error": "#fc8181"
    },
    "autumn_leaves": {
        "bg": "#2c1810",
        "fg": "#f4e4c1",
        "frame_bg": "#3d2317",
        "button_bg": "#4e2e1e",
        "button_fg": "#f4e4c1",
        "entry_bg": "#241209",
        "entry_fg": "#f4e4c1",
        "label_fg": "#e97451",
        "highlight": "#d2691e",
        "success": "#9acd32",
        "warning": "#daa520",
        "error": "#dc143c"
    },
    "electric_blue": {
        "bg": "#0a0e1a",
        "fg": "#e6f3ff",
        "frame_bg": "#1a1f35",
        "button_bg": "#2a3451",
        "button_fg": "#e6f3ff",
        "entry_bg": "#0d1220",
        "entry_fg": "#e6f3ff",
        "label_fg": "#64b5f6",
        "highlight": "#1e88e5",
        "success": "#4caf50",
        "warning": "#ff9800",
        "error": "#f44336"
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
    },
    "terminal_green": {
        "bg": "#001100",
        "fg": "#00ff00",
        "frame_bg": "#002200",
        "button_bg": "#003300",
        "button_fg": "#00ff00",
        "entry_bg": "#000800",
        "entry_fg": "#00ff00",
        "label_fg": "#00cc00",
        "highlight": "#00ff00",
        "success": "#00ff00",
        "warning": "#ffff00",
        "error": "#ff0000"
    }
}

class ToolTip:
    def __init__(self, widget, text, delay=500):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tooltip_window = None
        self.id = None
        self.x = self.y = 0
        widget.bind("<Enter>", self.schedule)
        widget.bind("<Leave>", self.unschedule)
        widget.bind("<ButtonPress>", self.unschedule)

    def schedule(self, event=None):
        self.unschedule()
        self.id = self.widget.after(self.delay, self.show_tooltip)

    def unschedule(self, event=None):
        if self.id:
            self.widget.after_cancel(self.id)
            self.id = None
        self.hide_tooltip()

    def show_tooltip(self):
        if self.tooltip_window or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify='left',
                         background="#ffffe0", relief='solid', borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tooltip(self):
        tw = self.tooltip_window
        self.tooltip_window = None
        if tw:
            tw.destroy()

class GlassButton(tk.Button):
    """Custom glass-effect button with hover animations"""
    def __init__(self, parent, text="", command=None, color="#4d94ff", **kwargs):
        super().__init__(parent, text=text, command=command, **kwargs)
        self.default_color = color
        self.hover_color = self._lighten_color(color, 30)
        
        self.configure(
            bg=self.default_color,
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            bd=0,
            padx=20,
            pady=10,
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
        self.theme = theme or THEMES["dark"]
        
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
    def __init__(self, parent, width=400, height=20, theme=None, **kwargs):
        super().__init__(parent, width=width, height=height, **kwargs)
        self.theme = theme or THEMES["dark"]
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
            # Gradient effect simulation with multiple rectangles
            for i in range(int(progress_width)):
                alpha = 1 - (i / progress_width) * 0.3
                color = self._blend_colors(self.theme["highlight"], self.theme["success"], i/progress_width)
                self.create_rectangle(
                    i, 1, i+1, self.height-1,
                    fill=color,
                    outline=""
                )
                
        # Border
        self.create_rectangle(
            0, 0, self.width, self.height,
            fill="",
            outline=self.theme["highlight"],
            width=2
        )
        
    def _blend_colors(self, color1, color2, ratio):
        """Blend two hex colors"""
        try:
            c1 = [int(color1[i:i+2], 16) for i in (1, 3, 5)]
            c2 = [int(color2[i:i+2], 16) for i in (1, 3, 5)]
            result = [int(c1[i] + (c2[i] - c1[i]) * ratio) for i in range(3)]
            return f"#{result[0]:02x}{result[1]:02x}{result[2]:02x}"
        except:
            return color1
            
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
        self.animation_queue = []
        self.is_scraping = False
        
        # Setup custom fonts
        self.setup_fonts()
        
        # Initialize UI
        self.setup_modern_ui()
        
        # Start animation loop
        self._animate()
        
    def setup_fonts(self):
        """Setup custom fonts for the application"""
        self.title_font = font.Font(family="Segoe UI", size=24, weight="bold")
        self.subtitle_font = font.Font(family="Segoe UI", size=14, weight="normal")
        self.body_font = font.Font(family="Segoe UI", size=11)
        self.button_font = font.Font(family="Segoe UI", size=11, weight="bold")
        
    def setup_modern_ui(self):
        """Create the modern, stunning UI"""
        self.root.title("✨ Adobe Stock Prompt Generator Pro")
        self.root.geometry("1400x900")
        self.root.configure(bg=self.theme["bg"])
        self.root.resizable(True, True)
        
        # Create main container with modern layout
        self.main_container = tk.Frame(self.root, bg=self.theme["bg"])
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header section with gradient effect
        self.create_header()
        
        # Main content area with modern cards
        self.create_main_content()
        
        # Modern sidebar
        self.create_sidebar()
        
        # Footer with status and animations
        self.create_footer()
        
        # Apply initial theme
        self.apply_modern_theme()
        
    def create_header(self):
        """Create stunning header with animations"""
        header_frame = tk.Frame(
            self.main_container, 
            bg=self.theme["bg"], 
            height=120
        )
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Animated title
        self.title_label = tk.Label(
            header_frame,
            text="🚀 Adobe Stock Prompt Generator",
            bg=self.theme["bg"],
            fg=self.theme["highlight"],
            font=self.title_font
        )
        self.title_label.pack(pady=(20, 5))
        
        # Subtitle with animation
        self.subtitle_label = tk.Label(
            header_frame,
            text="AI-Powered Content Scraping with Style",
            bg=self.theme["bg"],
            fg=self.theme["label_fg"],
            font=self.subtitle_font
        )
        self.subtitle_label.pack()
        
        # Animated separator line
        self.separator_canvas = tk.Canvas(
            header_frame, 
            height=3, 
            bg=self.theme["bg"],
            highlightthickness=0
        )
        self.separator_canvas.pack(fill="x", pady=(10, 0))
        self._animate_separator()
        
    def create_main_content(self):
        """Create main content area with modern cards"""
        content_frame = tk.Frame(self.main_container, bg=self.theme["bg"])
        content_frame.pack(fill="both", expand=True)
        
        # Left panel - Main controls
        left_panel = tk.Frame(content_frame, bg=self.theme["bg"])
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # URL Configuration Card
        self.create_url_card(left_panel)
        
        # Format Settings Card  
        self.create_format_card(left_panel)
        
        # Control Panel Card
        self.create_control_card(left_panel)
        
    def create_url_card(self, parent):
        """Create URL configuration card"""
        url_card = ModernCard(parent, "🌐 URL Configuration", self.theme)
        url_card.pack(fill="x", pady=(0, 15))
        
        # URL input with modern styling
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
        
        # Page range with modern input fields
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
        self.end_page_entry.insert(0, "10")
        
    def create_format_card(self, parent):
        """Create format settings card"""
        format_card = ModernCard(parent, "⚙️ Format Settings", self.theme)
        format_card.pack(fill="x", pady=(0, 15))
        
        # Checkboxes with modern styling
        checkbox_frame = tk.Frame(format_card.content_frame, bg=self.theme["frame_bg"])
        checkbox_frame.pack(fill="x", pady=(0, 15))
        
        # Create Boolean variables
        self.include_prefix_var = BooleanVar(value=True)
        self.include_suffix_var = BooleanVar(value=True)
        self.include_date_var = BooleanVar(value=True)
        self.include_params_var = BooleanVar(value=True)
        self.include_ar_var = BooleanVar(value=True)
        self.lowercase_var = BooleanVar(value=False)
        
        # Create checkboxes in a grid
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
        
        # Create input fields with labels
        self._create_input_field(inputs_frame, "Prefix:", "prefix_entry", self.generate_random_prefix())
        self._create_input_field(inputs_frame, "Suffix:", "custom_suffix_entry", "dumnaf")
        self._create_input_field(inputs_frame, "Aspect Ratio:", "aspect_ratio_entry", "16:9")
        self._create_input_field(inputs_frame, "Parameters:", "additional_params_entry", "--no dust --p 5y3izqx")
        self._create_input_field(inputs_frame, "Filename:", "filename_entry", "output")
        
    def _create_input_field(self, parent, label, attr_name, default_value):
        """Create a modern input field"""
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
            text="🚀 Start Scraping",
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
        
    def apply_theme(self):
        """Apply theme to entire application as a cohesive unit"""
        # Configure all ttk widget styles comprehensively
        style_configs = {
            # Basic widgets
            "TFrame": {"background": self.theme["frame_bg"]},
            "TLabel": {"background": self.theme["frame_bg"], "foreground": self.theme["label_fg"]},
            "TButton": {
                "background": self.theme["button_bg"], 
                "foreground": self.theme["button_fg"],
                "relief": "flat",
                "borderwidth": 1
            },
            "TCheckbutton": {
                "background": self.theme["frame_bg"], 
                "foreground": self.theme["label_fg"],
                "focuscolor": self.theme["highlight"]
            },
            "TEntry": {
                "fieldbackground": self.theme["entry_bg"], 
                "foreground": self.theme["entry_fg"],
                "bordercolor": self.theme["highlight"],
                "insertcolor": self.theme["entry_fg"]
            },
            "TCombobox": {
                "fieldbackground": self.theme["entry_bg"], 
                "foreground": self.theme["entry_fg"],
                "bordercolor": self.theme["highlight"],
                "arrowcolor": self.theme["label_fg"]
            },
            
            # Notebook and tabs
            "TNotebook": {"background": self.theme["frame_bg"]},
            "TNotebook.Tab": {
                "background": self.theme["button_bg"], 
                "foreground": self.theme["button_fg"],
                "padding": [10, 5]
            },
            
            # Label frames
            "TLabelframe": {"background": self.theme["frame_bg"]},
            "TLabelframe.Label": {
                "background": self.theme["frame_bg"], 
                "foreground": self.theme["highlight"],
                "font": ("Arial", 9, "bold")
            },
            
            # Progress bar
            "TProgressbar": {
                "background": self.theme["highlight"],
                "troughcolor": self.theme["entry_bg"],
                "borderwidth": 0,
                "lightcolor": self.theme["highlight"],
                "darkcolor": self.theme["highlight"]
            },
            
            # Scrollbar
            "Vertical.TScrollbar": {
                "background": self.theme["button_bg"],
                "troughcolor": self.theme["frame_bg"],
                "bordercolor": self.theme["frame_bg"],
                "arrowcolor": self.theme["label_fg"],
                "darkcolor": self.theme["button_bg"],
                "lightcolor": self.theme["button_bg"]
            },
            "Horizontal.TScrollbar": {
                "background": self.theme["button_bg"],
                "troughcolor": self.theme["frame_bg"],
                "bordercolor": self.theme["frame_bg"],
                "arrowcolor": self.theme["label_fg"],
                "darkcolor": self.theme["button_bg"],
                "lightcolor": self.theme["button_bg"]
            }
        }
        
        # Apply all styles
        for style_name, style_options in style_configs.items():
            self.style.configure(style_name, **style_options)
        
        # Configure hover states for interactive elements
        self.style.map("TButton",
                      background=[('active', self.theme["highlight"]),
                                ('pressed', self.theme["entry_bg"])],
                      foreground=[('active', self.theme["bg"]),
                                ('pressed', self.theme["entry_fg"])])
        
        self.style.map("TCombobox",
                      fieldbackground=[('readonly', self.theme["entry_bg"]),
                                     ('focus', self.theme["entry_bg"])],
                      bordercolor=[('focus', self.theme["highlight"])])
        
        self.style.map("TEntry",
                      bordercolor=[('focus', self.theme["highlight"])])
        
        self.style.map("TNotebook.Tab",
                      background=[('selected', self.theme["highlight"]),
                                ('active', self.theme["frame_bg"])],
                      foreground=[('selected', self.theme["bg"]),
                                ('active', self.theme["highlight"])])
        
        # Apply theme to main window and all frames
        self.root.configure(bg=self.theme["bg"])
        
        # Apply theme to all text areas and custom widgets
        self._apply_text_widget_theme()
        
        # Update canvas-based elements
        try:
            self.theme_preview_canvas.configure(bg=self.theme["frame_bg"])
        except:
            pass
            
    def _apply_text_widget_theme(self):
        """Apply theme to all text-based widgets"""
        text_widgets = []
        
        # Collect all text widgets
        try:
            text_widgets.append(self.preview_area)
        except:
            pass
        try:
            text_widgets.append(self.log_area)
        except:
            pass
            
        # Apply theme to each text widget
        for widget in text_widgets:
            try:
                widget.configure(
                    bg=self.theme["entry_bg"], 
                    fg=self.theme["entry_fg"],
                    insertbackground=self.theme["entry_fg"],
                    selectbackground=self.theme["highlight"],
                    selectforeground=self.theme["bg"],
                    relief="flat",
                    borderwidth=1
                )
            except:
                pass
        
    def create_main_tab(self):
        self.main_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.main_frame, text="Main")
        
        # URL input section
        url_frame = ttk.LabelFrame(self.main_frame, text="URL Settings")
        url_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(url_frame, text="Adobe Stock URL:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.url_entry = ttk.Entry(url_frame, width=80)
        self.url_entry.grid(row=0, column=1, padx=5, pady=5)
        self.url_entry.insert(0, "https://stock.adobe.com/vn/search?creator_id=206854500&filters%5Bcontent_type%3Aphoto%5D=1&filters%5Bcontent_type%3Aillustration%5D=1&filters%5Bcontent_type%3Azip_vector%5D=1&filters%5Bcontent_type%3Avideo%5D=1&filters%5Bcontent_type%3Atemplate%5D=1&filters%5Bcontent_type%3A3d%5D=1&filters%5Bcontent_type%3Aaudio%5D=0&filters%5Binclude_stock_enterprise%5D=0&filters%5Bis_editorial%5D=0&filters%5Bfetch_excluded_assets%5D=1&filters%5Bcontent_type%3Aimage%5D=1&order=relevance&get_facets=0&search_type=pagination")
        ToolTip(self.url_entry, "Enter the Adobe Stock URL to scrape prompts from")
        
        # Page range
        ttk.Label(url_frame, text="Start Page:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.start_page_entry = ttk.Entry(url_frame, width=10)
        self.start_page_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        self.start_page_entry.insert(0, "1")
        ToolTip(self.start_page_entry, "Enter the starting page number for scraping")
        
        ttk.Label(url_frame, text="End Page:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.end_page_entry = ttk.Entry(url_frame, width=10)
        self.end_page_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        self.end_page_entry.insert(0, "10")
        ToolTip(self.end_page_entry, "Enter the ending page number for scraping")
        
        # Format settings
        format_frame = ttk.LabelFrame(self.main_frame, text="Format Settings")
        format_frame.pack(fill="x", padx=10, pady=5)
        
        # Include/Exclude options
        include_options_frame = ttk.LabelFrame(format_frame, text="Include in Prompt")
        include_options_frame.grid(row=0, column=0, columnspan=3, sticky="w", padx=5, pady=5)
        
        # Create Boolean variables for checkboxes
        self.include_prefix_var = BooleanVar(value=True)
        self.include_suffix_var = BooleanVar(value=True)
        self.include_date_var = BooleanVar(value=True)
        self.include_params_var = BooleanVar(value=True)
        self.include_ar_var = BooleanVar(value=True)
        self.lowercase_var = BooleanVar(value=False)
        
        # Add checkboxes for each element
        ttk.Checkbutton(include_options_frame, text="Include Prefix", variable=self.include_prefix_var, command=self.update_preview).grid(row=0, column=0, sticky="w", padx=5, pady=2)
        ToolTip(include_options_frame.winfo_children()[-1], "Include a random prefix at the beginning of each prompt")
        
        ttk.Checkbutton(include_options_frame, text="Include Suffix", variable=self.include_suffix_var, command=self.update_preview).grid(row=0, column=1, sticky="w", padx=5, pady=2)
        ToolTip(include_options_frame.winfo_children()[-1], "Include a custom suffix at the end of each prompt")
        
        ttk.Checkbutton(include_options_frame, text="Include Date", variable=self.include_date_var, command=self.update_preview).grid(row=0, column=2, sticky="w", padx=5, pady=2)
        ToolTip(include_options_frame.winfo_children()[-1], "Include the current date in DDMMYYYY format")
        
        ttk.Checkbutton(include_options_frame, text="Include Parameters", variable=self.include_params_var, command=self.update_preview).grid(row=1, column=0, sticky="w", padx=5, pady=2)
        ToolTip(include_options_frame.winfo_children()[-1], "Include additional parameters in each prompt")
        
        ttk.Checkbutton(include_options_frame, text="Include Aspect Ratio", variable=self.include_ar_var, command=self.update_preview).grid(row=1, column=1, sticky="w", padx=5, pady=2)
        ToolTip(include_options_frame.winfo_children()[-1], "Include aspect ratio parameter in each prompt")
        
        ttk.Checkbutton(include_options_frame, text="Convert to Lowercase", variable=self.lowercase_var, command=self.update_preview).grid(row=1, column=2, sticky="w", padx=5, pady=2)
        ToolTip(include_options_frame.winfo_children()[-1], "Convert all text in prompts to lowercase")
        
        # Format settings (moved down)
        ttk.Label(format_frame, text="Prefix:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.prefix_entry = ttk.Entry(format_frame, width=20)
        self.prefix_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        self.prefix_entry.insert(0, self.generate_random_prefix())
        ToolTip(self.prefix_entry, "Custom prefix for prompts (leave empty for random)")
        
        ttk.Button(format_frame, text="Generate New", command=lambda: self.prefix_entry.delete(0, tk.END) or self.prefix_entry.insert(0, self.generate_random_prefix())).grid(row=1, column=2, padx=5, pady=5)
        ToolTip(format_frame.winfo_children()[-1], "Generate a new random prefix")
        
        ttk.Label(format_frame, text="Custom Suffix:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.custom_suffix_entry = ttk.Entry(format_frame, width=20)
        self.custom_suffix_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        self.custom_suffix_entry.insert(0, "dumnaf")
        ToolTip(self.custom_suffix_entry, "Custom suffix to append to each prompt")
        
        ttk.Label(format_frame, text="Aspect Ratio:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.aspect_ratio_var = tk.StringVar(value="16:9")
        self.aspect_ratio_combo = ttk.Combobox(format_frame, textvariable=self.aspect_ratio_var, values=["16:9", "4:3", "1:1", "9:16"])
        self.aspect_ratio_combo.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        ToolTip(self.aspect_ratio_combo, "Select aspect ratio for image generation")
        
        ttk.Label(format_frame, text="Additional Parameters:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.additional_params_entry = ttk.Entry(format_frame, width=40)
        self.additional_params_entry.grid(row=4, column=1, columnspan=2, sticky="w", padx=5, pady=5)
        self.additional_params_entry.insert(0, "--no dust --p 5y3izqx")
        ToolTip(self.additional_params_entry, "Additional parameters for image generation")
        
        ttk.Label(format_frame, text="Output Filename:").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.filename_entry = ttk.Entry(format_frame, width=20)
        self.filename_entry.grid(row=5, column=1, sticky="w", padx=5, pady=5)
        self.filename_entry.insert(0, "output")
        ToolTip(self.filename_entry, "Base name for the output file (date/time will be appended)")
        
        # Progress bar
        self.progress = ttk.Progressbar(self.main_frame, orient="horizontal", length=200, mode="determinate")
        self.progress.pack(pady=10)
        ToolTip(self.progress, "Shows progress of scraping operation")
        
        # Buttons
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(button_frame, text="Start Scraping", command=self.start_scraping).pack(side=tk.LEFT, padx=5)
        ToolTip(button_frame.winfo_children()[-1], "Start the scraping process")
        
        ttk.Button(button_frame, text="Update Preview", command=self.update_preview).pack(side=tk.LEFT, padx=5)
        ToolTip(button_frame.winfo_children()[-1], "Update the preview with current settings")
        
        ttk.Button(button_frame, text="Open Folder", command=self.open_current_folder).pack(side=tk.LEFT, padx=5)
        ToolTip(button_frame.winfo_children()[-1], "Open the folder containing the generated files")
        
    def create_settings_tab(self):
        self.settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_frame, text="Settings")
        
        # Theme selection
        theme_frame = ttk.LabelFrame(self.settings_frame, text="Theme Settings")
        theme_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(theme_frame, text="Select Theme:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.theme_var = tk.StringVar(value=self.current_theme)
        theme_list = list(THEMES.keys())
        theme_combo = ttk.Combobox(theme_frame, textvariable=self.theme_var, values=theme_list, state="readonly", width=15)
        theme_combo.grid(row=0, column=1, padx=5, pady=5)
        theme_combo.bind("<<ComboboxSelected>>", self.change_theme)
        ToolTip(theme_combo, "Select the UI theme from available options")
        
        # Theme Preview
        theme_preview_frame = ttk.LabelFrame(self.settings_frame, text="Theme Colors Preview")
        theme_preview_frame.pack(fill="x", padx=10, pady=5)
        
        # Create theme preview canvas
        self.theme_preview_canvas = tk.Canvas(theme_preview_frame, height=60)
        self.theme_preview_canvas.pack(fill="x", padx=5, pady=5)
        self.update_theme_preview()
        ToolTip(self.theme_preview_canvas, "Preview of the currently selected theme colors")
        
        # Preview settings
        preview_frame = ttk.LabelFrame(self.settings_frame, text="Preview Settings")
        preview_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(preview_frame, text="Preview Lines:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.preview_lines_var = tk.StringVar(value="5")
        preview_lines_entry = ttk.Entry(preview_frame, textvariable=self.preview_lines_var, width=10)
        preview_lines_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        ToolTip(preview_lines_entry, "Number of lines to show in preview (not implemented yet)")
        
    def create_preview_tab(self):
        self.preview_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.preview_frame, text="Preview")
        
        # Preview section
        preview_label_frame = ttk.LabelFrame(self.preview_frame, text="Prompt Preview")
        preview_label_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.preview_area = scrolledtext.ScrolledText(preview_label_frame, wrap=tk.WORD, height=15)
        self.preview_area.pack(fill="both", expand=True, padx=5, pady=5)
        ToolTip(self.preview_area, "Preview of how your prompts will look")
        
    def create_log_tab(self):
        self.log_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.log_frame, text="Log")
        
        # Log section
        log_label_frame = ttk.LabelFrame(self.log_frame, text="Activity Log")
        log_label_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.log_area = scrolledtext.ScrolledText(log_label_frame, wrap=tk.WORD, height=20)
        self.log_area.pack(fill="both", expand=True, padx=5, pady=5)
        ToolTip(self.log_area, "Shows detailed logs of the scraping process")
        
        # Clear log button
        ttk.Button(self.log_frame, text="Clear Log", command=lambda: self.log_area.delete(1.0, tk.END)).pack(pady=5)
        ToolTip(self.log_frame.winfo_children()[-1], "Clear the log window")
        
    def change_theme(self, event=None):
        self.current_theme = self.theme_var.get()
        self.theme = THEMES[self.current_theme]
        self.apply_theme()
        self.update_theme_preview()
        self.status_label.config(text=f"Theme changed to {self.current_theme}")
        
    def update_theme_preview(self):
        """Update the theme color preview canvas"""
        try:
            # Clear the canvas
            self.theme_preview_canvas.delete("all")
            
            # Get canvas dimensions
            canvas_width = self.theme_preview_canvas.winfo_width()
            if canvas_width <= 1:  # Canvas not yet rendered
                canvas_width = 600  # Default width
            canvas_height = 60
            
            # Color swatches to display
            colors = [
                ("Background", self.theme["bg"]),
                ("Frame", self.theme["frame_bg"]),
                ("Button", self.theme["button_bg"]),
                ("Entry", self.theme["entry_bg"]),
                ("Label", self.theme["label_fg"]),
                ("Highlight", self.theme["highlight"]),
                ("Success", self.theme["success"]),
                ("Warning", self.theme["warning"]),
                ("Error", self.theme["error"])
            ]
            
            # Calculate swatch dimensions
            swatch_width = canvas_width // len(colors)
            
            # Draw color swatches
            for i, (name, color) in enumerate(colors):
                x1 = i * swatch_width
                x2 = x1 + swatch_width
                y1 = 10
                y2 = 40
                
                # Draw color rectangle
                self.theme_preview_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#666666")
                
                # Add label below
                text_color = "#ffffff" if self._is_dark_color(color) else "#000000"
                self.theme_preview_canvas.create_text(
                    x1 + swatch_width//2, y2 + 10, 
                    text=name, 
                    fill=self.theme["label_fg"], 
                    font=("Arial", 8)
                )
                
        except Exception as e:
            # If there's an error, just show the theme name
            self.theme_preview_canvas.create_text(
                300, 30, 
                text=f"Current Theme: {self.current_theme.title()}", 
                fill=self.theme["label_fg"], 
                font=("Arial", 12)
            )
    
    def _is_dark_color(self, hex_color):
        """Determine if a color is dark or light"""
        try:
            # Remove # if present
            hex_color = hex_color.lstrip('#')
            # Convert to RGB
            rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            # Calculate brightness
            brightness = sum(rgb) / 3
            return brightness < 128
        except:
            return True
        
    def generate_random_prefix(self):
        prefix = ''.join(random.choice(string.digits) for _ in range(7))
        logger.info(f"Generated random prefix: {prefix}")
        return prefix
        
    def update_preview(self):
        # Get values from UI
        prefix = self.prefix_entry.get() or self.generate_random_prefix() if self.include_prefix_var.get() else ""
        custom_suffix = self.custom_suffix_entry.get() or "dumnaf" if self.include_suffix_var.get() else ""
        aspect_ratio = self.aspect_ratio_entry.get() if self.include_ar_var.get() else ""
        additional_params = self.additional_params_entry.get() or "--no dust --p 5y3izqx" if self.include_params_var.get() else ""
        
        # Format current date
        current_date = datetime.now().strftime('%d%m%Y') if self.include_date_var.get() else ""
        
        # Create sample preview
        sample_text = "A cheerful real estate agent exhibits a spacious, empty office with large windows. The setting radiates opportunity and potential, ideal for businesses ready to move forward."
        
        # Apply lowercase conversion if enabled
        if self.lowercase_var.get():
            sample_text = sample_text.lower()
        
        # Build preview text based on included elements
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
        if os.name == 'nt':  # For Windows
            os.startfile(current_dir)
        else:  # For macOS and Linux
            subprocess.call(['open', current_dir])
            
    def start_scraping(self):
        try:
            url = self.url_entry.get()
            start_page = int(self.start_page_entry.get())
            end_page = int(self.end_page_entry.get())
            custom_suffix = self.custom_suffix_entry.get() if self.include_suffix_var.get() else ""
            aspect_ratio = self.aspect_ratio_entry.get() if self.include_ar_var.get() else ""
            additional_params = self.additional_params_entry.get() if self.include_params_var.get() else ""
            base_filename = self.filename_entry.get() or "output"
            
            self.status_label.config(text=f"Scraping pages {start_page} to {end_page}...")
            self.log_area.insert(tk.END, f"Starting scrape from page {start_page} to {end_page}\n")
            
            # Set up Chrome options
            options = Options()
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--disable-gpu')
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--enable-unsafe-swiftshader')  # Fix for WebGL deprecation warnings
            
            self.log_area.insert(tk.END, "Setting up Chrome driver...\n")
            self.log_area.see(tk.END)
            logger.info("Setting up Chrome driver")
            
            # Set up ChromeDriver
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            
            # Base URL for scraping
            base_url = url
            
            # Function to scrape titles from a page
            def scrape_page(url):
                try:
                    self.log_area.insert(tk.END, f"Accessing URL: {url}\n")
                    self.log_area.see(tk.END)
                    self.root.update()
                    
                    driver.get(url)
                    time.sleep(5)  # Wait for page load
                    
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    titles = soup.find_all('meta', itemprop='name')
                    
                    self.log_area.insert(tk.END, f"Found {len(titles)} titles on page\n")
                    self.log_area.see(tk.END)
                    self.root.update()
                    
                    return [title.get('content', '').strip() for title in titles]
                except Exception as e:
                    error_msg = f"Error scraping page: {e}"
                    self.log_area.insert(tk.END, error_msg + "\n")
                    self.log_area.see(tk.END)
                    logger.error(error_msg)
                    return []
            
            # Collect all titles
            all_titles = []
            total_pages = end_page - start_page + 1
            # Update progress bar maximum
            self.progress_bar.set_max(total_pages)
            
            for i, page in enumerate(range(start_page, end_page + 1)):
                url = f"{base_url}&search_page={page}"
                self.log_area.insert(tk.END, f"Scraping page {page}: {url}\n")
                self.log_area.see(tk.END)
                self.root.update()
                
                page_titles = scrape_page(url)
                all_titles.extend(page_titles)
                time.sleep(1)  # Avoid overwhelming the server
                
                # Update progress bar
                self.progress_bar.set_progress(i + 1)
                self.root.update()
            
            # Remove duplicates while preserving order
            self.log_area.insert(tk.END, f"Total titles before removing duplicates: {len(all_titles)}\n")
            unique_titles = list(dict.fromkeys(all_titles))
            self.log_area.insert(tk.END, f"Unique titles after removing duplicates: {len(unique_titles)}\n")
            self.log_area.see(tk.END)
            
            # Format prompts
            formatted_prompts = []
            prefix = self.prefix_entry.get() or self.generate_random_prefix() if self.include_prefix_var.get() else ""
            current_date = datetime.now().strftime('%d%m%Y') if self.include_date_var.get() else ""
            
            for count, title in enumerate(unique_titles, 1):
                if title:
                    # Build prompt based on included elements
                    prompt = ""
                    
                    if self.include_prefix_var.get():
                        prompt += f"{prefix} {count:02d} "
                    
                    # Apply lowercase conversion if enabled
                    formatted_title = title.lower() if self.lowercase_var.get() else title
                    prompt += formatted_title
                    
                    if self.include_date_var.get():
                        prompt += f" {current_date}"
                    
                    if self.include_suffix_var.get():
                        prompt += custom_suffix
                    
                    if self.include_params_var.get():
                        prompt += f" {additional_params}"
                    
                    if self.include_ar_var.get():
                        prompt += f" --ar {aspect_ratio}"
                    
                    formatted_prompts.append(prompt)
            
            # Generate filename with date and time
            current_datetime = datetime.now()
            formatted_date = current_datetime.strftime('%d%m%Y%H%M%S')
            filename = f"{base_filename}{formatted_date}tic.txt"
            
            # Export to a text file
            self.log_area.insert(tk.END, f"Writing prompts to file: {filename}\n")
            skipped_count = 0
            with open(filename, 'w', encoding='utf-8') as file:
                for prompt in formatted_prompts:
                    try:
                        # Try to encode the prompt to check for problematic characters
                        prompt.encode('utf-8')
                        file.write(prompt + '\n')
                    except UnicodeEncodeError as e:
                        skipped_count += 1
                        error_msg = f"Skipped problematic prompt: {prompt[:30]}... ({str(e)})"
                        self.log_area.insert(tk.END, error_msg + "\n")
                        logger.warning(error_msg)
            
            self.log_area.insert(tk.END, f"Scraping completed. {len(formatted_prompts) - skipped_count} prompts saved to {filename}\n")
            if skipped_count > 0:
                self.log_area.insert(tk.END, f"Skipped {skipped_count} problematic prompts\n")
            self.status_label.config(text=f"Completed! Saved to {filename} ({skipped_count} skipped)")
            self.log_area.see(tk.END)
            
            # Reset progress bar
            self.progress_bar.set_progress(0)
            
            # Close the browser
            driver.quit()
            
        except Exception as e:
            error_msg = f"Critical error: {str(e)}"
            self.log_area.insert(tk.END, error_msg + "\n")
            self.log_area.see(tk.END)
            logger.error(error_msg, exc_info=True)
            self.status_label.config(text="Error occurred! Check logs.")
            self.progress_bar.set_progress(0)

    def create_sidebar(self):
        """Create a modern sidebar with stats and quick actions"""
        sidebar_frame = tk.Frame(self.main_container, bg=self.theme["frame_bg"], width=300)
        sidebar_frame.pack(side="right", fill="y", padx=(10, 0))
        sidebar_frame.pack_propagate(False)
        
        # Preview section
        preview_card = ModernCard(sidebar_frame, "👁️ Live Preview", self.theme)
        preview_card.pack(fill="x", pady=(0, 15))
        
        # Preview text area
        self.preview_area = tk.Text(
            preview_card.content_frame,
            bg=self.theme["entry_bg"],
            fg=self.theme["entry_fg"],
            height=10,
            relief="flat",
            bd=0,
            font=self.body_font,
            wrap="word"
        )
        self.preview_area.pack(fill="both", expand=True)
        
        # Stats card
        stats_card = ModernCard(sidebar_frame, "📊 Statistics", self.theme)
        stats_card.pack(fill="x", pady=(0, 15))
        
        # Create stats display
        self.stats_frame = tk.Frame(stats_card.content_frame, bg=self.theme["frame_bg"])
        self.stats_frame.pack(fill="both", expand=True)
        
        # Stats metrics
        stats = [
            ("📑 Total Prompts", "0", "total_prompts_label"),
            ("⏱️ Estimated Time", "0:00", "time_label"),
            ("✅ Success Rate", "100%", "success_rate_label")
        ]
        
        for i, (title, value, attr_name) in enumerate(stats):
            stat_frame = tk.Frame(self.stats_frame, bg=self.theme["frame_bg"])
            stat_frame.pack(fill="x", pady=(0, 10))
            
            tk.Label(
                stat_frame,
                text=title,
                bg=self.theme["frame_bg"],
                fg=self.theme["label_fg"],
                font=self.body_font
            ).pack(anchor="w")
            
            value_label = tk.Label(
                stat_frame,
                text=value,
                bg=self.theme["frame_bg"],
                fg=self.theme["highlight"],
                font=self.subtitle_font
            )
            value_label.pack(anchor="w")
            
            setattr(self, attr_name, value_label)
        
        # Theme selection card
        theme_card = ModernCard(sidebar_frame, "🎨 Theme", self.theme)
        theme_card.pack(fill="x")
        
        theme_frame = tk.Frame(theme_card.content_frame, bg=self.theme["frame_bg"])
        theme_frame.pack(fill="x")
        
        # Theme selector
        self.theme_var = tk.StringVar(value=self.current_theme)
        theme_list = list(THEMES.keys())
        
        tk.Label(
            theme_frame,
            text="Select Theme:",
            bg=self.theme["frame_bg"],
            fg=self.theme["label_fg"],
            font=self.body_font
        ).pack(anchor="w", pady=(0, 5))
        
        # Create a dropdown with modern styling
        theme_dropdown = ttk.Combobox(
            theme_frame,
            textvariable=self.theme_var,
            values=theme_list,
            state="readonly",
            font=self.body_font,
            width=20
        )
        theme_dropdown.pack(fill="x", ipady=5)
        theme_dropdown.bind("<<ComboboxSelected>>", self.change_theme)
        
        # Theme preview
        self.theme_preview_canvas = tk.Canvas(
            theme_frame,
            height=40,
            bg=self.theme["frame_bg"],
            highlightthickness=0
        )
        self.theme_preview_canvas.pack(fill="x", pady=10)
        self.update_theme_preview()
        
        # Log area (hidden, for compatibility)
        self.log_area = tk.Text(
            sidebar_frame,
            height=1,
            width=1,
            bg=self.theme["entry_bg"],
            fg=self.theme["entry_fg"],
            relief="flat",
            bd=0,
            font=self.body_font,
            wrap="word"
        )
        # Don't pack it - just create for compatibility
    
    def create_footer(self):
        """Create footer with status information and animations"""
        footer_frame = tk.Frame(self.root, bg=self.theme["frame_bg"], height=30)
        footer_frame.pack(side="bottom", fill="x")
        footer_frame.pack_propagate(False)
        
        # Status text with animation
        self.status_label = tk.Label(
            footer_frame,
            text="✨ Ready to scrape",
            bg=self.theme["frame_bg"],
            fg=self.theme["label_fg"],
            font=self.body_font,
            anchor="w"
        )
        self.status_label.pack(side="left", padx=10)
        
        # Version info
        version_label = tk.Label(
            footer_frame,
            text="v2.0 Pro",
            bg=self.theme["frame_bg"],
            fg=self.theme["label_fg"],
            font=self.body_font
        )
        version_label.pack(side="right", padx=10)
    
    def apply_modern_theme(self):
        """Apply modern theme to the entire application"""
        # Configure all main container elements
        self.main_container.configure(bg=self.theme["bg"])
        
        # Apply theme to custom widgets
        for widget in self.main_container.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.configure(bg=self.theme["bg"])
        
        # Update progress bar theme if it exists
        try:
            self.progress_bar.theme = self.theme
            self.progress_bar._draw_progress()
        except:
            pass
        
        # Update header elements
        try:
            self.title_label.configure(bg=self.theme["bg"], fg=self.theme["highlight"])
            self.subtitle_label.configure(bg=self.theme["bg"], fg=self.theme["label_fg"])
            self.separator_canvas.configure(bg=self.theme["bg"])
            self._animate_separator()
        except:
            pass
    
    def _animate(self):
        """Main animation loop"""
        try:
            # Process animation queue
            for animation in self.animation_queue:
                animation()
                
            # Pulse animation on separator line
            self._pulse_separator()
            
            # Update progress bar pulse if scraping
            if self.is_scraping:
                self._pulse_progress()
        except Exception as e:
            print(f"Animation error: {e}")
            
        # Continue animation loop
        self.root.after(50, self._animate)
    
    def _animate_separator(self):
        """Create initial gradient separator line"""
        try:
            self.separator_canvas.delete("separator")
            width = self.separator_canvas.winfo_width()
            if width <= 1:  # Not yet rendered
                width = 800
                
            # Create gradient line
            for i in range(width):
                # Create a gradient color
                ratio = i / width
                color = self._blend_colors(self.theme["highlight"], self.theme["success"], ratio)
                self.separator_canvas.create_line(
                    i, 1, i, 3,
                    fill=color,
                    tags="separator"
                )
                
            # Add pulsing highlight
            self.separator_pos = 0
            self.separator_direction = 1
        except:
            pass
    
    def _pulse_separator(self):
        """Create pulsing animation on separator"""
        try:
            width = self.separator_canvas.winfo_width()
            if width <= 1:  # Not yet rendered
                return
                
            # Move highlight pulse across line
            self.separator_pos += 5 * self.separator_direction
            
            # Reverse direction at edges
            if self.separator_pos >= width or self.separator_pos <= 0:
                self.separator_direction *= -1
                
            # Create highlight pulse
            pulse_width = 100
            start = max(0, self.separator_pos - pulse_width//2)
            end = min(width, self.separator_pos + pulse_width//2)
            
            # Update highlight
            self.separator_canvas.delete("pulse")
            for i in range(start, end):
                distance = abs(i - self.separator_pos)
                intensity = 1 - distance / (pulse_width/2)
                if intensity > 0:
                    color = self._lighten_color(self.theme["highlight"], intensity * 70)
                    self.separator_canvas.create_line(
                        i, 0, i, 4,
                        fill=color,
                        width=1,
                        tags="pulse"
                    )
        except:
            pass
    
    def _pulse_progress(self):
        """Create pulsing animation on progress bar during scraping"""
        try:
            if hasattr(self, 'progress_bar'):
                # Create subtle pulse animation
                current = self.progress_bar.progress
                pulse = math.sin(time.time() * 5) * 2
                self.progress_bar.set_progress(current + pulse)
        except:
            pass
    
    def _blend_colors(self, color1, color2, ratio):
        """Blend two hex colors"""
        try:
            c1 = [int(color1[i:i+2], 16) for i in (1, 3, 5)]
            c2 = [int(color2[i:i+2], 16) for i in (1, 3, 5)]
            result = [int(c1[i] + (c2[i] - c1[i]) * ratio) for i in range(3)]
            return f"#{result[0]:02x}{result[1]:02x}{result[2]:02x}"
        except:
            return color1
    
    def _lighten_color(self, color, percent):
        """Lighten a hex color by a percentage"""
        try:
            color = color.lstrip('#')
            rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
            rgb = tuple(min(255, int(c + (255-c)*percent/100)) for c in rgb)
            return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
        except:
            return color
    
    def change_theme(self, event=None):
        """Change the application theme"""
        new_theme = self.theme_var.get()
        if new_theme in THEMES:
            self.current_theme = new_theme
            self.theme = THEMES[self.current_theme]
            
            # Apply theme to all elements
            self.apply_modern_theme()
            self.update_theme_preview()
            
            # Update status
            self.status_label.config(
                text=f"🎨 Theme changed to {self.current_theme.title()}",
                bg=self.theme["frame_bg"],
                fg=self.theme["label_fg"]
            )
    
    def update_theme_preview(self):
        """Update the theme color preview canvas"""
        try:
            # Clear the canvas
            self.theme_preview_canvas.delete("all")
            
            # Get canvas dimensions
            canvas_width = self.theme_preview_canvas.winfo_width()
            if canvas_width <= 1:  # Canvas not yet rendered
                canvas_width = 280  # Default width for sidebar
            canvas_height = 40
            
            # Color swatches to display (fewer colors for sidebar)
            colors = [
                ("BG", self.theme["bg"]),
                ("Frame", self.theme["frame_bg"]),
                ("Highlight", self.theme["highlight"]),
                ("Success", self.theme["success"])
            ]
            
            # Calculate swatch dimensions
            swatch_width = canvas_width // len(colors)
            
            # Draw color swatches
            for i, (name, color) in enumerate(colors):
                x1 = i * swatch_width
                x2 = x1 + swatch_width
                y1 = 5
                y2 = 25
                
                # Draw color rectangle
                self.theme_preview_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#666666")
                
                # Add label below
                self.theme_preview_canvas.create_text(
                    x1 + swatch_width//2, y2 + 10, 
                    text=name, 
                    fill=self.theme["label_fg"], 
                    font=("Arial", 7)
                )
                
        except Exception as e:
            # If there's an error, just show the theme name
            self.theme_preview_canvas.create_text(
                140, 20, 
                text=f"Theme: {self.current_theme.title()}", 
                fill=self.theme["label_fg"], 
                font=("Arial", 10)
            )
    
    def start_scraping_threaded(self):
        """Start scraping in a separate thread to keep UI responsive"""
        if not self.is_scraping:
            self.is_scraping = True
            self.start_button.configure(text="🛑 Stop Scraping", bg="#e74c3c")
            threading.Thread(target=self.start_scraping, daemon=True).start()
        else:
            self.is_scraping = False
            self.start_button.configure(text="🚀 Start Scraping", bg=self.theme["success"])
    
    def start_scraping(self):
        try:
            url = self.url_entry.get()
            start_page = int(self.start_page_entry.get())
            end_page = int(self.end_page_entry.get())
            custom_suffix = self.custom_suffix_entry.get() if self.include_suffix_var.get() else ""
            aspect_ratio = self.aspect_ratio_entry.get() if self.include_ar_var.get() else ""
            additional_params = self.additional_params_entry.get() if self.include_params_var.get() else ""
            base_filename = self.filename_entry.get() or "output"
            
            # Update UI
            self.status_label.config(text=f"🔍 Scraping pages {start_page} to {end_page}...")
            self.log_area.delete(1.0, tk.END)
            self.log_area.insert(tk.END, f"✨ Starting scrape from page {start_page} to {end_page}\n")
            
            # Set up Chrome options
            options = Options()
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--disable-gpu')
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--enable-unsafe-swiftshader')
            
            # Start timer
            start_time = time.time()
            
            # Setup ChromeDriver
            self.log_area.insert(tk.END, "🚀 Setting up Chrome driver...\n")
            self.log_area.see(tk.END)
            logger.info("Setting up Chrome driver")
            
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            base_url = url
            
            # Progress setup
            total_pages = end_page - start_page + 1
            self.progress_bar.set_max(total_pages)
            
            # Collect all titles
            all_titles = []
            for i, page in enumerate(range(start_page, end_page + 1)):
                if not self.is_scraping:  # Check if stop was requested
                    break
                    
                # Update progress
                self.progress_bar.set_progress(i)
                
                # Scrape page
                page_url = f"{base_url}&search_page={page}"
                self.log_area.insert(tk.END, f"📄 Scraping page {page}...\n")
                self.log_area.see(tk.END)
                
                # Update UI stats
                elapsed = time.time() - start_time
                self.time_label.configure(text=f"{int(elapsed//60):02}:{int(elapsed%60):02}")
                
                # Get page content
                driver.get(page_url)
                time.sleep(3)  # Wait for page load
                
                # Parse content
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                titles = soup.find_all('meta', itemprop='name')
                page_titles = [title.get('content', '').strip() for title in titles]
                
                self.log_area.insert(tk.END, f"✅ Found {len(page_titles)} titles on page {page}\n")
                self.log_area.see(tk.END)
                
                all_titles.extend(page_titles)
                time.sleep(1)  # Avoid overwhelming server
                
                # Update total count
                self.total_prompts_label.configure(text=str(len(all_titles)))
            
            # Process collected titles
            if not self.is_scraping:  # Check if stop was requested
                self.log_area.insert(tk.END, "⛔ Scraping stopped by user\n")
                driver.quit()
                self.is_scraping = False
                self.start_button.configure(text="🚀 Start Scraping", bg=self.theme["success"])
                return
                
            # Remove duplicates
            self.log_area.insert(tk.END, f"📊 Total titles before removing duplicates: {len(all_titles)}\n")
            unique_titles = list(dict.fromkeys(all_titles))
            self.log_area.insert(tk.END, f"📊 Unique titles after filtering: {len(unique_titles)}\n")
            
            # Format prompts
            formatted_prompts = []
            prefix = self.prefix_entry.get() or self.generate_random_prefix() if self.include_prefix_var.get() else ""
            current_date = datetime.now().strftime('%d%m%Y') if self.include_date_var.get() else ""
            
            for count, title in enumerate(unique_titles, 1):
                if not self.is_scraping:  # Check if stop was requested
                    break
                    
                if title:
                    # Build prompt
                    prompt = ""
                    if self.include_prefix_var.get():
                        prompt += f"{prefix} {count:02d} "
                    
                    # Apply lowercase if needed
                    formatted_title = title.lower() if self.lowercase_var.get() else title
                    prompt += formatted_title
                    
                    # Add date if needed
                    if self.include_date_var.get():
                        prompt += f" {current_date}"
                    
                    # Add suffix if needed
                    if self.include_suffix_var.get():
                        prompt += custom_suffix
                    
                    # Add parameters if needed
                    if self.include_params_var.get():
                        prompt += f" {additional_params}"
                    
                    # Add aspect ratio if needed
                    if self.include_ar_var.get():
                        prompt += f" --ar {aspect_ratio}"
                    
                    formatted_prompts.append(prompt)
            
            # Create output file
            if not self.is_scraping:  # Check if stop was requested
                self.log_area.insert(tk.END, "⛔ Scraping stopped by user\n")
                driver.quit()
                self.is_scraping = False
                self.start_button.configure(text="🚀 Start Scraping", bg=self.theme["success"])
                return
                
            # Generate filename
            formatted_date = datetime.now().strftime('%d%m%Y%H%M%S')
            filename = f"{base_filename}{formatted_date}tic.txt"
            
            # Save to file
            self.log_area.insert(tk.END, f"💾 Writing prompts to file: {filename}\n")
            skipped_count = 0
            
            with open(filename, 'w', encoding='utf-8') as file:
                for prompt in formatted_prompts:
                    try:
                        prompt.encode('utf-8')  # Check for encoding issues
                        file.write(prompt + '\n')
                    except UnicodeEncodeError:
                        skipped_count += 1
            
            # Update success rate
            success_rate = 100 - (skipped_count / max(1, len(formatted_prompts)) * 100)
            self.success_rate_label.configure(text=f"{success_rate:.1f}%")
            
            # Show completion message
            elapsed = time.time() - start_time
            self.log_area.insert(tk.END, f"✅ Scraping completed in {int(elapsed//60)}m {int(elapsed%60)}s!\n")
            self.log_area.insert(tk.END, f"📁 {len(formatted_prompts) - skipped_count} prompts saved to {filename}\n")
            
            if skipped_count > 0:
                self.log_area.insert(tk.END, f"⚠️ Skipped {skipped_count} prompts with encoding issues\n")
                
            self.status_label.config(text=f"✅ Completed! Saved to {filename}")
            self.log_area.see(tk.END)
            
            # Reset progress bar
            self.progress_bar.set_progress(0)
            
            # Close browser
            driver.quit()
            
            # Sound notification
            self.root.bell()
            
            # Show success message
            messagebox.showinfo("Scraping Completed", f"Successfully saved {len(formatted_prompts) - skipped_count} prompts to {filename}")
            
        except Exception as e:
            # Handle errors
            error_msg = f"❌ Error: {str(e)}"
            self.log_area.insert(tk.END, error_msg + "\n")
            self.log_area.see(tk.END)
            logger.error(error_msg, exc_info=True)
            self.status_label.config(text="⚠️ Error occurred! Check logs.")
            
            # Show error message
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
        finally:
            # Reset UI state
            self.is_scraping = False
            self.start_button.configure(text="🚀 Start Scraping", bg=self.theme["success"])

# Create main window with special effects
root = tk.Tk()
root.title("Adobe Stock Prompt Generator Pro")

# Set window icon if available
try:
    icon_path = "icon.ico"
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)
except:
    pass
    
# Add modern splash screen
try:
    # Create splash screen
    splash = tk.Toplevel(root)
    splash.overrideredirect(True)
    
    # Center splash window
    width, height = 400, 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    splash.geometry(f"{width}x{height}+{x}+{y}")
    
    # Add content
    splash.configure(bg="#1a1b26")
    splash_label = tk.Label(
        splash, 
        text="Adobe Stock\nPrompt Generator Pro", 
        font=("Segoe UI", 22, "bold"),
        bg="#1a1b26",
        fg="#7aa2f7",
        justify="center"
    )
    splash_label.pack(pady=(80, 10))
    
    version_label = tk.Label(
        splash, 
        text="Version 2.0", 
        font=("Segoe UI", 12),
        bg="#1a1b26",
        fg="#c0caf5"
    )
    version_label.pack()
    
    # Progress bar
    splash_progress = ttk.Progressbar(
        splash, 
        orient="horizontal", 
        length=300, 
        mode="determinate"
    )
    splash_progress.pack(pady=20)
    
    # Update splash progress
    def update_splash_progress(value):
        splash_progress["value"] = value
        splash.update_idletasks()
    
    # Close splash after loading
    def close_splash():
        update_splash_progress(100)
        splash.destroy()
    
    # Show splash for a moment
    for i in range(0, 101, 5):
        update_splash_progress(i)
        splash.update()
        time.sleep(0.03)
    
    root.after(500, close_splash)
    
    # Hide main window until splash is done
    root.withdraw()
    root.after(1000, root.deiconify)
except Exception as e:
    print(f"Splash screen error: {e}")
    # Ensure main window is shown
    root.deiconify()

# Initialize app
app = ModernUI(root)

# Start application
root.mainloop()
