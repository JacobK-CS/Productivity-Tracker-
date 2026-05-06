import time
import sqlite3
from AppKit import NSWorkspace
from pynput import keyboard, mouse

conn = sqlite3.connect('excuses.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS activity_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        app_name TEXT,
        input_count INTEGER
    )
''')
conn.commit()

total_inputs = 0

def on_press(key):
    global total_inputs
    total_inputs += 1

def on_click(x, y, button, pressed):
    global total_inputs
    if pressed:
        total_inputs += 1

def on_scroll(x, y, dx, dy):
    global total_inputs
    total_inputs += 1

keyboard_listener = keyboard.Listener(on_press=on_press)
mouse_listener = mouse.Listener(on_click=on_click, on_scroll=on_scroll)
keyboard_listener.start()
mouse_listener.start()

def get_active_window():
    active_app = NSWorkspace.sharedWorkspace().activeApplication()
    return active_app['NSApplicationName']

print("👀 Excuse Detector Observer started...")
print("Saving activity to local database... (Press Ctrl+C to stop)\n")

try:
    while True:
        time.sleep(10)
        
        current_app = get_active_window()
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('''
            INSERT INTO activity_log (timestamp, app_name, input_count)
            VALUES (?, ?, ?)
        ''', (current_time, current_app, total_inputs))
        
        conn.commit()
        
        print(f"Saved -> [{current_time}] App: {current_app} | Inputs: {total_inputs}")
        
        total_inputs = 0
        
except KeyboardInterrupt:
    print("\nObserver stopped. Closing database connection.")
    conn.close()