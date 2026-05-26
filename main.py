from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="Flight Booker API")

class Flight(BaseModel):
    id: int
    flight_number: str
    destination: str
    departure_time: datetime
    base_price: float
    baggage_included: bool
    available_seats: int

flights = []

@app.get("/")
def home():
    return {"message": "Flight Booker API works"}

@app.get("/flights")
def get_flights():
    return flights

@app.post("/flights", status_code=201)
def create_flight(flight: Flight):
    flights.append(flight)
    return flight

@app.get("/flights/{flight_id}")
def get_flight_by_id(flight_id: int):
    for flight in flights:
        if flight.id == flight_id:
            return flight

    raise HTTPException(status_code=404, detail="Flight not found")

@app.put("/flights/{flight_id}")
def update_flight(flight_id: int, updated_flight: Flight):

    for index, flight in enumerate(flights):

        if flight.id == flight_id:
            flights[index] = updated_flight
            return updated_flight

    raise HTTPException(status_code=404, detail="Flight not found")

@app.delete("/flights/{flight_id}", status_code=204)
def delete_flight(flight_id: int):

    for index, flight in enumerate(flights):

        if flight.id == flight_id:
            flights.pop(index)
            return

    raise HTTPException(status_code=404, detail="Flight not found")

@app.get("/flights/{flight_id}/calculate-ticket")
def calculate_ticket(flight_id: int, class_type: str, extra_baggage: bool = False):

    for flight in flights:
        if flight.id == flight_id:
            final_price = flight.base_price

            if class_type == "business":
                final_price = final_price * 2

            if extra_baggage and not flight.baggage_included:
                final_price = final_price + 15000

            return {
                "flight_id": flight.id,
                "class_type": class_type,
                "extra_baggage": extra_baggage,
                "final_price": final_price
            }

    raise HTTPException(status_code=404, detail="Flight not found")