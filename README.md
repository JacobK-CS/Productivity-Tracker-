# The Excuse Detector: A macOS Productivity Tracker

I built this because I needed a way to track my own workflow and figure out when I was actually working versus just clicking around. I love diving into data and finding edges in the numbers, so I decided to build a logic engine to monitor my own daily habits.

This is a native macOS application written in Python. It runs completely silently in the background, tapping into system APIs to track what applications I have open and how much input I am actually generating. It then securely logs all that raw data into a local SQLite database.

The best part is the analytics engine built on top of it. It calculates my input ratios to detect when I am productively procrastinating and fires off automated desktop alerts to get me back on track.

## Tech Stack
* Language: Python
* System Integration: macOS APIs and Background Listeners
* Database: Local SQLite
* Analytics: Custom logic engine for time series metrics

## Core Features
* Silent Monitoring: Tracks active application focus and user input volume without getting in the way.
* Data Pipeline: Efficiently logs all metrics locally via SQLite.
* The Logic Engine: Analyzes historical user data to calculate input ratios and catch procrastination.
* Automated Reporting: Generates weekly productivity reports and custom desktop alerts to keep users honest.
  
