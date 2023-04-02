import random
import string
import time

from fastapi import FastAPI, Request

from api.core.config import settings
from api.core.loggr import loggr
from api.routers import router as main_router
from api.utils.constants import DEPLOY_ENVIRONMENT_LOCAL

logger = loggr.get_logger(__name__)

openapi_url = None
docs_url = None
redoc_url = None
swagger_ui_oauth2_redirect_url = None

if settings.deploy_environment == DEPLOY_ENVIRONMENT_LOCAL:
    openapi_url = "/openapi.json"
    docs_url = "/docs"
    redoc_url = "/redoc"
    swagger_ui_oauth2_redirect_url = "/docs/oauth2-redirect"

app = FastAPI(
    title="Boardie Backoffice Backend",
    description="Written with love with FastAPI",
    version="0.1.0",
    contact={"name": "Alex Brou", "email": "alexandrepilarbrou@gmail.com"},
    openapi_url=openapi_url,
    docs_url=docs_url,
    redoc_url=redoc_url,
    swagger_ui_oauth2_redirect_url=swagger_ui_oauth2_redirect_url,
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = "{0:.2f}".format(process_time)
    logger.info(
        f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}"
    )
    return response


app.include_router(
    main_router,
    prefix="",
)
