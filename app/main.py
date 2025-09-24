from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
from api import main_router, user_broker

@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    await user_broker.start()
    yield
    await user_broker.close()


app = FastAPI(lifespan=lifespan)
app.include_router(main_router)


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)