# 🍌 Banana Shell | NL to SQL

![Visitors](https://api.visitorbadge.io/api/visitors?path=tjiuce2%2nlp-to-sql%20&countColor=%23263759&style=flat&initial=5767) ![License](https://img.shields.io/badge/License-MIT-4e3eb5) ![Languages](https://img.shields.io/github/languages/count/tjiuce/nlp-to-sql?color=20B2AA) ![GitHub Repo stars](https://img.shields.io/github/stars/tjiuce/nlp-to-sql) ![GitHub last commit](https://img.shields.io/github/last-commit/tjiuce/nlp-to-sql) ![GitHub repo size](https://img.shields.io/github/repo-size/tjiuce/nlp-to-sql) ![GitHub total lines](https://sloc.xyz/github/tjiuce/nlp-to-sql) <a href="https://bananashell.vercel.app"><img alt="Website" src="https://img.shields.io/website?url=https%3A%2F%2Fbananashell.vercel.app/%2F&up_message=awake&up_color=%2300d18f&down_message=asleep&down_color=red&style=flat">
</a>

**Banana Shell** is a futuristic, intelligent command-line shell designed to combine stunning visuals with powerful functionality.

### ✨ Features

- 💎 **Glasmorphism UI** – A sleek, modern interface with frosted-glass effects.
- 🌈 **Colorful Yet Clean** – Carefully chosen colors for clarity and style.
- 🧠 **Smart Capabilities** – Built-in **NLP to SQL** conversion for effortless querying.
- 🍌 **Banana Prompts** – Unique, intuitive prompts to enhance user experience.
- 🚀 **User-Friendly** – Designed for both developers and power users.

> 🍌 *Banana Shell: Where intelligence meets aesthetics in your terminal.*

---

## Architecture Pipeline

```mermaid
flowchart LR
    subgraph User Interaction
        User[User Query] --> Input[Natural Language Prompt]
    end

    subgraph NLP Engine
        Input --> Parser[NLP Query Tokenizer]
        Parser --> Schema[Database Schema Injector]
        Schema --> LLM[SQL Translation Model]
    end

    subgraph Execution & Validation
        LLM --> SQL[Generated SQL Query]
        SQL --> Validator[Syntax & Safety Validator]
        Validator --> DB[(Connected SQL Database)]
        DB --> Result[Formatted Result Set]
    end

    Result --> Display[Glassmorphism UI / Terminal Output]
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- Active SQL Database (MySQL, PostgreSQL, or SQLite)

### 1. Clone & Navigate
```bash
git clone https://github.com/tjiuce/nlp-to-sql.git
cd nlp-to-sql
```

### 2. Install Dependencies
```bash
pip install -r documentation/installation/requirements.txt
```

### 3. Configure Database Connection
Edit `app/src/db_config.py` with your database credentials:
```python
DB_HOST = "localhost"
DB_USER = "your_username"
DB_PASSWORD = "your_password"
DB_NAME = "your_database"
```

### 4. Launch Application
```bash
python app/src/main.py
```

## Sample Usage

| Natural Language Input | Generated SQL Query |
|---|---|
| *"Show all customers from New York"* | `SELECT * FROM customers WHERE city = 'New York';` |
| *"Find total sales by product category in 2024"* | `SELECT category, SUM(amount) FROM sales WHERE year = 2024 GROUP BY category;` |
| *"List top 5 highest order totals"* | `SELECT * FROM orders ORDER BY total_amount DESC LIMIT 5;` |

---

| Initial Screen |
|-|
| ![](https://github.com/tjiuce/nlp-to-sql/blob/main/documentation/images/init.png?raw=true) |

<details>
<summary>View More</summary>
  
| Database Connected |
|-|
| ![](https://github.com/tjiuce/nlp-to-sql/blob/main/documentation/images/success.png?raw=true) |

| Connection Failure |
|-|
| ![](https://github.com/tjiuce/nlp-to-sql/blob/main/documentation/images/failure.png?raw=true) |

</details>