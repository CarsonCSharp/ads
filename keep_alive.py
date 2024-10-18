from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def main():
    # Display the message to indicate that the user can now set up UptimeRobot
     return '''
         <h1>Logged into account, use uptimer now!</h1>
         <br>
         <form action="https://www.youtube.com/@TriplCore" method="get">
             <button type="submit">TriplCore YouTube</button>
         </form>
         '''

def run():
     # Run the web server on the given host and port
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
     # Start the web server in a separate thread to keep the Replit project alive
    server = Thread(target=run)
    server.start()
