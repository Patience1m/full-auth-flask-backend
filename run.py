from app import create_app

app = create_app("development")

if __name__ == "__main__":
    app.run(port=5555, debug=True)  # the client proxies to port 5555
