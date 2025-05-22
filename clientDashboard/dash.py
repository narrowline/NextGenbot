from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")  # Relative to dash.py

@app.get("/dashboard")
async def show_dashboard(request: Request):
    try:
        with open("C:/Users/Abdulrehman/Desktop/Rasa project/testing-rasa/orders.json", "r") as f:
            data = json.load(f)
            orders = data.get("value", [])  # Get the orders array from the "value" key
        print("Loaded orders:", orders)  # Debug
    except FileNotFoundError:
        orders = []
        print("No orders.json found, using empty list")
    except json.JSONDecodeError:
        orders = []
        print("Error decoding orders.json, using empty list")
    return templates.TemplateResponse("dash.html", {"request": request, "orders": orders})

@app.get("/orders")
def get_orders():
    try:
        with open("C:/Users/Abdulrehman/Desktop/Rasa project/testing-rasa/orders.json", "r") as f:
            orders = json.load(f)
        return JSONResponse(content=orders)
    except FileNotFoundError:
        return JSONResponse(content=[])
    except json.JSONDecodeError:
        return JSONResponse(content=[])