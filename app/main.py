from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
import logging
from app import models
from app.database import engine, get_db, init_db
from app.models import Order

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# --- Pydantic Схема для вхідних даних ---
class OrderCreate(BaseModel):
    client_name: str
    client_phone: str
    product_name: str
    product_size: str
    quantity: int
    total_price: float

    class Config:
        # Дозволяє використання об'єктів Decimal (якщо б ми їх отримували, тут використовуємо float)
        from_attributes = True


# Ініціалізація FastAPI застосунку
app = FastAPI(
    title="KripMarket Fast API Service",
    description="Backend service for KripMarket product catalog.",
)


# --- АСИНХРОННА ІНІЦІАЛІЗАЦІЯ ТАБЛИЦЬ БД ---
@app.on_event("startup")
async def startup_event():
    try:
        await init_db()
        logger.info("Таблиці бази даних MySQL успішно перевірені/створені (Асинхронно).")
    except Exception as e:
        logger.error(f"ПОМИЛКА: Не вдалося підключитися або створити таблиці MySQL. Помилка: {e}")


# --- НАЛАШТУВАННЯ ШЛЯХІВ ---
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

if not TEMPLATES_DIR.is_dir():
    logger.error(f"Каталог шаблонів не знайдено: {TEMPLATES_DIR}")
if not STATIC_DIR.is_dir():
    STATIC_DIR.mkdir(exist_ok=True)

# Налаштування Jinja2 Templates
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Налаштування StaticFiles
app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static"
)




@app.get("/")
async def serve_index(request: Request, db: AsyncSession = Depends(get_db)):
    """Головна сторінка."""

    try:
        await db.execute(select(models.Product).limit(1))
        db_status = "Успішно підключено до MySQL (Асинхронно)"
    except Exception as e:
        db_status = f"Помилка підключення до БД: {e}"
        logger.warning(db_status)

    context = {"request": request, "title": "Головна сторінка КріпМаркет", "db_status": db_status}
    return templates.TemplateResponse("index.html", context)


@app.post("/api/orders/")
async def create_order(order_data: OrderCreate, db: AsyncSession = Depends(get_db)):
    """Приймає замовлення та зберігає його у таблицю `orders` MySQL."""
    # ДОДАНО ЛОГУВАННЯ ВХІДНИХ ДАНИХ
    logger.info(f"Отримано замовлення: {order_data.model_dump_json()}")
    try:
        new_order = Order(
            client_name=order_data.client_name,
            client_phone=order_data.client_phone,
            product_name=order_data.product_name,
            product_size=order_data.product_size,
            quantity=order_data.quantity,
            total_price=order_data.total_price,
        )

        db.add(new_order)
        await db.commit()

        # Для коректного логування
        await db.refresh(new_order)
        logger.info(f"Успішно збережено замовлення #{new_order.id} для {new_order.client_name}")

        return {"status": "success", "order_id": new_order.id, "message": "Замовлення успішно збережено"}

    except Exception as e:
        logger.error(f"Помилка при збереженні замовлення в БД: {e}")
        # Повертаємо помилку 500
        raise HTTPException(status_code=500, detail=f"Помилка сервера при збереженні замовлення: {e}")


# Приклад роута для подачі статичних файлів HTML
@app.get("/{filename}.html")
async def serve_html_file(request: Request, filename: str):
    """Обслуговує будь-який статичний HTML файл із кореня або templates/."""
    file_path = TEMPLATES_DIR / f"{filename}.html"

    if not file_path.is_file():
        # Спробуємо знайти у корені проєкту (якщо ви використовуєте FastAPI AppDir)
        file_path = BASE_DIR.parent / f"{filename}.html"

    if file_path.is_file():
        context = {"request": request}
        # Використовуємо response, щоб просто повернути HTML, якщо він не є Jinja2-шаблоном
        from fastapi.responses import FileResponse
        return FileResponse(file_path)

    raise HTTPException(status_code=404, detail=f"Файл {filename}.html не знайдено.")