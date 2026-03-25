import streamlit as st
import tldextract
import sqlite3
import random
from datetime import datetime

# --- 1. إعداد قاعدة البيانات ---
def init_db():
    conn = sqlite3.connect('ayman_guard.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reports 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT, date TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS stats (id INTEGER PRIMARY KEY, scan_count INTEGER)''')
    c.execute('''INSERT OR IGNORE INTO stats (id, scan_count) VALUES (1, 250)''')
    conn.commit()
    conn.close()

def update_scan_count():
    conn = sqlite3.connect('ayman_guard.db')
    c = conn.cursor()
    c.execute("UPDATE stats SET scan_count = scan_count + 1 WHERE id = 1")
    conn.commit()
    conn.close()

def get_stats():
    conn = sqlite3.connect('ayman_guard.db')
    c = conn.cursor()
    c.execute("SELECT scan_count FROM stats WHERE id = 1")
    res = c.fetchone()
    conn.close()
    return res[0] if res else 250

def add_report(url):
    conn = sqlite3.connect('ayman_guard.db')
    c = conn.cursor()
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    c.execute("INSERT INTO reports (url, date) VALUES (?, ?)", (url, date_str))
    conn.commit()
    conn.close()

def get_reports():
    conn = sqlite3.connect('ayman_guard.db')
    c = conn.cursor()
    c.execute("SELECT url
