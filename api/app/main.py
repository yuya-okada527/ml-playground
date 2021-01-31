from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def sample():
    return "hoge"
