import sys
import uvicorn
from fastapi import FastAPI
from app.routes import auth_routes, house_routes, residents_routes, mail_routes, sensor_routes
from app.routes.sensor_data_routes import router as sensor_data_router
from app.routes.bill_routes import router as bill_router
from app.database.connection import create_tables

app = FastAPI(title="Smart Home Project API", version="0.1.0")

@app.on_event("startup")
def on_startup():
    create_tables()

# Include your routers
app.include_router(auth_routes.router, prefix="/auth")
app.include_router(house_routes.router, prefix="/houses")
app.include_router(residents_routes.router, prefix="/residents")
app.include_router(mail_routes.router, prefix="/mail")
app.include_router(sensor_routes.router, prefix="/sensor")
app.include_router(sensor_data_router, prefix="/sensor_data")
app.include_router(bill_router, prefix="/bill")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
