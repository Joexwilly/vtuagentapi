from fastapi import APIRouter

from api.version1 import route_general_pages
from api.version1 import route_users
from api.version1 import route_jobs
from api.version1 import route_auth



api_router = APIRouter()
api_router.include_router(route_general_pages.general_pages_router,prefix="",tags=["general_pages"])
api_router.include_router(route_users.router,prefix="/users",tags=["User Routes"]) 
#api_router.include_router(route_users.router,prefix="/users",tags=["users"])
api_router.include_router(route_jobs.router,prefix="/jobs",tags=["jobs"]) 
api_router.include_router(route_auth.router,prefix="/login",tags=["Authentication"]) 
