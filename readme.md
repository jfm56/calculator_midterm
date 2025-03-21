# Advanced Python Command-Line Calculator with Plugin System

## 📌 Overview
This modular command-line calculator is designed with a plugin-based architecture, enabling dynamic addition of arithmetic and statistical operations. It features an interactive REPL, history tracking with Pandas, and comprehensive test coverage using Pytest and Faker. Built with **Python 3.13+**, the project also supports environment configuration, professional logging, and CI/CD via GitHub Actions.

---

## 🌟 Features
- ✅ **Plugin-Based Architecture** – Dynamically load new operations without modifying core logic.  
- ✅ **Interactive REPL Mode** – Menu-driven interface for real-time calculations.  
- ✅ **Calculation History** – View, retrieve, and clear history using Pandas and CSV.  
- ✅ **Comprehensive Testing** – Pytest with Faker and parameterized tests.  
- ✅ **Custom Test Generation** – Dynamic test data with `--num_record=<N>` option.  
- ✅ **CI/CD with GitHub Actions** – Code passes all tests on push and PR.  
- ✅ **Environment Variable Support** – Configurable logging and paths via `.env`.  
- ✅ **Professional Logging** – Configured log levels and formats using environment variables.  
- ✅ **Extensible Design** – Easily add new operations via the plugin system.

---

## ⚙️ Installation
```bash
git clone https://github.com/jfm56/Calculator_midterm.git
cd Calculator_midterm
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🚀 Usage

### Start REPL Mode
```bash
python main.py
```

### Direct Command Execution
```bash
python main.py add 10 5       # ✅ Result: 15.00
python main.py divide 20 4    # ✅ Result: 5.00
```

---

## 📜 Interactive Menu (REPL)
```text
📜 Calculator Menu:
==============================
🔹 Available Operations:
add, divide, mean, median, multiply, subtract
==============================
1️⃣ - View Calculation History
2️⃣ - Clear Calculation History
3️⃣ - Remove Entry by ID
4️⃣ - Reload History from CSV
5️⃣ - Exit Calculator
==============================
```

---

## 🧐 Design Pattern Usage

### Strategy & Factory Patterns
- The plugin system registers and retrieves operations dynamically via the `Operation` base class and `operation_mapping`.  
  [View Implementation → operation_base.py](./operations/operation_base.py)

### Facade Pattern
- The `History` class abstracts complex Pandas operations behind simple methods.  
  [View Implementation → history.py](./history/history.py)

### Command Pattern
- REPL input is parsed and routed to command handlers through the `Menu` and `CalculatorREPL` logic.  
  [View Implementation → menu.py](./app/menu.py)

---

## 🧪 Testing

### Run Tests with Coverage
```bash
pytest --cov=main --cov=operations --cov=history --cov=tests --cov-report=term-missing
```

### Run with Custom Test Records
```bash
pytest --num_record=10
```

### Lint Check
```bash
pylint main.py operations history tests
```

---

## 🔐 Environment Variables

- Managed via `.env` file.
- Supports custom logging levels and history paths.

```env
LOG_LEVEL=INFO
HISTORY_PATH=history.csv
```

[View Usage → log_config.py](./config/log_config.py)

---

## 📝 Exception Handling (LBYL vs EAFP)
- **EAFP**: Used in input validation with `Decimal()` conversion wrapped in `try/except`.  
  [Example → addition.py](./operations/addition.py)

- **LBYL**: Used in history operations like checking if the entry exists before removing.  
  [Example → menu.py](./app/menu.py)

---

## 📹 Video Demo
A short video walkthrough demonstrating REPL, plugin usage, history features, and error handling:  
[![Watch the video](https://img.youtube.com/vi/pvTk703yhU4/0.jpg)](https://youtu.be/pvTk703yhU4)


---

## 🔌 Adding a New Operation
1. Create a new file in `operations/`, e.g., `modulus.py`.
2. Inherit from `Operation` and implement `execute()`.
3. Register it in `operation_mapping.py`.
4. Done! It will appear in the REPL automatically.

---

## 📂 Project Structure
```
Calculator_midterm/
├── app/               # CLI menu and REPL
├── config/            # Logging and plugin loaders
├── history/           # Pandas-based history handler
├── mappings/          # Operation mapping
├── operations/        # Core + statistical operation plugins
├── tests/             # Pytest test suite
├── .env               # Configuration file
├── .github/           # GitHub Actions workflows
├── main.py            # CLI entry point
├── README.md          # Project documentation
```

---

## 📄 License
MIT License

## 👨‍💼 Author
Jim Mullen  
**GitHub:** [jfm56](https://github.com/jfm56)

---

🚀 Happy Calculating! 🎯

