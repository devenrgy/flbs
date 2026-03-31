# FLBS — Flibusta Book Search

> **⚠️ Примечание:** Тестировалось только на Linux с раздачей Флибуста (Flibusta) & Либрусек (lib.rus.ec) + FLibrary [640514 книги] (2009-2026) [FB2] [Обновляемая]

**FLBS** — это альтернатива программе FLibrary, написанная на Python. Консольная утилита для быстрого поиска и скачивания книг из библиотеки Флибуста/Либрусек.

---

## 📋 Оглавление

- [Возможности](#-возможности)
- [Зависимости](#-зависимости)
- [Установка](#-установка)
- [Настройка переменных окружения](#-настройка-переменных-окружения)
- [Использование](#-использование)
- [Рекомендации](#-рекомендации)
- [Первый запуск](#-первый-запуск)
- [Удаление](#-удаление)
- [Поддержка проекта](#-поддержка-проекта)
- [История изменений](#-история-изменений)

---

## ✨ Возможности

- 🔍 **Поиск по автору** — найдите книги по имени автора
- 📚 **Поиск по названию** — поиск по названию книги
- 🏷️ **Поиск по жанру** — фильтрация по жанрам
- 📖 **Поиск по серии** — просмотр серий с количеством книг
- 🌐 **Фильтр по языку** — отбор книг по языку (ru, en, и т.д.)
- ⬇️ **Скачивание книг** — загрузка выбранных книг в формате FB2
- 📚 **Скачивание серий** — загрузка всех книг из серии одной командой
- 🔄 **Сортировка** — сортировка результатов по дате (возрастание/убывание)
- 📄 **Пагинация** — удобный просмотр результатов по страницам
- 🖼️ **Извлечение обложек и изображений** — автоматическое добавление иллюстраций
- 💾 **Кэширование результатов** — быстрый доступ к последним результатам
- 🔁 **Пересборка индекса** — возможность полного обновления базы данных

---

## 📦 Зависимости

Для корректной работы программы необходимо установить следующие зависимости:

### Системные утилиты

| Утилита | Назначение |
|---------|------------|
| `p7zip` / `p7zip-full` | Распаковка архивов .7z |
| `libxml2-utils` | Утилита `xmllint` для форматирования XML |
| `djxl` (libjxl) | Конвертация изображений в JPEG |

### Python зависимости

```
# См. файл requirements.txt
```

---

## 🚀 Установка

### 1. Установка системных зависимостей

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

### 2. Установка Python зависимостей

```bash
pip install -r requirements.txt
```

---

## ⚙️ Настройка переменных окружения

Программа требует настройки четырёх переменных окружения для корректной работы.

### Переменные окружения

| Переменная | Описание | Пример |
|------------|----------|--------|
| `FLBS_PATH` | Путь к директории с библиотекой Флибуста | `/home/user/flibusta` |
| `FLBS_INPX` | Имя файла индекса .inpx | `flibusta.inpx` |
| `FLBS_SAVE` | Директория для сохранения скачанных книг | `/home/user/Books` |
| `FLBS_DB` | Путь к SQLite файлу базы данных | `/home/user/.local/share/flbs/books.db` |

### Настройка для разных оболочек

#### **Bash** (~/.bashrc или ~/.bash_profile)

```bash
export FLBS_PATH="/home/user/flibusta"
export FLBS_INPX="flibusta.inpx"
export FLBS_SAVE="/home/user/Books"
export FLBS_DB="/home/user/.local/share/flbs/books.db"
```

**Применить изменения:**
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

**Применить изменения:**
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

**Применить изменения:**
```bash
source ~/.zshrc
```

### Настройка на Windows

#### **Через PowerShell (временная сессия):**

```powershell
$env:FLBS_PATH="C:\flibusta"
$env:FLBS_INPX="flibusta.inpx"
$env:FLBS_SAVE="C:\Users\Username\Books"
$env:FLBS_DB="C:\Users\Username\AppData\Local\flbs\books.db"
```

#### **Через командную строку (cmd):**

```cmd
set FLBS_PATH=C:\flibusta
set FLBS_INPX=flibusta.inpx
set FLBS_SAVE=C:\Users\Username\Books
set FLBS_DB=C:\Users\Username\AppData\Local\flbs\books.db
```

#### **Постоянная настройка через PowerShell:**

```powershell
# Добавить в переменные среды пользователя
[Environment]::SetEnvironmentVariable("FLBS_PATH", "C:\flibusta", "User")
[Environment]::SetEnvironmentVariable("FLBS_INPX", "flibusta.inpx", "User")
[Environment]::SetEnvironmentVariable("FLBS_SAVE", "C:\Users\Username\Books", "User")
[Environment]::SetEnvironmentVariable("FLBS_DB", "C:\Users\Username\AppData\Local\flbs\books.db", "User")
```

**После настройки перезапустите терминал!**

---

## 📖 Использование

### Основные команды

```bash
# Поиск по автору
python flbs.py -a "Пушкин"

# Поиск по названию книги
python flbs.py -t "Война и мир"

# Поиск по жанру
python flbs.py -g "фантастика"

# Поиск по серии
python flbs.py -s "Гарри Поттер"

# Поиск с фильтром по языку
python flbs.py -a "Asimov" -l en

# Скачать книги по номерам из списка
python flbs.py -a "Стругацкий" --download 1,3,5

# Скачать по ID книги
python flbs.py -e 123456

# Показать все жанры
python flbs.py --genres

# Показать все языки
python flbs.py --langs

# Пересобрать индекс (полное обновление базы)
python flbs.py --reindex
```

### Интерактивный режим

После поиска вы попадаете в интерактивный режим с следующими командами:

| Команда | Описание |
|---------|----------|
| `n` | Следующая страница |
| `p` | Предыдущая страница |
| `g <номер>` | Перейти на страницу |
| `da` | Сортировать по дате (возрастание) |
| `dd` | Сортировать по дате (убывание) |
| `dr` | Сбросить сортировку |
| `l <язык>` | Фильтр по языку (например: `l ru`) |
| `d <номера>` | Скачать книги (например: `d 1,3,5`) |
| `dl` | Скачать все книги (в серии/на странице) |
| `o <номер>` | Открыть серию (в режиме просмотра серий) |
| `d <номер>` | Скачать все книги серии (в режиме просмотра серий) |
| `<` | Назад (в режиме серии) |
| `q` | Выход |

---

## 📚 Рекомендации

### Calibre

Для удобного управления библиотекой книг рекомендуется установить программу **Calibre**.

#### Установка Calibre

**Официальный сайт:** https://calibre-ebook.com/download

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

### Автозагрузка книг

Для автоматического отслеживания и добавления скачанных книг в Calibre:

1. Откройте Calibre
2. Перейдите в **Настройки** → **Дополнительно** → **Папки для автозагрузки**
3. Добавьте папку, указанную в переменной `FLBS_SAVE`
4. Включите опцию **"Автоматически добавлять книги"**

Теперь все скачанные книги будут автоматически появляться в вашей библиотеке Calibre!

---

## ⏳ Первый запуск

При первом использовании программы необходимо подождать **1-2 минуты** для создания SQLite базы данных.

Программа автоматически:
1. Распакует индексные файлы из `.inpx` архива
2. Создаст SQLite базу данных
3. Проиндексирует все книги (~640 514 книг)

**Сообщение при первом запуске:**
```
Extracting index from flibusta.inpx ...
Building SQLite index (one-time, ~1-2 min) ...
  000.inp: 100000 records
  001.inp: 150000 records
  ...
Done. Indexed: 640514 books.
```

Последующие запуски будут работать мгновенно!

---

## 🗑️ Удаление

Если вам потребуется удалить программу и все данные:

### 1. Удаление базы данных
```bash
rm -f $FLBS_DB
```

### 2. Удаление кэша
```bash
rm -f /tmp/flbs_last_results.json
```

### 3. Удаление индексных файлов
```bash
rm -rf $FLIBUSTA_PATH/index
```

### 4. Удаление программы
```bash
rm -rf /path/to/flbs
```

### 5. Удаление скачанных книг (опционально)
```bash
rm -rf $FLBS_SAVE
```

### 6. Очистка переменных окружения

Удалите строки с `export FLBS_*` из ваших файлов конфигурации:
- `~/.bashrc`
- `~/.bash_profile`
- `~/.zshrc`
- `~/.config/fish/config.fish`

---

## 🌟 Поддержка проекта

Всем приятного пользования!

Если вам понравилась программа:

- ⭐ **Поставьте звезду** на GitHub — это поможет проекту развиваться
- 🐛 **Сообщите об ошибке** — создайте Issue с описанием проблемы
- 💡 **Предложите идею** — поделитесь своими пожеланиями по улучшению
- 🔄 **Сделайте форк** — внесите свой вклад в развитие проекта

### Ссылки

- 📦 **GitHub Releases:** [Скачать последнюю версию](../../releases)
- 🐛 **Issue Tracker:** [Сообщить о проблеме](../../issues)
- 📝 **Обсуждения:** [GitHub Discussions](../../discussions)

---

## 📄 Лицензия

Проект распространяется под лицензией MIT.

---

**Сделано с ❤️ для любителей книг**
