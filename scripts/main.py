from dotenv import load_dotenv
from models.core import add_forecast_data
from scripts.api_script import fetch_data

load_dotenv()

if __name__ == "__main__":
    data = fetch_data()
    add_forecast_data(data)
