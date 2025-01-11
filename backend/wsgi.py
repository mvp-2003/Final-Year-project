from app import app
from pyngrok import ngrok

ngrok.set_auth_token("2rDb5PWkQlTDo3ndagFZguAJ5ii_7iAFj9dqDmZWQiTPHS4Ka")
public_url = ngrok.connect(5000)
print(" * ngrok tunnel \"{}\" -> \"http://127.0.0.1:5000\"".format(public_url))

if __name__ == "__main__":
    app.run()
