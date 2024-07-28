# start.py
import uvicorn



from app import create_app
from config import ip,port

app = create_app()
if __name__ == "__main__":
    uvicorn.run(app, host=ip, port=port)
