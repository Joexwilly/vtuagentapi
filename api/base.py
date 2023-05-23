from fastapi import APIRouter

from api.version1 import route_general_pages
from api.version1 import route_page_discounts
from api.version1 import route_users
from api.version1 import route_jobs
from api.version1 import route_auth
from api.version1 import route_transactions
from api.version1 import route_wallet



api_router = APIRouter()
api_router.include_router(route_general_pages.general_pages_router,prefix="",tags=["general_pages"])
api_router.include_router(route_page_discounts.router,prefix="/page-discounts",tags=["Page Discounts"])
api_router.include_router(route_users.router,prefix="/users",tags=["User Routes section"]) 
#api_router.include_router(route_users.router,prefix="/users",tags=["users"])
api_router.include_router(route_jobs.router,prefix="/jobs",tags=["jobs"]) 
api_router.include_router(route_auth.router,prefix="/login",tags=["Authentication"]) 
api_router.include_router(route_transactions.router,prefix="/transactions",tags=["Transactions"])
api_router.include_router(route_wallet.router,prefix="/wallet",tags=["Wallet"])
