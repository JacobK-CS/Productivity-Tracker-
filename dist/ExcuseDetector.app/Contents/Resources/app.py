import rumps
import time
import sqlite3
from AppKit import NSWorkspace
from pynput import keyboard, mouse

# 1. Global Input Counter
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

# 2. Build the Mac App
class ExcuseDetectorApp(rumps.App):
    def __init__(self):
        # The emoji is what will show up in your Mac menu bar!
        super(ExcuseDetectorApp, self).__init__("🕵️‍♂️") 
        self.menu = ["Run Weekly Report"]

        # Connect to Database
        self.conn = sqlite3.connect('excuses.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS activity_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                app_name TEXT,
                input_count INTEGER
            )
        ''')
        self.conn.commit()

        # Start tracking keyboard and mouse
        self.keyboard_listener = keyboard.Listener(on_press=on_press)
        self.mouse_listener = mouse.Listener(on_click=on_click, on_scroll=on_scroll)
        self.keyboard_listener.start()
        self.mouse_listener.start()

    def get_active_window(self):
        active_app = NSWorkspace.sharedWorkspace().activeApplication()
        return active_app['NSApplicationName']

    # 3. The Observer (Runs automatically every 10 seconds)
    @rumps.timer(10)
    def track_activity(self, _):
        global total_inputs
        current_app = self.get_active_window()
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')

        self.cursor.execute('''
            INSERT INTO activity_log (timestamp, app_name, input_count)
            VALUES (?, ?, ?)
        ''', (current_time, current_app, total_inputs))
        self.conn.commit()
        
        # Reset counter for the next 10 seconds
        total_inputs = 0 

    # 4. The Analyzer (Runs when you click the menu button)
    @rumps.clicked("Run Weekly Report")
    def run_report(self, _):
        self.cursor.execute('''
            SELECT app_name, SUM(input_count), (COUNT(id) * 10)
            FROM activity_log 
            GROUP BY app_name 
            ORDER BY (COUNT(id) * 10) DESC
        ''')
        results = self.cursor.fetchall()

        if not results:
            rumps.alert("No data yet! Give it a minute.")
            return

        report_text = ""
        research_apps = ["Google Chrome", "Safari", "Brave Browser"]

        for row in results:
            app_name = row[0]
            inputs = row[1]
            time_sec = row[2]
            time_min = round(time_sec / 60, 2)
            
            report_text += f"🔹 {app_name}: {time_min} min | {inputs} inputs\n"

            # The Excuse Trap (Still set to 2 minutes for testing)
            if app_name in research_apps and time_min > 2 and inputs < 20:
                report_text += "  🚨 FLAG: Productive Procrastination detected!\n"

        # Pop up a real Mac alert window!
        rumps.alert(title="📊 The Excuse Detector Report", message=report_text)

if __name__ == "__main__":
    # Start the app
    ExcuseDetectorApp().run()