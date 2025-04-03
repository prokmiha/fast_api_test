from fastapi import FastAPI, Depends

from api import user_credits, plans, plans_performance, year_performance
from dotenv import load_dotenv
from core.auth import verify_api_key


load_dotenv()

app = FastAPI()

app.include_router(user_credits.router, prefix="/user_credits", tags=["User Credits"], dependencies=[Depends(verify_api_key)])
app.include_router(plans.router, prefix="/plans_insert", tags=["Upload New Plan"], dependencies=[Depends(verify_api_key)])
app.include_router(plans_performance.router, prefix="/plans_performance", tags=["Plan Performance"], dependencies=[Depends(verify_api_key)])
app.include_router(year_performance.router, prefix="/year_performance", tags=["Year Plan Performance"], dependencies=[Depends(verify_api_key)])