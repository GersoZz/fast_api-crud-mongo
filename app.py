from fastapi import FastAPI
from routes.user import user
from docs import tags_metadata

app = FastAPI(
  title = "CRUD with Users",
  description = "Simple REST API CRUD with FastAPI and Mongodb",
  version = "1.0.0",
  openapi_tags = tags_metadata
)

app.include_router(user)