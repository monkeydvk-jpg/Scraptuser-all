# 🚀 Scraptuser-All - Adobe Stock Prompt Generator

A comprehensive collection of tools for scraping Adobe Stock content and generating AI prompts, available in both desktop and web versions.

## 📁 Project Structure

```
Scraptuser-all/
├── v1.1/                    # Desktop Application (Python + Tkinter)
│   ├── customui_ready.py    # Main desktop application with modern UI
│   └── *.txt               # Generated prompt files
├── V2-Web/                  # Web Application (Next.js + React)
│   ├── src/                # Source code for web app
│   ├── package.json        # Dependencies and scripts
│   ├── vercel.json         # Vercel deployment config
│   └── README.md           # Web version documentation
├── app.py                   # Flask web interface (legacy)
└── README.md               # This file
```

## 🌟 Features

### 🖥️ Desktop Version (v1.1)
- **Modern Tkinter UI** with multiple themes
- **Real-time preview** of prompt formatting  
- **Progress tracking** with animated progress bars
- **Selenium-based scraping** with Chrome automation
- **Multi-theme support** (Cyberpunk, Dark, Light, Nord, etc.)
- **Error handling** and validation
- **File export** functionality

### 🌐 Web Version (V2-Web)
- **Next.js 14** with App Router
- **Responsive design** for all devices
- **Modern React components** with TypeScript
- **Real-time updates** and progress tracking
- **Puppeteer-based scraping** optimized for serverless
- **Download functionality** for generated prompts
- **Glass morphism UI** with smooth animations
- **Vercel deployment ready**

## 🚀 Quick Start

### Desktop Version
```bash
cd v1.1
python customui_ready.py
```

### Web Version
```bash
cd V2-Web
npm install
npm run dev
```

## 🛠️ Tech Stack

| Component | Desktop (v1.1) | Web (V2) |
|-----------|---------------|----------|
| **Frontend** | Tkinter | Next.js 14 + React 18 |
| **Language** | Python | TypeScript |
| **Scraping** | Selenium + Chrome | Puppeteer (serverless) |
| **Styling** | Custom Tkinter Themes | TailwindCSS + Custom CSS |
| **State** | Class-based | Zustand |
| **Deployment** | Executable | Vercel |

## 🎯 Usage

1. **Enter Adobe Stock URL** - Provide the search URL
2. **Set Page Range** - Define start and end pages  
3. **Configure Format** - Customize prefix, suffix, parameters
4. **Preview Output** - See formatted prompts in real-time
5. **Start Scraping** - Begin extraction process
6. **Download Results** - Save generated prompts

## 📊 Supported Features

- ✅ URL validation and page range settings
- ✅ Customizable prompt formatting
- ✅ Prefix/suffix configuration  
- ✅ Date inclusion options
- ✅ Aspect ratio parameters
- ✅ Case conversion (uppercase/lowercase)
- ✅ Real-time preview updates
- ✅ Progress tracking with visual feedback
- ✅ Error handling and recovery
- ✅ Multiple export formats
- ✅ Theme customization

## 🚀 Deployment

### Desktop Version
The desktop application runs locally with Python. Requirements:
- Python 3.8+
- Chrome browser
- Required packages: `selenium`, `beautifulsoup4`, `webdriver-manager`, `tkinter`

### Web Version  
Deploy to Vercel with one click:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/monkeydvk-jpg/Scraptuser-all)

Or manually:
```bash
cd V2-Web
npm install
vercel --prod
```

## 📈 Version History

### v2.0 Web (Latest)
- ✅ Complete Next.js rewrite
- ✅ Serverless architecture
- ✅ Mobile-responsive design
- ✅ TypeScript implementation
- ✅ Enhanced error handling

### v1.1 Desktop
- ✅ Modern Tkinter UI
- ✅ Multiple theme support
- ✅ Improved scraping logic
- ✅ Better error handling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/monkeydvk-jpg/Scraptuser-all/issues)
- **Discussions**: [GitHub Discussions](https://github.com/monkeydvk-jpg/Scraptuser-all/discussions)

## 🙏 Acknowledgments

- **Adobe Stock** for providing the content platform
- **Next.js Team** for the excellent React framework
- **Vercel** for seamless deployment platform
- **Open Source Community** for the amazing tools and libraries

---

**Built with ❤️ by the Scraptuser Team**

Choose your preferred version:
- 🖥️ **Desktop**: Full-featured local application
- 🌐 **Web**: Modern cloud-based solution
