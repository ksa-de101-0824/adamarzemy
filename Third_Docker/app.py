from fastapi import FastAPI, Form

app = FastAPI()

FILE_PATH = "/data/storage.txt"  # Path to store user inputs in the volume

@app.post("/submit/")
def submit_input(user_input: str = Form(...)):
    # Save the user input to the file
    with open(FILE_PATH, "a") as f:
        f.write(user_input + "\n")
    return {"status": "Input received", "input": user_input}

@app.get("/")
def read_inputs():
    # Read all inputs from the file
    try:
        with open(FILE_PATH, "r") as f:
            content = f.read().splitlines()
    except FileNotFoundError:
        content = []
    return {"saved_inputs": content}