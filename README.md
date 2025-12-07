# Market Basket Analysis - Data Structures & Algorithms

## 🎯 Project Overview

This project implements a comprehensive market basket analysis system using data structures and algorithms to analyze customer purchasing patterns from supermarket transaction data. Built following **Test-Driven Development (TDD)** principles with a web-based interface using Streamlit.

## 📋 Academic Context

**Module**: Programming and Algorithms  
**Task**: Task 2 - Data Structure and Algorithm Implementation  
**Development Approach**: Test-Driven Development (TDD)

## 🏗️ Project Structure

```
pai_task2/
├── data/                      # Data directory
│   ├── raw/                   # Raw datasets
│   ├── processed/             # Processed/cached data
│   └── sample/                # Sample data for testing
│
├── src/                       # Source code
│   ├── data_structures/       # Core data structures (Graph, Edge)
│   ├── algorithms/            # Algorithm implementations
│   ├── analysis/              # Business logic and queries
│   ├── visualization/         # Visualization functions
│   └── utils/                 # Utility functions
│
├── tests/                     # Test suite (TDD)
│   ├── conftest.py            # Pytest config & shared fixtures
│   └── unit/                  # Unit tests
│
├── app/                       # Streamlit web application
│   └── streamlit_app.py       # Main web interface
│
├── reports/                   # Analysis reports
└── notebooks/                 # Jupyter notebooks (exploration)
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd pai_task2
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🧪 Running Tests

This project follows **Test-Driven Development (TDD)** with comprehensive **unit testing**. Tests are written before implementation.

### Run all tests
```bash
pytest
```

### Run tests with coverage
```bash
pytest --cov=src --cov-report=html --cov-report=term
```

### Run specific test file
```bash
pytest tests/unit/test_graph.py
```

### View coverage report
After running tests with coverage, open `htmlcov/index.html` in your browser.

### Coverage Target
- Maintain **minimum 80% code coverage**
- All new features must have corresponding unit tests

## 🌐 Running the Web Application

Start the Streamlit web interface:

```bash
streamlit run app/streamlit_app.py
```

The application will open in your default browser at `http://localhost:8501`

## 📊 Features

- **Graph-based Item Network**: Represents items and their co-purchase relationships
- **Efficient Algorithms**: BFS/DFS for item associations, frequent itemset mining
- **Business Queries**: 
  - Find items frequently bought together
  - Identify top product bundles
  - Generate product recommendations
- **Interactive Visualization**: Web-based graph visualization with Streamlit
- **Comprehensive Testing**: Full test coverage with unit and integration tests

## 🛠️ Development Workflow

1. **Write Tests First** (TDD approach)
   - Create test file in `tests/unit/`
   - Write failing unit tests for new functionality
   
2. **Implement Functionality**
   - Write minimal code to pass tests
   - Refactor as needed
   
3. **Verify Coverage**
   - Run tests with coverage report
   - Ensure new code is adequately tested

4. **Commit Changes**
   - Make meaningful, atomic commits
   - Write clear commit messages

## 📚 Key Technologies

- **Core**: Python 3.8+
- **Data Processing**: NumPy, Pandas
- **Web Framework**: Streamlit
- **Visualization**: Matplotlib, Seaborn, Plotly, NetworkX
- **Testing**: Pytest, pytest-cov
- **Code Quality**: Black, Flake8, Pylint

## 📖 Documentation

See the `docs/` directory for:
- Design justification
- Computational complexity analysis
- API reference

## 🤝 Contributing

This is an academic project. For collaboration:
1. Follow TDD principles
2. Maintain test coverage above 80%
3. Write meaningful commit messages
4. Document code with docstrings

## 📝 License

Academic project - All rights reserved

## 👤 Author

Ogieltaziba Douglas

---

**Note**: This project is developed as part of an academic assignment following strict TDD methodology and software engineering best practices.
