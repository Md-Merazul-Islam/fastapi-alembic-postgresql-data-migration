from fastapi import  BackgroundTasks, HTTPException,APIRouter
from pydantic import BaseModel, EmailStr
from .services.email_services import send_otp_email
from .services.otp_service import generate_otp, check_otp



router = APIRouter(prefix="/email", tags=["auth"])


class OTPRequest(BaseModel):
    email: EmailStr


class OTPVerifyRequest(BaseModel):
    email: EmailStr
    otp: str

@router.post("/send-otp")
def send_otp(request:OTPRequest, background_tasks: BackgroundTasks):
    otp_code = generate_otp(request.email)
    background_tasks.add_task(send_otp_email, request.email, otp_code)
    return {"message": "OTP sent successfully"}
  

@router.post("/verify-otp")
def verify_otp(request:OTPVerifyRequest):
    if check_otp(request.email, request.otp):
      return {"message": "OTP verified successfully"}
    raise HTTPException(status_code=400, detail="Invalid OTP")