from flask import Flask
import webbrowser
import threading
import random

app = Flask(__name__)

SITES = [
    # School tools
    "https://app.schoology.com",
    "https://www.khanacademy.org",
    "https://codehs.com",
    "https://code.org",
    "https://classroom.google.com",
    # Coding / your stuff
    "https://github.com",
    "https://github.com/DaEpickid540",  # my profile lol
    "https://replit.com",
    "https://leetcode.com",
    # Other legit edu sites
    "https://quizlet.com",
    "https://www.desmos.com/calculator",
    "https://www.wolframalpha.com",
    "https://brilliant.org",
    "https://www.duolingo.com",
    "https://www.coursera.org",
    "https://www.edx.org",
    "https://www.codecademy.org",
    "https://scratch.mit.edu",
    "https://www.typing.com",
    "https://www.commonlit.org",
    "https://www.ixl.com",
    "https://www.readworks.org",
    "https://docs.google.com",
    "https://drive.google.com",
    # You can add other sites, use it for work, even load up something like update faker or work sites ;)
]

@app.route('/trigger')
def trigger():
    url = random.choice(SITES)
    print(f"Door opened! Opening -> {url}")
    threading.Thread(target=lambda: webbrowser.open_new_tab(url)).start()
    return "ok", 200

if __name__ == '__main__':
    print("Mom detector running on port 5555...")
    app.run(host='0.0.0.0', port=5555)