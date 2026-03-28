from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routes.chat import router as chat_router
from backend.api.routes.configuration import router as config_router
from backend.api.routes.health import router as health_router
from backend.api.routes.quran_testing import router as quran_testing_router
from backend.config import Settings, settings
from backend.services.quran_local_lookup_service import QuranLocalLookupService
from backend.services.quran_api_testing_service import QuranAPITestingService
from backend.services.rag_service import RAGService


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.quran_local_lookup_service = QuranLocalLookupService(app.state.settings)
    app.state.rag_service = RAGService(
        app.state.settings,
        quran_lookup_service=app.state.quran_local_lookup_service,
    )
    app.state.quran_api_testing_service = QuranAPITestingService()
    yield
    app.state.quran_api_testing_service.close()


def create_app(custom_settings: Settings | None = None) -> FastAPI:
    app_settings = custom_settings or settings

    app = FastAPI(
        title=app_settings.app_name,
        lifespan=lifespan,
    )
    app.state.settings = app_settings

    app.add_middleware(
        CORSMiddleware,
        allow_origins=app_settings.cors_allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router)
    app.include_router(config_router, prefix=app_settings.api_prefix)
    app.include_router(chat_router, prefix=app_settings.api_prefix)
    app.include_router(quran_testing_router, prefix=app_settings.api_prefix)

    return app


app = create_app()
