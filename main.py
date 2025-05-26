from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
import time as otp_time
import os
import asyncio

from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
import uuid
from time import time
from dataclasses import dataclass
import logging
import json
import ssl
from fastapi import Request, HTTPException
from starlette.responses import JSONResponse
from login_routes import router as login_router
import random
from email.mime.text import MIMEText
import smtplib
from apscheduler.schedulers.background import BackgroundScheduler
load_dotenv()


EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Session header for API key
X_SESSION_ID = APIKeyHeader(name="X-Session-ID", auto_error=False)

otp_store = {}
# Background scheduler to clean expired OTPs every minute
scheduler = BackgroundScheduler()
def clean_expired_otps():
    current_time = otp_time.time()
    expired_emails = [email for email, data in otp_store.items() if current_time - data["timestamp"] > 120]
    for email in expired_emails:
        del otp_store[email]

scheduler.add_job(clean_expired_otps, "interval", minutes=60*2)
scheduler.start()


@dataclass
class SessionInfo:
    """Store session information including service and last access time."""
    last_accessed: float





# Session dependency with proper async handling
async def get_session_id(session_id: str = Depends(X_SESSION_ID)) -> str:
    """Get or create a session ID for the request."""
    if not session_id:
        session_id = str(uuid.uuid4())
    return session_id



# Create the FastAPI application
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://report-generator-six-eta.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Authentication route

app.include_router(login_router)

#Checks
@app.get("/")
async def root():
    """Root endpoint to check if the API is running."""
    return {"message": "Report-gen backend is running!"}



@app.get("/healthcheck")
async def healthcheck():
    """Health check endpoint."""
    return {"status": "ok", "timestamp": datetime.now().isoformat()}
    

def generate_otp(length=6):
    return ''.join(random.choices("0123456789", k=length))


@app.post("/send-otp/{email}")
async def send_otp(email:str):
    otp = generate_otp()
    otp_store[email] = {"otp": otp, "timestamp": otp_time.time()}
    msg = MIMEText(f"Your OTP code is: {otp}")
    msg["Subject"] = "Sign up OTP Code"
    msg["From"] = EMAIL_USERNAME
    msg["To"] = email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        server.sendmail(EMAIL_USERNAME, email, msg.as_string())

    return {"message": "OTP sent","success":True}


@app.post("/verify-otp/{email}/{otp}")
async def verify_otp(email:str,otp:str):
    record = otp_store.get(email)

    if not record:
        return {"message": "OTP verification failed!","success":False}

    if otp_time.time() - record["timestamp"] > 60*5:
        del otp_store[email]
        return {"message": "OTP expired!","success":False}

    if otp != record["otp"]:
        return {"message": "Invalid OTP!","success":False}

    del otp_store[email]
    return {"message": "OTP verified","success":True}




# Middleware processing

@app.middleware("http")
async def timeout_middleware(request, call_next):
    """First middleware to handle timeouts."""
    try:
        return await asyncio.wait_for(call_next(request), timeout=20.0)
    except asyncio.TimeoutError:
        logger.error(f"Request timed out: {request.url.path}")
        return JSONResponse(
            status_code=504,
            content={"detail": "Request timed out"},
        )
    except asyncio.CancelledError:
        logger.debug(f"Request to {request.url.path} was cancelled")
        return JSONResponse(
            status_code=499,
            content={"detail": "Request cancelled"}
        )
    except Exception as e:
        logger.exception(f"Error in timeout middleware: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error during request processing"},
        )


@app.middleware("http")
async def session_middleware(request, call_next):
    """Middleware for session management with timing metrics."""
    start_time = time()
    
    try:
        response = await call_next(request)
        if response is None:
            logger.error("No response returned from downstream middleware or route handler")
            return JSONResponse(
                {"detail": "No response returned from server"},
                status_code=500
            )
        
        # Add timing information
        process_time = time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response
        
    except ssl.SSLError as e:
        logger.error(f"SSL Error in session middleware: {str(e)}")
        return JSONResponse(
            {"detail": "SSL connection error. Ensure proper protocol (HTTP/HTTPS) is used"},
            status_code=400
        )
    except Exception as e:
        logger.error(f"Unhandled exception in session middleware: {str(e)}")
        return JSONResponse(
            {"detail": "Internal server error"},
            status_code=500
        )


@app.exception_handler(ssl.SSLError)
async def ssl_error_handler(request: Request, exc: ssl.SSLError):
    """Global exception handler for SSL errors."""
    logger.error(f"SSL Error: {str(exc)}")
    return JSONResponse(
        status_code=400,
        content={"detail": "SSL connection error. Check if HTTP/HTTPS protocols match"}
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for all unhandled exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again later."}
    )
