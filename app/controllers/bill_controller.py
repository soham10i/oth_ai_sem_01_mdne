from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.services.bill_service import calculate_total_amount, dump_bill_data

router = APIRouter()

class BillRequest(BaseModel):
    house_id: int
    start_date: str
    stop_date: str

class BillDataRequest(BaseModel):
    bill_name: str
    bill_type: str
    total_consumption: float
    amount: float
    house_id: int
    user_id: int
    access_level: str
    due_date: str

@router.post("/calculate_total_amount")
def calculate_total_amount_endpoint(bill_request: BillRequest):
    try:
        total_amount = calculate_total_amount(bill_request.house_id, bill_request.start_date, bill_request.stop_date)
        return {"total_amount": total_amount}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/dump_bill_data")
def dump_bill_data_endpoint(bill_data_request: BillDataRequest):
    try:
        dump_bill_data(bill_data_request)
        return {"message": "Bill data dumped successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
