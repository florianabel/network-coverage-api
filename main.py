from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {
        "orange": {"2G": True, "3G": True, "4G": False}, 
        "SFR": {"2G": True, "3G": True, "4G": True}
    }