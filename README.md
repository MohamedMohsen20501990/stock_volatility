# Stock Volatility Prediction API

A machine learning project that uses **Alpha Vantage** stock data to calculate market volatility, train a prediction model, and deploy it as a **FastAPI REST API**.

## 🚀 Project Pipeline

```text
Alpha Vantage API
       ↓
Historical Stock Data
       ↓
Feature Engineering
       ↓
Volatility Calculation
       ↓
ML Model Training
       ↓
FastAPI
       ↓
Deployment
```

## 📊 Data

The project uses [Alpha Vantage](https://www.alphavantage.co/documentation/) to collect historical OHLCV stock data.

Features include:

* Daily returns
* Rolling volatility
* Moving averages
* Trading volume
* Price ranges

Volatility is calculated from historical returns, for example:

```python
df["return"] = df["close"].pct_change()
df["volatility"] = df["return"].rolling(20).std()
```

## 🤖 Machine Learning

A regression model is trained to predict future stock volatility.

Example:

```python
from sklearn.ensemble import RandomForestRegressor

model = RandomForestRegressor(
    n_estimators=300,
    random_state=42
)

model.fit(X_train, y_train)
```

The trained model is saved using `joblib`.

## ⚡ FastAPI

The model is exposed through a REST API.

### Health Check

```http
GET /health
```

### Prediction

```http
GET /predict/AAPL
```

Example response:

```json
{
  "symbol": "AAPL",
  "predicted_volatility": 0.0245
}
```

API documentation is available at:

```text
/docs
```

## 📁 Project Structure

```text
stock-volatility/
├── app/
│   ├── main.py
│   └── services/
├── data/
├── models/
│   └── volatility_model.pkl
├── training/
│   └── train.py
├── tests/
├── Dockerfile
├── requirements.txt
└── README.md
```

## ▶️ Run Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Set your Alpha Vantage API key:

```env
ALPHA_VANTAGE_API_KEY=your_api_key
```

Start the API:

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://localhost:8000/docs
```

## 🐳 Docker

Build and run:

```bash
docker build -t stock-volatility-api .
docker run -p 8000:8000 --env-file .env stock-volatility-api
```

## ⚠️ Disclaimer

This project is for **educational purposes only**. Volatility predictions are not financial advice or guarantees of future market performance.
