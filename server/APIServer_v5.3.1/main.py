from application import create_app

app = create_app()



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, auto_reload=True, access_log=False)