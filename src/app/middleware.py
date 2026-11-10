import uuid
from logging_config import request_id_var


async def request_id_middleware(request, call_next):

    request_id = str(uuid.uuid4())

    token = request_id_var.set(request_id)

    try:
        response = await call_next(request)

        response.headers["X-Request-ID"] = request_id

        return response

    finally:
        request_id_var.reset(token)