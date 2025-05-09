import subprocess
import os

db_path = "library.db"
if os.path.exists(db_path):
    os.remove(db_path)
    print("Old database removed.")
else:
    print("No old database found.")


    
# Run setup_db.py
print("Running setup_db.py...")
subprocess.run(["python", "setup_db.py"], check=True)

# Run populate_db.py
print("Running populate_db.py...")
subprocess.run(["python", "populate_db.py"], check=True)

# Run simulate_events.py
print("Running simulate_events.py...")
subprocess.run(["python", "simulate_events.py"], check=True)

print("All scripts executed successfully.")
