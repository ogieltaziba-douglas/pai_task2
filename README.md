# Market Basket Analysis

A market basket analysis system using custom data structures and algorithms to analyze customer purchasing patterns from supermarket transaction data. Built with **Test-Driven Development (TDD)**.

## Project Structure

```
pai_task2/
├── data/raw/                  # Supermarket dataset (14,963 transactions)
├── src/
│   ├── data_structures/       # Custom Graph class
│   ├── algorithms/            # BFS, DFS, Merge Sort
│   ├── analysis/              # Association queries
│   └── utils/                 # Data loading utilities
├── tests/unit/                # 139 unit tests
├── app/                       # Streamlit web interface
└── docs/                      # Documentation
```

## Features

- **Custom Graph Data Structure**: Adjacency list implementation for item relationships
- **Search Algorithms**: BFS and DFS with depth limiting
- **Custom Merge Sort**: O(n log n) sorting (replaces built-in `sorted()`)
- **Association Queries**: Find items bought together, top bundles
- **Interactive Web App**: Streamlit + PyVis network visualization

## Quick Start

### Installation

```bash
git clone https://github.com/ogieltaziba-douglas/pai_task2
cd pai_task2
pip install -r requirements.txt
```

### Run Web Application

```bash
streamlit run app/streamlit_app.py
```

Opens at `http://localhost:8501`

### Run Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=src --cov-report=html
```

**Current Status**: 139 tests passing, 94.5% coverage

## Key Algorithms

| Algorithm | Time Complexity | Use Case |
|-----------|----------------|----------|
| **BFS** | O(V + E) | Find associated items by depth |
| **DFS** | O(V + E) | Graph traversal |
| **Merge Sort** | O(n log n) | Sort bundles by frequency |

## Dataset

- **Source**: `data/raw/Supermarket_dataset_PAI.csv`
- **Transactions**: 14,963
- **Unique Items**: 167
- **Item Pairs**: 6,260

## Dependencies

- Python 3.8+
- Streamlit
- Plotly
- PyVis
- Pandas
- Pytest

## Author

Ogieltaziba Douglas

---

*Academic project following TDD methodology*

