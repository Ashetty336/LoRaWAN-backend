# user_routes.py
from fastapi import APIRouter, HTTPException
from typing import Dict, Any,List

from models import UserVerify,UserResponse,UserDetails,UserUpdateDetails,UserSignUp
from login_service import UserService

router = APIRouter(prefix="/login", tags=["Login"])

@router.post("/verify", response_model=UserResponse)
async def verify_user(user_data: UserVerify):
    """Verify a user after Google authentication in frontend."""
    try:
        user = await UserService.verify_user(user_data)
        return UserResponse(**user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/signUp")
async def signUp_user(user_data: UserSignUp):
    """Sign up to create a new user."""
    try:
        user = await UserService.sign_up(user_data)
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/data", response_model=List[UserDetails])
async def get_users():
    """Get all users"""
    response = await UserService.get_all_users()
    return response


@router.put("/batchUpdate", response_model=Dict[str, Any])
async def batch_update_users(updates: List[UserUpdateDetails]):
    """
    Batch update multiple users with different data.
    Each item must include an 'id' and the fields to update.
    """
    
    updated_result = await UserService.batchUpdate_users(updates)
    return updated_result


@router.delete("/delete/{user_id}")
async def delete_user(user_id: str):
    """Delete user details."""
    success= await UserService.delete_user(user_id)
    return success

@router.get("/checkEmail/{email}", response_model=UserResponse)
async def get_user(email: str):
    """Get user by email."""
    user = await UserService.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(**user)




    