from fastapi import FastAPI

from api import user_credits, plans, plans_performance

app = FastAPI()

app.include_router(user_credits.router, prefix="/user_credits", tags=["User Credits"])
app.include_router(plans.router, prefix="/plans_insert", tags=["Upload New Plan"])
app.include_router(plans_performance.router, prefix="/plans_performance", tags=["Plan Performance"])