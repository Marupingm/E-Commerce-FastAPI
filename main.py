from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, products, cart, orders
from app.database import create_tables

app = FastAPI(title="E-Commerce API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api", tags=["Authentication"])
app.include_router(products.router, prefix="/api", tags=["Products"])
app.include_router(cart.router, prefix="/api", tags=["Cart"])
app.include_router(orders.router, prefix="/api", tags=["Orders"])

# Create database tables
create_tables()

@app.get("/")
async def root():
    return {"message": "Welcome to E-Commerce API"} # Modified on 2025-02-20 13:01:06
# Modified on 2025-02-20 13:03:24
