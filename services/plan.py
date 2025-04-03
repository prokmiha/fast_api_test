from fastapi import UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from io import BytesIO
from collections import defaultdict

import pandas as pd
import datetime

from db.models import Plan
from schemas.plan import PlanPerformanceResponse, PlanPerformanceItemIn, PlanPerformanceItemOut, YearPerformanceItem, YearPerformanceResponse
from repository.user_credit import UserCreditsRepository
from repository.payment import PaymentRepository
from repository.plan import PlanRepository
from repository.dictionary import DictionaryRepository


class PlanService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = PlanRepository(session)
        self.dict_repo = DictionaryRepository(session)

    async def process_new_plan(self, new_file: UploadFile):
        file_data = await new_file.read()

        try:
            df = pd.read_excel(BytesIO(file_data))
        except Exception:
            raise HTTPException(status_code=400, detail="Неможливо прочитати Excel-файл")

        required_columns = {"period", "sum", "name"}
        if not required_columns.issubset(df.columns):
            raise HTTPException(status_code=400, detail=f"Відсутні обов’язкові колонки: {required_columns - set(df.columns)}")

        for i, row in df.iterrows():
            try:
                period = pd.to_datetime(row["period"]).date()
            except Exception:
                raise HTTPException(status_code=400, detail=f"Error: невірна дата")

            if period.day != 1:
                raise HTTPException(status_code=400, detail=f"Error: 'period' має бути першим числом місяця")

            if pd.isna(row["sum"]):
                raise HTTPException(status_code=400, detail=f"Error: поле 'sum' не може бути порожнім")

            category_name = str(row["name"]).strip()
            category_id = self.dict_repo.get_category_id_by_name(category_name)

            if category_id is None:
                raise HTTPException(status_code=400, detail=f"Error: категорія '{category_name}' не знайдена")

            exists = await self.repo.plan_exists(period, category_id)
            if exists:
                raise HTTPException(status_code=400, detail=f"План з категорією '{category_name}' за {period.strftime('%m.%Y')} вже існує")

            plan = Plan(period=period, total_sum=row["sum"], category_id=category_id)
            await self.repo.add_plan(plan)

        await self.session.commit()
        return {"message": "Дані успішно додано до бази"}


class PlanPerformance:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.TYPE_OUT = 3
        self.TYPE_IN = 4
        self.TYPE_PAYMENT_TYPES = (1, 2)

    async def process_plan_performance(self, target_date: datetime.date):
        total_in = await PaymentRepository(self.session).get_monthly_payments(target_date)
        total_out = await UserCreditsRepository(self.session).get_monthly_credits(target_date)
        plans = await PlanRepository(self.session).get_current_plan(target_date)

        plan_in = next((p.total_sum for p in plans if p.category_id == self.TYPE_IN), 0)
        plan_out = next((p.total_sum for p in plans if p.category_id == self.TYPE_OUT), 0)

        if not plan_in and not plan_out:
            raise HTTPException(status_code=400, detail="Не задано план на даний період")

        completion_in = round((total_in / plan_in) * 100, 2) if plan_in else 0
        completion_out = round((total_out / plan_out) * 100, 2) if plan_out else 0

        dict_repo = DictionaryRepository(self.session)
        in_name = await dict_repo.get_category_name_by_id(self.TYPE_IN)
        out_name = await dict_repo.get_category_name_by_id(self.TYPE_OUT)

        return PlanPerformanceResponse(
            performance_in=[
                PlanPerformanceItemIn(
                    month=target_date.strftime("%m.%Y"),
                    category=in_name,
                    plan_sum=plan_in,
                    fact_sum=total_in,
                    completion=f"{completion_in}%"
                )
            ],
            performance_out=[
                PlanPerformanceItemOut(
                    month=target_date.strftime("%m.%Y"),
                    category=out_name,
                    plan_sum=plan_out,
                    fact_sum=total_out,
                    completion=f"{completion_out}%"
                )
            ]
        )

    def validate_date(self, date_str: str):
        return datetime.datetime.strptime(date_str, "%d.%m.%Y").date()


class YearPerformance:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.TYPE_OUT = 3
        self.TYPE_IN = 4
        self.TYPE_PAYMENT_TYPES = (1, 2)

    async def process_year_performance(self, target_date: int):
        payments = await PaymentRepository(self.session).get_yearly_payments(target_date)
        credits = await UserCreditsRepository(self.session).get_yearly_credits(target_date)
        plans = await PlanRepository(self.session).get_yearly_plans(target_date)

        payment_data = defaultdict(lambda: {"count": 0, "sum": 0})
        credit_data = defaultdict(lambda: {"count": 0, "sum": 0})
        plan_credit = defaultdict(float)
        plan_payment = defaultdict(float)

        for month, count, total, type_id in payments:
            if type_id in self.TYPE_PAYMENT_TYPES:
                payment_data[month]["count"] += count
                payment_data[month]["sum"] += total

        for month, count, total in credits:
            credit_data[month]["count"] = count
            credit_data[month]["sum"] = total

        for month, total, category_id in plans:
            if category_id == self.TYPE_OUT:
                plan_credit[month] = total
            elif category_id == self.TYPE_IN:
                plan_payment[month] = total

        total_year_credit = sum(v["sum"] for v in credit_data.values())
        total_year_payment = sum(v["sum"] for v in payment_data.values())

        result = []
        for month in range(1, 13):
            credit_sum = credit_data[month]["sum"]
            payment_sum = payment_data[month]["sum"]
            credit_count = credit_data[month]["count"]
            payment_count = payment_data[month]["count"]

            credit_plan = plan_credit.get(month, 0)
            payment_plan = plan_payment.get(month, 0)

            result.append(YearPerformanceItem(
                month=f"{month:02d}.{target_date}",
                credit_count=credit_count,
                credit_plan_sum=credit_plan,
                credit_sum=credit_sum,
                credit_completion=round((credit_sum / credit_plan * 100), 2) if credit_plan else 0,
                payment_count=payment_count,
                payment_plan_sum=payment_plan,
                payment_sum=payment_sum,
                payment_completion=round((payment_sum / payment_plan * 100), 2) if payment_plan else 0,
                credit_year_percent=round((credit_sum / total_year_credit * 100), 2) if total_year_credit else 0,
                payment_year_percent=round((payment_sum / total_year_payment * 100), 2) if total_year_payment else 0
            ))

        return YearPerformanceResponse(performance=result)


    def validate_year(self, year_str: str) -> int:
        year = int(year_str)
        if not (1900 <= year <= 2100):
            raise ValueError("Некоректний рік")
        return year
