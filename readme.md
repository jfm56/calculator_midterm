# **Command-Line Calculator with Plugin System**

---

## **📌 Overview**

This modular command-line calculator is designed with a plugin-based architecture, enabling dynamic addition of new arithmetic and statistical operations. The system provides an interactive menu, history tracking using Pandas, and comprehensive testing with high test coverage.

Built with **Python 3.13+**, the calculator leverages plugins for operations, **pytest** for testing, **Faker** for dynamic test generation, and **Pandas** for managing historical data. It also supports customizable test records via the `--num_record=<N>` CLI option.

### **🌟 Features**

✅ **Plugin-Based System** – Easily extendable with dynamically loaded arithmetic and statistical operations.  
✅ **Interactive REPL Mode** – Menu-driven interface with real-time calculations.  
✅ **History Tracking** – View, retrieve, and clear past calculations using **Pandas-based storage**.  
✅ **Robust Testing Suite** – High test coverage with **pytest**, **Faker**, and **parameterized tests**.  
✅ **Custom Test Data** – Generate test cases dynamically using `--num_record=<N>`.  
✅ **Code Quality & CI/CD** – Linting with **Pylint**, testing with **pytest-cov**, and maintainable architecture.  
✅ **Extensible Design** – Easily add new arithmetic or statistical operations without modifying the core logic.  
✅ **Persistent History Storage** – **history.csv** stores calculation history across sessions.  
✅ **Environment Configuration** – Supports `.env` files for managing configurations.  
✅ **Demonstration Video** – A tutorial video will be available to showcase the calculator's functionality.  

---

## **⚙️ Installation**

Ensure **Python 3.13+** is installed. Then, clone the repository and install dependencies:

```bash
git clone https://github.com/jfm56/Calculator_midterm.git
cd Calculator_midterm
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```
---

## **🚀 Usage**

### **Run the Interactive Menu**
Start the calculator in interactive mode:

```bash
python main.py
```

### **Perform Direct Command-Line Calculations**
Run operations directly from the terminal:
```bash
python main.py add 10 5
# Output: ✅ Result: 15.00
```
```bash
python main.py divide 20 4
# Output: ✅ Result: 5.00
```

---

## **📜 Interactive Menu**

The calculator supports an interactive **REPL (Read-Eval-Print Loop)**, allowing users to perform calculations seamlessly.

### **🔹 Interactive Menu Example:**
```bash
== Welcome to REPL Calculator ==
Type 'menu' for options, or enter calculations (e.g., add 2 3).
>> menu

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

### **💡 Example Calculation in REPL Mode:**
```bash
>> add 5 3
✅ Result: 8.00

>> divide 10 2
✅ Result: 5.00

>> history
📜 Calculation History:
1. add 5 3 = 8.00
2. divide 10 2 = 5.00

>> remove 1
✅ Entry 1 removed successfully.

>> clear
✅ History cleared.

>> exit
👋 Exiting calculator...
```
---

## **🛠️ Configuration**

### **Persistent History Storage**
The calculator saves all calculations to `history.csv`, allowing users to retain their calculation history across sessions.

### **Environment Variables**
Environment configuration settings can be managed via a `.env` file to set paths, logging configurations, or other runtime parameters.

### **🎲 Faker-based Test Data**

The test suite uses **Faker** to generate randomized test cases dynamically. To control the number of test cases generated:
```bash
pytest --num_record=10
```

---

## **🧪 Testing**

Run the test suite with full coverage:
```bash
pytest --cov=main --cov=operations --cov=history --cov=tests --cov-report=term-missing
```
Check code quality:
```bash
pylint main.py operations history.py tests/
```

---

## **🔌 Extending the Calculator**

### **Adding a New Operation**
To add a new arithmetic or statistical operation, follow these steps:

1️⃣ **Create a new file** in the `operations/` directory, e.g., `modulus.py`.
2️⃣ **Define a class** that inherits from `OperationBase`:
```python
from operations.operation_base import OperationBase
from decimal import Decimal

class Modulus(OperationBase):
    """Modulus operation for remainder calculation."""
    @classmethod
    def execute(cls, a, b):
        return Decimal(a) % Decimal(b)
```
3️⃣ **Register the new operation** in `operation_mapping.py`:
```python
operation_mapping = {
    "add": Add,
    "subtract": Subtract,
    "multiply": Multiply,
    "divide": Divide,
    "mean": Mean,
    "median": Median,
    "std_dev": StandardDeviation,
    "variance": Variance,
    "modulus": Modulus,  # ✅ New operation added
}
```
4️⃣ The **plugin system will automatically load the new operation** when the calculator runs.

---

## **📂 Project Structure**

```bash
Calculator2/
│── .github/               # CI/CD pipeline configuration
│── app/                   # Application utilities
│   ├── menu.py
│── config/                # Configuration files
│── history/               # Calculation history management
│   ├── history.py
│── mappings/              # Operation mappings
│── operations/            # Arithmetic & statistical operation plugins
│   ├── add.py
│   ├── subtract.py
│   ├── multiply.py
│   ├── divide.py
│   ├── statistics.py    # Mean, Median, Std_dev, Variance
│   ├── operation_base.py
│   ├── operation_mapping.py
│── tests/                 # Unit & integration tests
│   ├── conftest.py
│   ├── test_main.py
│   ├── test_operations.py
│   ├── test_history.py
│   ├── test_menu.py
│   ├── test_operation_base.py
│   ├── test_plugins.py
│   ├── test_statistics.py
│── .coveragerc            # Coverage configuration
│── history.csv            # Calculation history file
│── main.py                # Main CLI program
│── .env                   # Environment configuration
│── README.md              # Project documentation
│── requirements.txt       # Dependencies
```
---

## **📄 License**

This project is licensed under the **MIT License**. You are free to modify and distribute the software with attribution.

---

## **👨‍💻 Author**

Developed by **Jim Mullen**. Contributions and improvements are welcome!

📧 Contact: [GitHub](https://github.com/jfm56)

---

## **🔗 References & Acknowledgments**
- [Python 3.13 Documentation](https://docs.python.org/3/)
- [Pytest](https://docs.pytest.org/)
- [Faker](https://faker.readthedocs.io/)
- [Pylint](https://pylint.pycqa.org/)

---

🚀 **Happy Calculating!** 🎯

