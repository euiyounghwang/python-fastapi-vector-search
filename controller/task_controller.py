
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from service.Handler.job.task import TaskState
from service.Handler.search.StatusHanlder import StatusHanlder



app = APIRouter(
    # prefix="/api",
)


state = TaskState()

@app.post("/post_job", status_code=StatusHanlder.HTTP_STATUS_200)
async def send_notification(background_tasks: BackgroundTasks):
    background_tasks.add_task(state.background_work)
    return {"message": "Job Created, check status after some time!"}

@app.get("/get_status")
def status():
    return state.get_state()