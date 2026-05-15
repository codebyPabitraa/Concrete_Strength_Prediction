# 🧱 Concrete Strength Predictor

> *Predicting compressive strength through intelligent material analysis — faster, smarter, safer.*

[![Live App](https://img.shields.io/badge/🚀%20Live%20Demo-Streamlit-FF4B4B?style=for-the-badge)](https://concretestrengthprediction-hkmfyykf8rynjdiekpyrbg.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)]()
[![XGBoost](https://img.shields.io/badge/Best%20Model-XGBoost%2091%25-189AB4?style=for-the-badge)]()

---

## 🔍 What Is This?

Concrete compressive strength determines the **safety and durability** of every structure it's used in. Traditional lab testing is time-consuming and costly.

This project uses **Machine Learning** to predict **Concrete Compressive Strength (MPa)** from mix composition — delivering fast, accurate results without the wait.

---

## 🎯 Objectives

- Predict compressive strength from material properties
- Compare multiple ML regression models
- Identify key influencing factors
- Achieve high prediction accuracy (target: >90%)

---

## 📐 Project Pipeline

```
Raw Data → EDA → Preprocessing → Model Training → Evaluation → Deployment
```

> See full flowchart below ↓

---

## 📂 Dataset Features

| Feature | Unit | Role |
|---|---|---|
| Cement | kg/m³ | Input |
| Blast Furnace Slag | kg/m³ | Input |
| Fly Ash | kg/m³ | Input |
| Water | kg/m³ | Input |
| Superplasticizer | kg/m³ | Input |
| Coarse Aggregate | kg/m³ | Input |
| Fine Aggregate | kg/m³ | Input |
| Age | days | Input |
| **Compressive Strength** | **MPa** | **Target** ✅ |

---

## 🔬 Exploratory Data Analysis

- Analyzed feature distributions and skewness
- Computed Pearson correlation matrix
- Visualized relationships using scatter plots & heatmaps
- Detected and handled outliers
- Confirmed zero missing values

---

## ⚙️ Data Preprocessing

| Step | Detail |
|---|---|
| Train-Test Split | 80% / 20% |
| Feature Scaling | StandardScaler |
| Data Type | All numerical |
| Outlier Handling | Applied where necessary |

---

## 🤖 ML Models Used

| # | Model | R² Accuracy |
|---|---|---|
| 1 | Linear Regression | 82% |
| 2 | Decision Tree | 86% |
| 3 | Support Vector Regressor | 88% |
| 4 | Random Forest | 90% |
| 5 | **XGBoost** ⭐ | **91%** |

### 🏆 Best Model: XGBoost Regressor (~91% R²)

---

## 📈 Key Insights

- 🧱 **Cement** is the strongest predictor of compressive strength
- ⏳ **Age** has a significant positive correlation — longer curing = stronger concrete
- 💧 **Excess water** reduces strength (high w/c ratio weakens structure)
- ⚖️ A balanced mix design consistently improves performance

---

## 📊 Evaluation Metrics

- **R² Score** — Variance explained by the model
- **RMSE** — Root Mean Squared Error
- **MAE** — Mean Absolute Error

---

## 🧰 Tech Stack

**Language:** Python 3.9+

**Libraries:**
```
numpy · pandas · matplotlib · seaborn · scikit-learn · xgboost
```

**Environment:**
```
Jupyter Notebook · Kaggle · Streamlit
```

---

## 📁 Project Structure

```
Concrete_Strength_Prediction/
│
├── 📁 data/
│   └── concrete_data.csv
│
├── 📁 notebooks/
│   └── analysis.ipynb
│
├── 📁 models/
│   └── xgboost_model.pkl
│
├── app.py              ← Streamlit web app
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/your-username/Concrete_Strength_Prediction

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
```

---

## 🌐 Live Demo

🔗 **[Open App →](https://concretestrengthprediction-hkmfyykf8rynjdiekpyrbg.streamlit.app/)**

Input your concrete mix parameters and get an **instant strength prediction**.

---

## 📌 Flowchart

```
[Raw Dataset]
      ↓
[Exploratory Data Analysis]
  - Distributions
  - Correlations
  - Outliers
      ↓
[Data Preprocessing]
  - Train/Test Split (80/20)
  - StandardScaler
      ↓
[Model Training]
  ┌─────────────────────────────────────┐
  │ Linear Regression → Decision Tree  │
  │ SVR → Random Forest → XGBoost      │
  └─────────────────────────────────────┘
      ↓
[Model Evaluation]
  - R², RMSE, MAE
      ↓
[Best Model: XGBoost (91%)]
      ↓
[Streamlit Deployment]
```

---

## 👤 Author

**Pabitra Chakraborty**
Mechanical Engineering | Jadavpur University | 2023–2027

---

> *"Concrete is the skeleton of civilization — let's make it smarter."*
