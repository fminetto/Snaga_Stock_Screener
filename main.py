from fastapi import FastAPI
from routers import WalletRouter

app = FastAPI()
app.include_router(WalletRouter)
