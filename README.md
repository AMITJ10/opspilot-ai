# 🚀 OpsPilot AI — AI-Powered Business Analytics SaaS

**Transforming operational data into actionable business intelligence.**

OpsPilot AI is a cloud-deployed, multi-company business analytics platform built using Python, Streamlit, FastAPI, PostgreSQL, and Machine Learning.

The platform helps businesses monitor revenue, profitability, sales, operational performance, and customer trends through interactive dashboards. It also provides predictive analytics, anomaly detection, automated business insights, and a conversational interface for answering business questions.

Designed as a SaaS prototype, OpsPilot AI demonstrates the integration of data engineering, machine learning, backend development, authentication, and cloud deployment into a single application.

### 🌐 Live Demo and Repository

**Live Application:** https://opspilot-ai-gr24.onrender.com

**GitHub Repository:** https://github.com/AMITJ10/opspilot-ai

**Deployment Platform:** Render

*Note: The live application may take additional time to start after inactivity on Render's free tier.*

---

## 🎯 Problem Statement

Many small and medium-sized businesses rely on spreadsheets and disconnected systems to manage sales, expenses, customers, and operational activities.

This creates challenges such as:

- Limited visibility into business performance
- Difficulty identifying profitable customers and operational units
- Manual and time-consuming financial reporting
- Limited ability to predict future revenue
- Delayed detection of unusual transactions
- Lack of centralized analytics for business decisions

**OpsPilot AI addresses these challenges by providing a centralized analytics platform with machine learning capabilities.**

## ✨ Key Features

### 📊 1. Executive Analytics Dashboard

A centralized overview of important business performance indicators.

- Total revenue and gross profit
- Gross profit margin
- Total orders
- Monthly revenue and profit trends
- Revenue distribution across plants and products
- Top-performing customers
- Interactive charts and KPI cards

### 📈 2. Sales, Finance, and Operations Analytics

Dedicated dashboards for different business functions.

**Sales Analytics**
- Customer revenue analysis
- Product performance
- Sales trends and comparisons

**Finance Analytics**
- Revenue and direct cost tracking
- Gross profit analysis
- Profitability monitoring

**Operations Analytics**
- Plant and site performance
- Order quantities
- Operational comparisons

### 🤖 3. Machine Learning Revenue Forecasting

Predictive analytics for estimating future business revenue.

Implemented techniques include:

- Linear Regression for baseline forecasting
- Random Forest Regression
- XGBoost Regression
- Lag-based and rolling-average features
- Historical model evaluation using Mean Absolute Error (MAE)
- Multi-month revenue projections

The advanced forecasting module requires sufficient historical data to train and evaluate models.

*Forecasts are experimental estimates and should not be treated as guaranteed financial predictions.*

### 🔍 4. AI-Based Anomaly Detection

Identifies potentially unusual business transactions using Isolation Forest.

The model analyzes:

- Order quantity
- Product pricing
- Unit costs
- Revenue
- Gross profit

Detected anomalies are displayed through interactive visualizations and transaction-level analysis.

### 💬 5. Business Analytics Copilot

A natural-language interface that allows users to ask common business questions.

Example questions:

- What is my total revenue?
- What is my gross profit margin?
- Show my top five customers.
- Which plant has the highest profit?
- How many orders do I have?

The current implementation uses deterministic, rule-based business analytics on filtered data rather than an external large language model.

### 📁 6. Data Management

- Upload order data through CSV files
- Validate required fields and numeric values
- Remove invalid and duplicate records
- Store transactions in PostgreSQL
- Refresh dashboard data
- Export filtered transactions

### 🔐 7. Multi-Company Authentication and Administration

- Company account registration
- Password hashing using Argon2
- Sign-in and sign-out functionality
- Company-specific data queries
- Role-based access for owners, administrators, and viewers
- User creation and account activation controls
- JWT authentication endpoints in the FastAPI backend

The application implements company-level access controls. Additional security hardening and end-to-end database-level tenant isolation are required before handling sensitive production customer data.

### 📄 8. Automated Business Reports

Generate downloadable PDF business performance reports containing:

- Revenue and cost summaries
- Gross profit and margin
- Order counts
- Top customers
- Automated business insights

PDF reporting is controlled through subscription feature entitlements.

### 💳 9. SaaS Subscription Architecture

OpsPilot AI includes a prototype subscription management system with three plans:

| Plan | Price | Orders | Users |
|---|---|---|---|
| Starter | Free | 1,000 | 2 |
| Growth | ₹1,999/month (proposed) | 25,000 | 10 |
| Enterprise | Custom | Custom | Custom |

The platform includes plan definitions and feature access checks.

**Payment processing and online subscription upgrades are not yet implemented.**

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| Programming Language | Python |
| Dashboard and UI | Streamlit |
| Backend API | FastAPI, Uvicorn |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn, XGBoost |
| Data Visualization | Plotly |
| Authentication | Argon2, JWT |
| Report Generation | ReportLab |
| Testing | Pytest |
| Deployment | Render |
| Version Control | Git, GitHub |

## 🏗️ System Architecture

```text
                  Business Users
                        |
                        v
                Streamlit Dashboard
                        |
          +-------------+-------------+
          |             |             |
          v             v             v
    Authentication  Analytics UI   Data Upload
          |             |             |
          +-------------+-------------+
                        |
                        v
                SQLAlchemy ORM
                        |
                        v
                PostgreSQL Database
                        |
          +-------------+-------------+
          |             |             |
          v             v             v
     Forecasting    Anomaly      Business
       Models       Detection     Insights
          |             |             |
          +-------------+-------------+
                        |
                        v
              Dashboards / Reports

          Separate FastAPI Backend
          JWT Authentication Endpoints
```

## 📂 Project Structure

```text
opspilot-ai/
|
├── app.py
├── requirements.txt
├── generate_data.py
|
├── backend/
│   ├── main.py
│   ├── api/
│   │   └── auth.py
│   └── core/
│       └── jwt_security.py
|
├── pages/
│   ├── admin.py
│   ├── ai_insights.py
│   ├── copilot.py
│   ├── data_hub.py
│   ├── finance.py
│   ├── forecasting.py
│   ├── operations.py
│   ├── reports.py
│   ├── sales.py
│   └── subscription.py
|
├── src/
│   ├── ai/
│   ├── billing/
│   ├── database/
│   ├── reports/
│   ├── security/
│   └── dashboard.py
|
├── scripts/
│   ├── init_db.py
│   ├── import_orders.py
│   └── rls_setup.sql
|
├── data/
│   └── sample_orders.csv
|
├── tests/
├── .streamlit/
└── README.md
```

---

## ⚙️ Installation and Local Setup

### Step 1: Clone the repository

```bash
git clone https://github.com/AMITJ10/opspilot-ai.git
cd opspilot-ai
```

### Step 2: Create a virtual environment

Python 3.12 is recommended for local development.

**Windows PowerShell**

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install dependencies

```bash
python -m pip install -r requirements.txt
```

For the optional FastAPI authentication backend, ensure `PyJWT` and `email-validator` are installed.

### Step 4: Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+psycopg://YOUR_USER:YOUR_PASSWORD@YOUR_HOST:5432/YOUR_DATABASE

JWT_SECRET_KEY=REPLACE_WITH_A_RANDOM_SECRET_OF_AT_LEAST_32_CHARACTERS
```

Replace the placeholders with your PostgreSQL connection details and a securely generated JWT secret.

For local development, PostgreSQL can run through Docker or an existing PostgreSQL installation.

**Never commit `.env`, passwords, or API secrets to GitHub.**

### Step 5: Initialize the database

Ensure PostgreSQL is running and `DATABASE_URL` points to the correct database.

```bash
python -m scripts.init_db
```

This creates the application's SQLAlchemy tables if they do not already exist.

### Step 6: Start the Streamlit application

```bash
python -m streamlit run app.py
```

Open the local URL displayed in your terminal, usually:

http://localhost:8501

### Step 7: Create a company account

1. Open the application.
2. Select **Create Company Account**.
3. Register your company.
4. Sign in.
5. Open the **Data Hub** page.
6. Upload `data/sample_orders.csv`.
7. Explore the analytics dashboards.

### Optional: Start the FastAPI Backend

```bash
python -m uvicorn backend.main:app --reload --port 8000
```

API documentation:

http://127.0.0.1:8000/docs

Available API endpoints include:

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | API information |
| `/health` | GET | Application health |
| `/health/database` | GET | PostgreSQL connectivity |
| `/auth/login` | POST | Authenticate and issue JWT |
| `/auth/me` | GET | Retrieve authenticated user |
| `/auth/check` | GET | Verify authentication |

---

## 🧪 Testing

The repository contains automated tests for API behavior, JWT authentication, and tenant isolation.

Run tests using:

```bash
python -m pytest tests/ -v
```

Some tests require a configured PostgreSQL database and additional environment variables.

The database row-level security test requires a restricted database connection configured through `APP_DATABASE_URL`. It is skipped when this variable is absent.

A successful test run does not replace live security testing or production validation.

## ☁️ Cloud Deployment

OpsPilot AI is configured for deployment using Render.

The Streamlit application can be started with:

```bash
python -m streamlit run app.py --server.address 0.0.0.0 --server.port $PORT --server.headless true
```

This command is intended for a deployment environment where the `PORT` variable is provided.

Production deployment also requires a reachable PostgreSQL database and correctly configured environment variables.

A database running on a developer's laptop cannot be accessed through `localhost` from Render.

## 📸 Application Screenshots

Screenshots of the following modules can be added here:

- Executive Dashboard
- Sales and Finance Analytics
- Machine Learning Forecasting
- Anomaly Detection
- Business Analytics Copilot
- Data Hub
- Subscription Management

## 🚧 Current Limitations and Future Roadmap

OpsPilot AI is an actively developed SaaS prototype.

Planned improvements include:

- Complete production-grade tenant isolation and security testing
- Stronger authentication and session management
- Fully integrated API-driven architecture
- Verified payment processing and subscription lifecycle management
- LLM-powered conversational analytics
- Automated data integrations
- Background jobs and scheduled reports
- Additional forecasting validation and monitoring
- Production observability, database migrations, and CI/CD
- Expanded automated and end-to-end testing

## 💡 Use Cases

OpsPilot AI can be adapted for businesses operating in:

- Construction and infrastructure
- Ready-Mix Concrete (RMC) production
- Manufacturing
- Wholesale and distribution
- Retail operations
- Small and medium enterprises

The platform is intended to demonstrate how data analytics and machine learning can improve operational visibility and business decision-making.

## 👨‍💻 Developer

**Amit Jadhav**

AI/ML Engineer | Python Developer | Data Science & Analytics

**GitHub:** https://github.com/AMITJ10

**Project Repository:** https://github.com/AMITJ10/opspilot-ai

---

### ⭐ Project Vision

To make business intelligence, predictive analytics, and AI-assisted decision-making more accessible to growing businesses through a unified, scalable analytics platform.

**OpsPilot AI — From Business Data to Smarter Decisions.**
