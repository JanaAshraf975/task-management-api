from fastapi import FastAPI
from logging_config import setup_logging
from middleware import request_id_middleware
from routes import router


setup_logging()

app = FastAPI()

# Register middleware
app.middleware("http")(request_id_middleware)

# Register routes
app.include_router(router)