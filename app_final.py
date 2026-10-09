from fastapi import FastAPI

app = FastAPI(title="HSE Document Finder")


@app.get("/")
def root():
    return {"message": "base endpoint"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/version")
def version():
    return {"version": "0.1v"}
