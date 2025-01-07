import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import sys

class GameFileEventHandler(FileSystemEventHandler):
    def __init__(self, game_script):
        self.game_script = game_script
        self.process = None
        self.start_game()

    def start_game(self):
        if self.process:
            self.process.terminate()
            self.process.wait()
        self.process = subprocess.Popen([sys.executable, self.game_script])

    def on_modified(self, event):
        if event.src_path == os.path.abspath(self.game_script):
            print(f"{self.game_script} has been modified. Restarting the game.")
            self.start_game()

if __name__ == "__main__":
    game_script = "game.py"
    event_handler = GameFileEventHandler(game_script)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(os.path.abspath(game_script)), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
