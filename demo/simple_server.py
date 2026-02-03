from fastapi import FastAPI
import time
app = FastAPI()
@app.get('/status')
async def status():
    return {'status':'ok','time':time.time()}
