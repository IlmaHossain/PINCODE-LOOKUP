from pydantic import BaseModel,field_validator
class PinCodeRequest(BaseModel):
    pincode: str
    @field_validator("pincode")
    @classmethod
    def validate_pincode(cls, value):
        if len(value) != 4 or not value.isdigit():
            raise ValueError("Pincode must be 4 digits")
        return value
class LocationResponse(BaseModel):
    pincode: str
    city: str
    state: str
    district: str
    upazila: str | None = None
    latitude: float | None = None
    longitude: float | None = None
class BulkRequest(BaseModel):
    pincodes: list[str]
    @field_validator("pincodes")
    @classmethod
    def validate_pincodes(cls, values):
        if len(values) == 0:
            raise ValueError("At least one Pincode must be provided")
        if len(values) > 20:
            raise ValueError("Maximum of 20 pincodes allowed per request")
        for pincode in values:
            if len(pincode) != 4 or not pincode.isdigit():
                raise ValueError("Each Pincode must be 4 digits")
        return values
class BulkResponse(BaseModel):
    status: str="success"
    found: int
    not_found: int
    result: list[LocationResponse]
    missing:list[str]





class Task(BaseModel):
    id: int
    task_name: str
    task_description: str


class Tasks(BaseModel):
    status: str="success"
    count: int
    tasks: list[Task]
