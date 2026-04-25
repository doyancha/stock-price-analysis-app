# Stock Price Analysis App

Streamlit dashboard for multi-stock price analysis, built for Heroku deployment.

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy To Heroku From GitHub

1. Create a Heroku app.
2. In the Heroku dashboard, open the app's Deploy tab.
3. Choose GitHub as the deployment method.
4. Connect this repository and select the `main` branch.
5. Click Deploy Branch, or enable automatic deploys.

Heroku uses the included `Procfile`:

```text
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

The app includes a compact `data/stock_prices.csv` file, so it does not require the old
`individual_stocks_5yr/` folder during deployment.
