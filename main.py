from fastapi import FastAPI, HTTPException

from data import tasks
from models import Tasks, Task, LocationResponse, BulkResponse, BulkRequest
from exception import (
    PinCodeNotFoundError,
pincode_not_found_handler,
invalid_pincode_handler,
InvalidPinCodeError
)
from pincode_repository import get_by_pincode, get_many, get_by_district

app = FastAPI(
    title="Bangladesh Pincode Lookup",
    description="Look up city, district, division and location details for any Bangladesh postal code."
)


# register Custom exception  handler
app.add_exception_handler(PinCodeNotFoundError, pincode_not_found_handler)
app.add_exception_handler(InvalidPinCodeError, invalid_pincode_handler)

@app.get("/")
async def root():
    return {"message": "Welcome to Bangladesh Pincode Lookup"}

@app.get("/pincode/{code}",response_model=LocationResponse)
def lookup_pincode(code:str):
    if len(code) != 4 or not code.isdigit():
        raise InvalidPinCodeError(code,"PinCode must be 4 digits")
    location = get_by_pincode(code)
    if location is None:
        raise PinCodeNotFoundError(code)
    return location
@app.get("/pincode/district/{district}",response_model=list[LocationResponse])
def lookup_pincodes_city(district:str):
    locations = get_by_district(district)
    if not locations:
        raise HTTPException(status_code=404, detail=f"No pincodes found for city: {district}")
    return locations

@app.post("/pincode/bulk",response_model=BulkResponse)
def bulk_lookup(request:BulkRequest):
    results = get_many(request.pincodes)
    found_codes = {loc.pincode for loc in results}
    missing = [code for code in request.pincodes if code not in found_codes]
    return BulkResponse(
        found=len(results),
        not_found=len(missing),
        result=results,
        missing=missing

    )

#
# @app.get("/tasks",response_model=Tasks)
# def get_tasks():
#     return Tasks(count=len(tasks), tasks=tasks)
# @app.get("/tasks/{task_id}",response_model=Task)
# def get_task(task_id: int):
#     for task in tasks:
#         if task.id==task_id:
#             return task
#     raise HTTPException(status_code=404, detail="Task not found")

