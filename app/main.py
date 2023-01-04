from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.public_toilets import routes as public_toilets_routes
from app.users import routes as users_routes
from app.default import routes as default_routes


Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3000/registration",
    "http://localhost:3000/add-public-toilet",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(default_routes.router)
app.include_router(public_toilets_routes.router)
app.include_router(users_routes.router)
