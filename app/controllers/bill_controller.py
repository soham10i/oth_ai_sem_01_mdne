from fastapi import APIRouter, HTTPException, status, Depends, Query
from pydantic import BaseModel
from typing import List, Optional
from app.services.bill_service import BillService
from app.models.bill_info import BillInfo
from sqlalchemy.orm import Session
from app.database.connection import get_db

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
        total_amount = BillService.calculate_total_amount(bill_request.house_id, bill_request.start_date, bill_request.stop_date)
        return {"total_amount": total_amount}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/dump_bill_data")
def dump_bill_data_endpoint(bill_data_request: BillDataRequest):
    try:
        BillService.dump_bill_data(bill_data_request)
        return {"message": "Bill data dumped successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/calculate_and_insert_bills")
async def calculate_and_insert_bills_endpoint(service: BillService = Depends(BillService)):
    try:
        service.calculate_and_insert_bills()
        return {"message": "Bills calculated and inserted successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/bills/{house_id}", response_model=List[BillInfo.BillInfoResponse])
def get_bills_by_house_id(house_id: int, db: Session = Depends(get_db)):
    try:
        bills = db.query(BillInfo).filter(BillInfo.house_id == house_id).all()
        if not bills:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No bills found for the given house ID")
        return bills
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/bills", response_model=List[BillInfo.BillInfoResponse])
def get_bills(house_id: Optional[int] = Query(None), user_id: Optional[int] = Query(None), service: BillService = Depends(BillService)):
    try:
        bills = service.fetch_all_bills(house_id=house_id, user_id=user_id)
        if not bills:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No bills found for the given filters")
        return bills
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/bills/schedule")
async def schedule_monthly_bills(service: BillService = Depends(BillService)):
    try:
        service.start_monthly_scheduler()
        return {"message": "Monthly bill generation scheduler started successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
