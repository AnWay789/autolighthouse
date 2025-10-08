from main import get_lighthouse_stats
import time

while True:
    get_lighthouse_stats()
    time.sleep(600)  # Sleep for 10 minutes
