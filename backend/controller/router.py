from fastapi import APIRouter

from backend.controller import autocomplete, model, feedback

router = APIRouter()
router.include_router(autocomplete.router, tags=["autocomplete"])
router.include_router(model.router, tags=["model"])
router.include_router(feedback.router, tags=["feedback"])
