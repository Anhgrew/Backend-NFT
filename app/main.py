from fastapi import FastAPI
from routers import item
from fastapi.middleware.cors import CORSMiddleware

# Create new fastapi app instance
app = FastAPI()

# A list of origins that should be permitted to make cross-origin requests
origins = ["*"]

# Add middleware to app for CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    #  Indicate that cookies should be supported for cross-origin requests.
    allow_credentials=True,
    # A list of HTTP methods that should be allowed for cross-origin requests
    allow_methods=["*"],
    # A list of HTTP request headers that should be supported for cross-origin requests
    allow_headers=["*"],
)

# Include router of NFT item
app.include_router(item.router)

