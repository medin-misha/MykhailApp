from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
from api import main_router\

# @asynccontextmanager
# async def lifespan(app: FastAPI) -> None:
#     await user_broker.start()
#     yield
#     await user_broker.close()


app = FastAPI()
app.include_router(main_router)


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)