
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

XAG_API_URL = "https://api.gold-api.com/price/XAG"
EXCHANGE_API_URL = "https://open.er-api.com/v6/latest/USD"

@app.get("/silver")
def get_silver_prices():
    try:
        silver_res = requests.get(XAG_API_URL, timeout=10)
        silver_res.raise_for_status()
        silver_data = silver_res.json()
        if "price" not in silver_data:
            return {"error": "Silver price not found in response."}
        xag_price_usd_oz = float(silver_data["price"])

        fx_res = requests.get(EXCHANGE_API_URL, timeout=10)
        fx_res.raise_for_status()
        fx_data = fx_res.json()
        usd_to_myr = fx_data["rates"].get("MYR")
        if not usd_to_myr:
            return {"error": "MYR exchange rate not found."}

        # Corrected logic: price per gram = price per oz / 31.1035
        # Then convert to MYR, multiply by 1000 to get price per kg
        price_per_gram_usd = xag_price_usd_oz / 31.1035
        base_price = price_per_gram_usd * usd_to_myr * 1000  # MYR/kg

        we_buy = round(base_price * 0.75, 2)
        we_sell = round(base_price * 1.15, 2)
        we_buy_100g = round(base_price * 0.75 * 100 / 1000, 2)
        we_sell_100g = round(base_price * 1.35 * 100 / 1000, 2)

return {
    "spot_price": round(base_price, 2),
    "currency": "MYR",
    "purity": "999",
    "we_buy": we_buy,
    "we_sell": we_sell,
    "we_buy_100g": we_buy_100g,
    "we_sell_100g": we_sell_100g,
}


    except Exception as e:
        return {"error": f"Failed to retrieve silver price: {str(e)}"}
