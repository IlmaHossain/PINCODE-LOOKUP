from fastapi.responses import JSONResponse
from fastapi import Request

class PinCodeNotFoundError(Exception):
    def __init__(self,pin_code:str):
        self.pin_code = pin_code
class InvalidPinCodeError(Exception):
    def __init__(self,pin_code:str,reason:str="Invalid Format"):
        self.pin_code = pin_code
        self.reason = reason

# Custom Handlers
async def pincode_not_found_handler(request: Request,excep:PinCodeNotFoundError):
    return JSONResponse(status_code=404,
                        content={
                            "error":"Pin Code not found",
                            "message":f"No Location for Pin Code: {excep.pin_code}",
                            "pin_code":str(excep.pin_code)

                        }
                    )


async def invalid_pincode_handler(request: Request, excep: InvalidPinCodeError):
    return JSONResponse(status_code=400,
                        content={
                            "error": "Invalid Pin Code",
                            "message": f"PinCode {excep.pin_code} is invalid:{excep.reason}",
                            "pin_code": str(excep.pin_code)

                        }
                 )
