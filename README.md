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
 

## ⚡ FastAPI

The model is exposed through a REST API.

### Health Check

```http
GET /health
```

### Prediction

```http
GET /predict/AMBUJACEM

```

Example response:

```json
{
  "symbol": "AMBUJACEM",
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
├── notebooks/
│   ├── main.ipunb
├── data/
├── models/
│   └── volatility_model.pkl
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
