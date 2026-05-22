# 🛒 E-Commerce Intelligence Platform

> A full-stack data analytics project solving 10 real-world e-commerce problems using Python, Machine Learning, and interactive dashboards.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://e-commerce-intelligence-platform-avv.streamlit.app)

🔗 **Live Dashboard** → [https://e-commerce-intelligence-platform-avv.streamlit.app](https://e-commerce-intelligence-platform-avv.streamlit.app)

📁 **GitHub** → [https://github.com/ankamvinayv/E-Commerce-Intelligence-Platform](https://github.com/ankamvinayv/E-Commerce-Intelligence-Platform)

---

## 📌 Project Overview

This project was built to solve **10 critical problems** faced by e-commerce startups — spanning supply chain gaps, pricing barriers, and customer trust issues. Each problem is tackled with real data analysis and machine learning models.

| Pillar | Problems Solved |
|--------|----------------|
| 🎯 Customer Experience | Visual mismatch returns · Counterfeit products · Packaging waste · After-hours returns |
| 🚚 Supply Chain | Stockout prediction · Perishable quality · Rural delivery gaps |
| 💰 Pricing & Access | Hidden fee impact · Bulk discount engine · Wholesale pricing opportunity |

---

## 🚀 Live Dashboard

The dashboard is deployed on Streamlit Cloud with **3 interactive tabs**:

- **📦 Operations Tab** — XGBoost stockout risk scores with live category filters, delivery success rate by rural vs urban zone, perishable quality complaint analysis by transit time
- **💰 Pricing Tab** — Hidden fee cart abandonment impact, price elasticity by product category, interactive bulk discount revenue simulator with live sliders
- **🔍 Seller Trust Tab** — Isolation Forest anomaly detection scatter plot, seller risk tier breakdown, flagged seller table with CSV download

---

## 🤖 Machine Learning Models

### Model 1 — Stockout Predictor (XGBoost Classifier)
- **Problem Solved:** Products going out of stock without warning (P5)
- **Algorithm:** XGBoost Binary Classifier
- **Features:** Stock level, reorder point, stock-to-reorder ratio, rolling 7-day average stock, category, month, day of week, quarter, is_perishable, price
- **Target:** Binary stockout event (0 = no stockout, 1 = stockout)
- **Handling Imbalance:** scale_pos_weight to handle rare stockout events
- **Output:** Stockout risk score (0–1) per product — High / Medium / Low risk labels
- **Evaluation Metric:** ROC-AUC score

### Model 2 — Price Elasticity & Discount Engine (Linear Regression)
- **Problem Solved:** No data-driven bulk discount strategy (P9, P10)
- **Algorithm:** Linear Regression on log-transformed price and quantity
- **Features:** Log price, discount percentage, hidden fee flag, household size, category, order month
- **Output:** Elasticity coefficient per category + interactive revenue impact simulation
- **Key Insight:** Categories with negative elasticity below -0.5 are strongest bulk discount candidates

### Model 3 — Seller Authenticity Anomaly Scorer (Isolation Forest)
- **Problem Solved:** Counterfeit products from suspicious sellers (P2)
- **Algorithm:** Isolation Forest (Unsupervised Anomaly Detection)
- **Why Unsupervised:** No labelled fraud data available — model finds outliers automatically
- **Features:** Fake product rate, complaint rate per product, counterfeit complaint count, price volatility
- **Output:** Anomaly score per seller + risk tier (Low / Medium / High Risk)
- **Key Advantage:** No human labelling needed — detects fraud patterns automatically

---

## 📊 Key Findings from EDA

| Problem | Finding |
|---------|---------|
| P8 — Hidden fees | Cart abandonment is measurably higher when a hidden fee is revealed at checkout vs upfront pricing |
| P7 — Rural delivery | Rural delivery success rate is significantly lower than urban — last-mile gap confirmed |
| P6 — Perishables | Quality complaint rate spikes sharply for perishable items with transit time over 48 hours |
| P4 — Return timing | A large percentage of all return attempts happen outside standard business hours (before 9am / after 6pm) |
| P3 — Packaging | A significant share of products are shipped in boxes larger than actually needed |
| P5 — Stockouts | Grocery and Fashion categories show the highest stockout rates across the year |

---

## 🗂 Project Structure

```
ecommerce-analytics/
├── requirements.txt               # Python dependencies for Streamlit Cloud
├── README.md                      # This file
│
├── data/
│   ├── raw/                       # 6 synthetic CSV datasets
│   │   ├── customers.csv          # 5,000 customer records
│   │   ├── products.csv           # 500 product listings
│   │   ├── orders.csv             # 10,000 orders
│   │   ├── returns.csv            # 900 return records
│   │   ├── deliveries.csv         # 10,000 delivery records
│   │   └── inventory.csv          # 3,650 daily stock snapshots
│   └── processed/                 # EDA charts, model outputs, risk scores
│
├── notebooks/
│   ├── 01_data_generation.ipynb   # Synthetic dataset generation
│   ├── 02_eda.ipynb               # Exploratory data analysis (11 charts)
│   ├── 03_model_stockout.ipynb    # XGBoost stockout prediction
│   ├── 04_model_pricing.ipynb     # Price elasticity model
│   └── 05_model_authenticity.ipynb # Isolation Forest seller anomaly detection
│
├── models/                        # Saved .pkl model files
│   ├── stockout_model.pkl
│   ├── category_encoder.pkl
│   ├── pricing_model.pkl
│   ├── anomaly_model.pkl
│   └── anomaly_scaler.pkl
│
└── dashboard/                     # Streamlit app
    ├── app.py                     # Main dashboard (3 tabs)
    ├── orders.csv
    ├── products.csv
    ├── customers.csv
    ├── returns.csv
    ├── deliveries.csv
    ├── stockout_risk_scores.csv
    ├── seller_risk_scores.csv
    └── category_elasticity.csv
```

---

## 🛠 Tech Stack

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.10 | Core language |
| Pandas | Latest | Data wrangling and analysis |
| NumPy | Latest | Numerical computation |
| Matplotlib & Seaborn | Latest | EDA charts and visualisations |
| Scikit-learn | Latest | ML models and preprocessing |
| XGBoost | Latest | Stockout prediction classifier |
| Plotly | Latest | Interactive dashboard charts |
| Streamlit | Latest | Dashboard deployment |
| Faker (en_IN) | Latest | Synthetic Indian e-commerce data |
| Joblib | Latest | Model serialisation |
| Git & GitHub | — | Version control and portfolio |

---

## 📁 Dataset Details

Fully synthetic dataset generated using Python's Faker library with Indian locale (`en_IN`), designed to simulate a realistic Indian e-commerce platform with intentional patterns that reflect the 10 problems being solved.

| Dataset | Records | Key Columns |
|---------|---------|-------------|
| customers.csv | 5,000 | customer_id, city, pincode, household_size, profession, is_rural |
| products.csv | 500 | product_id, category, price, is_perishable, box_size_used, actual_size_needed, is_authentic |
| orders.csv | 10,000 | order_id, base_price, hidden_fee, discount_applied, cart_abandoned, order_hour |
| returns.csv | 900 | return_id, reason, return_attempt_hour, pickup_available |
| deliveries.csv | 10,000 | delivery_id, transit_hours, delivery_success, quality_complaint, is_rural |
| inventory.csv | 3,650 | snapshot_date, product_id, stock_level, stockout_event |

---

## 🏃 How to Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/ankamvinayv/E-Commerce-Intelligence-Platform.git
cd E-Commerce-Intelligence-Platform

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate the dataset (run once)
cd notebooks
jupyter notebook 01_data_generation.ipynb

# 4. Run the dashboard
cd ../dashboard
streamlit run app.py
```

---

## 💡 10 Problems Solved

| ID | Problem | Approach |
|----|---------|---------|
| P1 | Fashion products look different in reality | Return reason analysis — colour mismatch and visual mismatch returns quantified |
| P2 | Beauty buyers can't verify authenticity | Isolation Forest anomaly detection on seller behaviour |
| P3 | Small orders arrive in oversized packaging | Box size vs actual size needed — over-packaging rate per category |
| P4 | Can't return products outside business hours | Return attempt hour analysis — after-hours % quantified |
| P5 | Items unavailable when shoppers arrive | XGBoost stockout prediction model with risk scoring |
| P6 | Quick delivery sends bruised produce | Quality complaint rate vs transit time — perishable threshold identified |
| P7 | Rural residents can't get doorstep delivery | Delivery success rate by pincode rural/urban classification |
| P8 | Hidden fees inflate prices | Cart abandonment rate comparison — fee vs no-fee orders |
| P9 | No bulk discount or negotiation online | Price elasticity modelling per category + discount simulator |
| P10 | Large families can't access wholesale pricing | Household size vs average order value segmentation |

---

## 👤 Author

**Ankam Vinay Vardhan**
- GitHub: [@ankamvinayv](https://github.com/ankamvinayv)
- Live Dashboard: [E-Commerce Intelligence Platform](https://e-commerce-intelligence-platform-avv.streamlit.app)

---
