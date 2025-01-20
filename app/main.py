import sys
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from app.routes import auth_routes, house_routes, residents_routes, mail_routes, \
        sensor_routes, user_routes, bill_routes, sensor_data_routes, calendar_routes
from app.controllers import calendar_event_controller, calendar_event_share_controller
from app.database.connection import create_tables

app = FastAPI(title="Smart Home Project API", version="0.1.0")

@app.on_event("startup")
def on_startup():
    """
    Event handler for the startup event.
    Creates the necessary database tables.
    """
    try:
        create_tables()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during startup: {str(e)}")

# Include your routers
app.include_router(auth_routes, prefix="/auth")
app.include_router(house_routes, prefix="/houses")
app.include_router(residents_routes, prefix="/residents")
app.include_router(mail_routes, prefix="/mail")
app.include_router(sensor_routes.router, prefix="/sensor")
app.include_router(sensor_data_routes.router, prefix="/sensor_data")
app.include_router(bill_routes.router, prefix="/bill")
app.include_router(user_routes.router, prefix="/users")
app.include_router(calendar_routes, prefix="/calendar")
app.include_router(calendar_event_controller.router, prefix="/calender_event", tags=["calendar_event"])
app.include_router(calendar_event_share_controller.router, prefix="/calender_event_share", tags=["calendar_event_share"])

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler to catch unhandled exceptions.
    """
    return JSONResponse(
        status_code=500,
        content={"message": f"An unexpected error occurred: {str(exc)}"}
    )

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
