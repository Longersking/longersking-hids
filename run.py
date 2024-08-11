# start.py

import uvicorn

from app.main import app
from config import ip, port
if __name__ == "__main__":
    uvicorn.run(app, host=ip, port=port)
