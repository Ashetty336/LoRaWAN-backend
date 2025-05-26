# user_service.py
from datetime import datetime
import logging
from typing import Optional, Dict, Any,List
from uuid import UUID
from fastapi import HTTPException

from supabase_client import supabase
from models import UserVerify,UserUpdateDetails,UserSignUp,UserResponse

logger = logging.getLogger(__name__)

class UserService:
    @staticmethod
    async def verify_user(user_data: UserVerify) -> Optional[UserResponse]:
        """Verify user, return user if exists, else None."""
        try:
            # Check by Google ID
            response = supabase.table('login-data').select('*').eq('google_id', user_data.google_id).execute()
            if response.data:
                user = response.data[0]
                supabase.table('login-data').update({
                    'last_login': datetime.utcnow().isoformat()
                }).eq('id', user['id']).execute()
                return user

            # Check by email
            response = supabase.table('login-data').select('*').eq('email', user_data.email).execute()
            if response.data:
                user = response.data[0]
                update_data = {'last_login': datetime.utcnow().isoformat()}
                if not user.get('google_id'):
                    update_data['google_id'] = user_data.google_id

                supabase.table('login-data').update(update_data).eq('id', user['id']).execute()

                updated_user = supabase.table('login-data').select('*').eq('id', user['id']).execute().data[0]
                return updated_user

            no_user ={
                "id":UUID("00000000-0000-0000-0000-000000000001"),
                "email":"signup@gmail.com",
                "name":"signup",
                "role":"signup",
                "is_active":False,
                "created_at":datetime.utcnow(),
                "last_login":None,
                "google_id":None
            }
            return no_user

        except Exception as e:
            print("Error verifying user:", e)
            no_user ={
                "id":UUID("00000000-0000-0000-0000-000000000001"),
                "email":"signup@gmail.com",
                "name":"signup",
                "role":"signup",
                "is_active":False,
                "created_at":datetime.utcnow(),
                "last_login":None,
                "google_id":None
            }
            return no_user
        
    async def sign_up(user_data: UserSignUp) -> Dict[str, Any]:
        """Sign up to add new user"""
        try:
            # Check if user exists by email ID
            response =  supabase.table('login-data').select('*').eq('email', user_data.email).execute()
            
            if response.data and len(response.data) > 0:
                user = {
                        "message":"User email already exists!",
                        "success":False    
                        }
                return user
                
            new_user = {
                'email': user_data.email,
                'name': user_data.name if hasattr(user_data, 'name') else user_data.email.split('@')[0],
                'google_id': "pending",
                'role': user_data.role,
                'is_active': False,
                'created_at': datetime.utcnow().isoformat(),
                'last_login': datetime.utcnow().isoformat()
            }
            
            response =  supabase.table('login-data').insert(new_user).execute()
            return {
                        "message":"User created successfully!",
                        "success":True    
                }
            
        except Exception as e:
            logger.error(f"Error verifying user: {e}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    @staticmethod
    async def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
        """Get user by email."""
        try:
            response =  supabase.table('login-data').select('*').eq('email', email).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Error retrieving user by email: {e}")
            raise HTTPException(status_code=500, detail="Database error")
    
        
    @staticmethod
    async def batchUpdate_users(updates: List[UserUpdateDetails]) -> Dict[str, Any]:
        """Update multiple users with individual data."""
        updated_users = []
        try:
            for update_model in updates:
                item = update_model.model_dump(exclude_unset=True)
                user_id = item.pop('id', None)
                if not user_id:
                    continue

                response = supabase.table('login-data').update(item).eq('id', user_id).execute()
                if response.data:
                    updated_users.append(response.data[0])

            if not updated_users:
                raise HTTPException(status_code=404, detail="No users were updated")

            return {"updated_count": len(updated_users), "updated_users": updated_users}

        except Exception as e:
            logger.error(f"Error in batch updating users: {e}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


        
    @staticmethod
    async def get_all_users() ->Dict[str, Any]:
        """Get all users present."""
        try:
            response = supabase.table('login-data') \
                .select('*') \
                .execute()
            return response.data or []
        except Exception as e:
            logger.error(f"Error retrieving user: {e}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        

    @staticmethod
    async def delete_user(user_id: str) -> bool:
        """Delete a particular user."""
        try:
            response = supabase.table('login-data') \
                .delete() \
                .eq('id', user_id) \
                .execute()

            if response.data and len(response.data) > 0:
                return True
            else:
                return False
        except Exception as e:
            logger.error(f"Error deleting user {user_id}: {e}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


