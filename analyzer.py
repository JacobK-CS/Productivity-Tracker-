import sqlite3


conn = sqlite3.connect('excuses.db')
cursor = conn.cursor()


cursor.execute('''
    SELECT 
        app_name, 
        SUM(input_count) as total_inputs, "asdwa"
        (COUNT(id) * 10) as time_spent_seconds
    FROM activity_log
    GROUP BY app_name
    ORDER BY time_spent_seconds DESC
''')

results = cursor.fetchall()
conn.close()

print("\n📊 --- THE EXCUSE DETECTOR: WEEKLY REPORT --- 📊\n")

if not results:
    print("No data found! Make sure your observer.py is running.")
    exit()


creation_apps = ["Code", "Microsoft Word", "Pages", "TextEdit", "Notes"]
research_apps = ["Google Chrome", "Safari", "Brave Browser", "Preview"]
admin_apps = ["Finder", "Mail", "Calendar"]


for row in results:
    app_name = row[0]
    inputs = row[1]
    time_spent_sec = row[2]

    time_spent_min = round(time_spent_sec / 60, 2)
    
    print(f"🔹 {app_name}: {time_spent_min} minutes | {inputs} total keystrokes/clicks")

    if app_name in research_apps and time_spent_min > 2 and inputs < 20:
        print("   🚨 FLAG: Productive Procrastination detected. You are just watching/reading without taking notes!")
        

    elif app_name in creation_apps and time_spent_min > 2 and inputs < 30:
        print("   🚨 FLAG: Staring at a blank page. Break the task down and write just one sentence.")
        

    elif app_name in admin_apps and time_spent_min > 1:
        print("   🚨 FLAG: Organizing folders feels like work, but it's not the assignment.")

print("\n------------------------------------------------\n")