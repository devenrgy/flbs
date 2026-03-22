# FLBS — Flibusta Book Search

> **⚠️ Note:** Tested only on Linux with Flibusta & Librusec (lib.rus.ec) distribution + FLibrary [640514 books] (2009-2026) [FB2] [Updatable]

**FLBS** is an alternative to FLibrary program, written in Python. A console utility for fast searching and downloading books from Flibusta/Librusec library.

---

## 📋 Table of Contents

- [Features](#-features)
- [Dependencies](#-dependencies)
- [Installation](#-installation)
- [Environment Variables Setup](#-environment-variables-setup)
- [Usage](#-usage)
- [Recommendations](#-recommendations)
- [First Run](#-first-run)
- [Uninstall](#-uninstall)
- [Support the Project](#-support-the-project)

---

## ✨ Features

- 🔍 **Search by Author** — find books by author name
- 📚 **Search by Title** — search by book title
- 🏷️ **Search by Genre** — filter by genres
- 📖 **Search by Series** — view series with book counts
- 🌐 **Language Filter** — filter books by language (ru, en, etc.)
- ⬇️ **Download Books** — download selected books in FB2 format
- 🔄 **Sorting** — sort results by date (ascending/descending)
- 📄 **Pagination** — convenient page-by-page results browsing
- 🖼️ **Extract Covers and Images** — automatic illustration extraction
- 💾 **Results Caching** — quick access to last search results
- 🔁 **Rebuild Index** — full database update capability

---

## 📦 Dependencies

The following dependencies are required for the program to work correctly:

### System Utilities

| Utility | Purpose |
|---------|---------|
| `p7zip` / `p7zip-full` | Unpack .7z archives |
| `libxml2-utils` | `xmllint` utility for XML formatting |
| `djxl` (libjxl) | Convert images to JPEG |

### Python Dependencies

```
# See requirements.txt file
```

---

## 🚀 Installation

### 1. Install System Dependencies

#### **Debian/Ubuntu:**
```bash
sudo apt update
sudo apt install p7zip-full libxml2-utils libjxl-extra
```

#### **Fedora:**
```bash
sudo dnf install p7zip libxml2 libjxl-tools
```

#### **Arch Linux:**
```bash
sudo pacman -S p7zip libxml2 libjxl
```

#### **openSUSE:**
```bash
sudo zypper install p7zip libxml2-tools libjxl-tools
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Environment Variables Setup

The program requires four environment variables to be set for correct operation.

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `FLBS_PATH` | Path to Flibusta library directory | `/home/user/flibusta` |
| `FLBS_INPX` | Index file name .inpx | `flibusta.inpx` |
| `FLBS_SAVE` | Directory to save downloaded books | `/home/user/Books` |
| `FLBS_DB` | Path to SQLite database file | `/home/user/.local/share/flbs/books.db` |

### Setup for Different Shells

#### **Bash** (~/.bashrc or ~/.bash_profile)

```bash
export FLBS_PATH="/home/user/flibusta"
export FLBS_INPX="flibusta.inpx"
export FLBS_SAVE="/home/user/Books"
export FLBS_DB="/home/user/.local/share/flbs/books.db"
```

**Apply changes:**
```bash
source ~/.bashrc
```

#### **Fish** (~/.config/fish/config.fish)

```fish
set -x FLBS_PATH "/home/user/flibusta"
set -x FLBS_INPX "flibusta.inpx"
set -x FLBS_SAVE "/home/user/Books"
set -x FLBS_DB "/home/user/.local/share/flbs/books.db"
```

**Apply changes:**
```fish
source ~/.config/fish/config.fish
```

#### **Zsh** (~/.zshrc)

```bash
export FLBS_PATH="/home/user/flibusta"
export FLBS_INPX="flibusta.inpx"
export FLBS_SAVE="/home/user/Books"
export FLBS_DB="/home/user/.local/share/flbs/books.db"
```

**Apply changes:**
```bash
source ~/.zshrc
```

### Setup on Windows

#### **Via PowerShell (temporary session):**

```powershell
$env:FLBS_PATH="C:\flibusta"
$env:FLBS_INPX="flibusta.inpx"
$env:FLBS_SAVE="C:\Users\Username\Books"
$env:FLBS_DB="C:\Users\Username\AppData\Local\flbs\books.db"
```

#### **Via Command Prompt (cmd):**

```cmd
set FLBS_PATH=C:\flibusta
set FLBS_INPX=flibusta.inpx
set FLBS_SAVE=C:\Users\Username\Books
set FLBS_DB=C:\Users\Username\AppData\Local\flbs\books.db
```

#### **Permanent Setup via PowerShell:**

```powershell
# Add to user environment variables
[Environment]::SetEnvironmentVariable("FLBS_PATH", "C:\flibusta", "User")
[Environment]::SetEnvironmentVariable("FLBS_INPX", "flibusta.inpx", "User")
[Environment]::SetEnvironmentVariable("FLBS_SAVE", "C:\Users\Username\Books", "User")
[Environment]::SetEnvironmentVariable("FLBS_DB", "C:\Users\Username\AppData\Local\flbs\books.db", "User")
```

**Restart your terminal after setup!**

---

## 📖 Usage

### Basic Commands

```bash
# Search by author
python flbs.py -a "Pushkin"

# Search by title
python flbs.py -t "War and Peace"

# Search by genre
python flbs.py -g "fantasy"

# Search by series
python flbs.py -s "Harry Potter"

# Search with language filter
python flbs.py -a "Asimov" -l en

# Download books by numbers from list
python flbs.py -a "Strugatsky" --download 1,3,5

# Download by book ID
python flbs.py -e 123456

# Show all genres
python flbs.py --genres

# Show all languages
python flbs.py --langs

# Rebuild index (full database update)
python flbs.py --reindex
```

### Interactive Mode

After search, you enter interactive mode with the following commands:

| Command | Description |
|---------|----------|
| `n` | Next page |
| `p` | Previous page |
| `g <number>` | Go to page |
| `da` | Sort by date (ascending) |
| `dd` | Sort by date (descending) |
| `dr` | Reset sorting |
| `l <language>` | Language filter (e.g., `l ru`) |
| `d <numbers>` | Download books (e.g., `d 1,3,5`) |
| `<` | Back (in series mode) |
| `q` | Quit |

---

## 📚 Recommendations

### Calibre

For convenient book library management, it is recommended to install **Calibre**.

#### Install Calibre

**Official website:** https://calibre-ebook.com/download

#### **Debian/Ubuntu:**
```bash
sudo apt install calibre
```

#### **Fedora:**
```bash
sudo dnf install calibre
```

#### **Arch Linux:**
```bash
sudo pacman -S calibre
```

#### **openSUSE:**
```bash
sudo zypper install calibre
```

#### **macOS:**
```bash
brew install --cask calibre
```

### Auto-Load Books

For automatic tracking and adding downloaded books to Calibre:

1. Open Calibre
2. Go to **Preferences** → **Advanced** → **Auto-adding folders**
3. Add the folder specified in `FLBS_SAVE` variable
4. Enable **"Automatically add books"** option

Now all downloaded books will automatically appear in your Calibre library!

---

## ⏳ First Run

On first use, you need to wait **1-2 minutes** for the SQLite database to be created.

The program will automatically:
1. Extract index files from `.inpx` archive
2. Create SQLite database
3. Index all books (~640,514 books)

**First run message:**
```
Extracting index from flibusta.inpx ...
Building SQLite index (one-time, ~1-2 min) ...
  000.inp: 100000 records
  001.inp: 150000 records
  ...
Done. Indexed: 640514 books.
```

Subsequent runs will be instant!

---

## 🗑️ Uninstall

If you need to remove the program and all data:

### 1. Remove Database
```bash
rm -f $FLBS_DB
```

### 2. Remove Cache
```bash
rm -f /tmp/flbs_last_results.json
```

### 3. Remove Index Files
```bash
rm -rf $FLIBUSTA_PATH/index
```

### 4. Remove Program
```bash
rm -rf /path/to/flbs
```

### 5. Remove Downloaded Books (optional)
```bash
rm -rf $FLBS_SAVE
```

### 6. Clean Environment Variables

Remove lines with `export FLBS_*` from your configuration files:
- `~/.bashrc`
- `~/.bash_profile`
- `~/.zshrc`
- `~/.config/fish/config.fish`

---

## 🌟 Support the Project

Enjoy using the program!

If you like the program:

- ⭐ **Star on GitHub** — helps the project grow
- 🐛 **Report a Bug** — create an Issue with problem description
- 💡 **Suggest an Idea** — share your improvement suggestions
- 🔄 **Fork** — contribute to project development

### Links

- 📦 **GitHub Releases:** [Download Latest Version](../../releases)
- 🐛 **Issue Tracker:** [Report a Problem](../../issues)
- 📝 **Discussions:** [GitHub Discussions](../../discussions)

---

## 📄 License

The project is distributed under the MIT license.

---

**Made with ❤️ for book lovers**
