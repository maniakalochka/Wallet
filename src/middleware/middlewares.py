from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from database.db import get_db


class DBSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Создание сессии
        db_generator = get_db()
        request.state.db = await anext(db_generator)  # Получение сессии
        try:
            response = await call_next(request)
        except Exception as e:
            await request.state.db.rollback()  # Откат транзакции при ошибке
            raise e
        finally:
            await request.state.db.close()  # Закрытие сессии
            await db_generator.aclose()  # Закрытие генератора
        return response
