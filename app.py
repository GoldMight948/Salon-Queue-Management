import sqlite3
import uuid
from datetime import datetime, date, time, timedelta, timezone
from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

APP_DIR = Path(__file__).parent
DB_PATH = Path(__import__("os").environ.get("SALON_DB_PATH", APP_DIR / "salon_queue.db"))
TZ_LABEL = "Asia/Kolkata"

st.set_page_config(page_title="Salon Queue", layout="wide", initial_sidebar_state="expanded")

# ---------- Translations (English / Gujarati) ----------
TRANSLATIONS = {
    "English": {
        "title": "Salon Queue",
        "tagline": "QUEUE MANAGEMENT",
        "hero_title": "Good day. Your queue, at a glance.",
        "hero_sub": "A calmer way to run the salon — from first token to final service.",
        "waiting": "WAITING",
        "in_service": "IN SERVICE",
        "served_today": "SERVED TODAY",
        "available_barbers": "BARBERS AVAILABLE",
        "queue_right_now": "Queue right now",
        "team_availability": "Team availability",
        "quick_actions": "Quick actions",
        "add_customer": "Register walk-in",
        "reception_desk": "Reception desk",
        "auto_assign": "Auto-assign queue",
        "live_display": "Live TV display",
        "quick_walkin": "Walk-in registration",
        "join_title": "Join the queue",
        "join_sub": "Choose your service and we will save your place.",
        "your_name": "Your name",
        "mobile_number": "Mobile number",
        "select_services": "Select services (max 3)",
        "preferred_barber": "Preferred barber",
        "no_preference": "No preference (fastest)",
        "get_token": "Get my token",
        "reception_title": "Reception desk",
        "reception_sub": "Manage chairs, dispatch customers, and monitor live service timers.",
        "barber_desk_title": "Barber desk",
        "barber_desk_sub": "Your chair, your customers, your pace.",
        "display_title": "Now serving",
        "display_sub": "A clear, calm view for the waiting area.",
        "admin_title": "Salon settings",
        "admin_sub": "Manage services, the team and online queue availability.",
        "track_title": "Track your token",
        "track_sub": "Check where you are in the queue and watch your live timer.",
        "start_coming": "Start coming to the salon — You are 2nd in line!",
        "cancel_spot": "Cancel my spot",
        "confirm_cancel": "Yes, cancel my spot",
        "people_ahead": "People ahead",
        "est_wait": "Estimated wait",
        "elapsed_wait": "Elapsed wait time",
        "complete_service": "Complete service",
        "call_next": "Call next customer",
        "take_break": "Take a break",
        "end_break": "End break",
        "save_services": "Save all service changes",
        "lounge_radio_title": "Waiting Lounge Ambience · Deluxe Saloon Radio",
        "lounge_radio_sub": "Authentic 90s Indian barber shop melodies streaming live from saloon.wtf.",
        "enable_lounge_radio": "Stream waiting lounge radio",
        "floating_radio_pill": "Saloon Radio",
        "floating_radio_header": "Deluxe Saloon · Retro Barber Shop Radio",
    },
    "ગુજરાતી": {
        "title": "સેલોન કતાર",
        "tagline": "કતાર સંચાલન",
        "hero_title": "નમસ્તે. તમારી સેલોન કતારની સ્થિતિ.",
        "hero_sub": "સેલોન ચલાવવાની એક સરળ અને શાંત રીત.",
        "waiting": "પ્રતીક્ષામાં",
        "in_service": "સેવા ચાલુ છે",
        "served_today": "આજે સેવા પૂર્ણ",
        "available_barbers": "હાજર વાળંદ",
        "queue_right_now": "હાલની કતાર",
        "team_availability": "વાળંદની સ્થિતિ",
        "quick_actions": "ઝડપી ક્રિયાઓ",
        "add_customer": "વોક-ઇન નોંધણી",
        "reception_desk": "રિસેપ્શન ડેસ્ક",
        "auto_assign": "આપોઆપ વાળંદ સોંપો",
        "live_display": "લાઈવ ટીવી ડિસ્પ્લે",
        "quick_walkin": "ઝડપી વોક-ઇન નોંધણી",
        "join_title": "કતારમાં જોડાઓ",
        "join_sub": "તમારી સેવા પસંદ કરો અને અમે તમારો વારો સાચવીશું.",
        "your_name": "તમારું નામ",
        "mobile_number": "મોબાઇલ નંબર",
        "select_services": "સેવાઓ પસંદ કરો (મહત્તમ 3)",
        "preferred_barber": "પસંદગીના વાળંદ",
        "no_preference": "કોઈ પસંદગી નથી (સૌથી ઝડપી)",
        "get_token": "મારું ટોકન મેળવો",
        "reception_title": "રિસેપ્શન ડેસ્ક",
        "reception_sub": "ખુરશીઓનું સંચાલન કરો, કતાર આગળ વધારો અને લાઈવ ટાઈમર જુઓ.",
        "barber_desk_title": "વાળંદ ડેસ્ક",
        "barber_desk_sub": "તમારી ખુરશી, તમારા ગ્રાહકો, તમારી ગતિ.",
        "display_title": "હાલમાં સેવામાં",
        "display_sub": "પ્રતીક્ષા વિસ્તાર માટે સ્વચ્છ અને શાંત ડિસ્પ્લે.",
        "admin_title": "સેલોન સેટિંગ્સ",
        "admin_sub": "સેવાઓ, ટીમ અને ઓનલાઇન કતારની ઉપલબ્ધતાનું સંચાલન કરો.",
        "track_title": "તમારું ટોકન ટ્રેક કરો",
        "track_sub": "કતારમાં તમારું સ્થાન અને લાઈવ ટાઈમર જુઓ.",
        "start_coming": "સેલોન આવવા માટે નીકળો — તમે લાઈનમાં 2જા છો!",
        "cancel_spot": "મારો વારો રદ કરો",
        "confirm_cancel": "હા, મારો વારો રદ કરો",
        "people_ahead": "આગળના ગ્રાહકો",
        "est_wait": "અંદાજિત રાહ",
        "elapsed_wait": "રાહ જોવાનો સમય",
        "complete_service": "સેવા પૂર્ણ કરો",
        "call_next": "આગળના ગ્રાહકને બોલાવો",
        "take_break": "વિરામ લો",
        "end_break": "વિરામ સમાપ્ત કરો",
        "save_services": "સેવાના તમામ ફેરફારો સાચવો",
        "lounge_radio_title": "પ્રતીક્ષા લાઉન્જ સંગીત · ડીલક્સ સલૂન રેડિયો",
        "lounge_radio_sub": "પ્રતીક્ષા કરી રહેલા ગ્રાહકો માટે saloon.wtf પરથી 90ના દાયકાના રેટ્રો વાળંદ ગીતોનું લાઈવ પ્રસારણ.",
        "enable_lounge_radio": "લાઉન્જ રેડિયો પ્લેયર ચાલુ કરો",
        "floating_radio_pill": "સલૂન રેડિયો",
        "floating_radio_header": "ડીલક્સ સલૂન · રેટ્રો વાળંદ રેડિયો",
    }
}

def t(key):
    lang = st.session_state.get("lang_choice", "English")
    return TRANSLATIONS.get(lang, {}).get(key, TRANSLATIONS["English"].get(key, key))

# ---------- Styling ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #f8f9fb; }
.block-container { padding-top: 1.5rem; padding-bottom: 3rem; max-width: 1440px; }
h1,h2,h3,h4 { font-family: 'Manrope', sans-serif; color: #171a2b; letter-spacing: -0.035em; }
.hero { background: linear-gradient(120deg,#171a2b 0%,#2d3250 100%); padding: 1.8rem 2.2rem; border-radius: 16px; color: white; margin-bottom: 1.2rem; }
.hero h1 { color:white; font-size:2.1rem; margin:0; }
.hero p { color:#d9dcef; margin:.3rem 0 0 0; font-size:0.95rem; }
.metric-card { background:white; padding:1.1rem 1.2rem; border:1px solid #e9eaf1; border-radius:12px; }
.metric-label { color:#777d91; font-size:.8rem; font-weight:600; letter-spacing:0.02em; }
.metric-value { color:#191d31; font-family:Manrope,sans-serif; font-size:1.8rem; font-weight:800; margin-top:.2rem; }
.panel { background:white; border:1px solid #e9eaf1; padding:1.1rem 1.2rem; border-radius:14px; margin-bottom:0.8rem; }
.chair-card { background:white; border:1px solid #e2e8f0; border-radius:12px; padding:1.1rem; margin-bottom:0.9rem; }
.chair-card-serving { border-left:4px solid #0f766e; }
.chair-card-available { border-left:4px solid #3b82f6; }
.chair-card-break { border-left:4px solid #94a3b8; }
.token { background:#f0efff; color:#4a3fc5; padding:.3rem .65rem; border-radius:6px; font-weight:800; font-size:0.95rem; }
.status { display:inline-block; padding:.22rem .55rem; border-radius:99px; font-size:.76rem; font-weight:700; background:#edf0f7; color:#515a70; }
.status-waiting { background:#fef3c7; color:#92400e; }
.status-called { background:#ede9fe; color:#5b21b6; }
.status-in_chair { background:#dcfce7; color:#166534; }
.status-done { background:#f1f5f9; color:#475569; }
.timer-pill { display:inline-flex; align-items:center; padding:.2rem .55rem; border-radius:6px; font-size:.78rem; font-weight:700; font-family:monospace; }
.timer-pill-calm { background:#f1f5f9; color:#334155; }
.timer-pill-warn { background:#fef3c7; color:#92400e; }
.timer-pill-alert { background:#fee2e2; color:#991b1b; }
.alert-box { border-left: 4px solid #0f766e; background:#f0fdfa; padding: 0.9rem 1.1rem; border-radius:10px; margin-bottom:1rem; color:#134e4a; font-weight:600; }
.alert-box-warn { border-left: 4px solid #e07a5f; background:#fff7ed; padding: 0.9rem 1.1rem; border-radius:10px; margin-bottom:1rem; color:#9a3412; font-weight:600; }
.summary-box { background:#f8fafc; border:1px solid #e2e8f0; padding:1rem; border-radius:10px; margin-bottom:1rem; }
div[data-testid="stMetric"] { background:white; border:1px solid #e9eaf1; padding:1rem; border-radius:12px; }
div.stButton > button { border-radius:8px; font-weight:600; min-height:2.4rem; }
div.stButton > button[kind="primary"] { background:#171a2b; color:white; border:none; }
div.stButton > button[kind="primary"]:hover { background:#2d3250; color:white; }
section[data-testid="stSidebar"] { background:#171a2b; }
section[data-testid="stSidebar"] * { color:#f2f3fa !important; }
section[data-testid="stSidebar"] button { background:#2d3250; border:1px solid #4a5075; }
.small-muted { color:#7c8294; font-size:.85rem; }
</style>
""", unsafe_allow_html=True)

SERVICES = [
    ("haircut", "Haircut", 30, 150),
    ("beard", "Beard trim", 15, 80),
    ("spa", "Hair spa", 45, 400),
    ("shave", "Hot shave", 25, 120),
    ("color", "Coloring", 90, 800),
]
BARBERS = [("ravi", "Ravi"), ("amit", "Amit"), ("imran", "Imran")]

def db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def init_db():
    with db() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS services(
          id TEXT PRIMARY KEY, name TEXT NOT NULL, minutes INTEGER NOT NULL,
          price INTEGER NOT NULL, active INTEGER NOT NULL DEFAULT 1
        );
        CREATE TABLE IF NOT EXISTS barbers(
          id TEXT PRIMARY KEY, name TEXT NOT NULL, on_duty INTEGER NOT NULL DEFAULT 1,
          on_break INTEGER NOT NULL DEFAULT 0, current_entry_id TEXT
        );
        CREATE TABLE IF NOT EXISTS queue_entries(
          id TEXT PRIMARY KEY, token TEXT NOT NULL, customer_name TEXT NOT NULL,
          phone TEXT NOT NULL, service_id TEXT NOT NULL, service_name TEXT NOT NULL,
          duration INTEGER NOT NULL, price INTEGER NOT NULL, preferred_barber TEXT,
          status TEXT NOT NULL, created_at TEXT NOT NULL, called_at TEXT,
          started_at TEXT, finished_at TEXT, no_show_at TEXT, source TEXT NOT NULL DEFAULT 'Online',
          assigned_barber TEXT,
          FOREIGN KEY(service_id) REFERENCES services(id)
        );
        CREATE TABLE IF NOT EXISTS queue_entry_services(
          entry_id TEXT NOT NULL,
          service_id TEXT NOT NULL,
          service_name TEXT NOT NULL,
          duration INTEGER NOT NULL,
          price INTEGER NOT NULL,
          PRIMARY KEY(entry_id, service_id),
          FOREIGN KEY(entry_id) REFERENCES queue_entries(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY, value TEXT NOT NULL);
        CREATE INDEX IF NOT EXISTS idx_queue_day_status ON queue_entries(created_at,status);
        """)
        try:
            c.execute("ALTER TABLE queue_entries ADD COLUMN assigned_barber TEXT")
        except sqlite3.OperationalError:
            pass
        # Auto-upgrade any previously called entries to in_chair with started_at
        c.execute("UPDATE queue_entries SET status='in_chair', started_at=COALESCE(called_at, created_at) WHERE status='called'")
        for sid, name, mins, price in SERVICES:
            c.execute("INSERT OR IGNORE INTO services VALUES(?,?,?,?,1)", (sid,name,mins,price))
        for bid, name in BARBERS:
            c.execute("INSERT OR IGNORE INTO barbers(id,name) VALUES(?,?)", (bid,name))
        c.execute("INSERT OR IGNORE INTO settings VALUES('online_open','1')")
        c.execute("INSERT OR IGNORE INTO settings VALUES('closing_time','21:00')")
        c.execute("INSERT OR IGNORE INTO settings VALUES('salon_name','The Salon')")

init_db()

def now():
    return datetime.now(timezone(timedelta(hours=5, minutes=30))).replace(tzinfo=None)

def stamp(dt=None):
    return (dt or now()).isoformat(timespec="seconds")

def elapsed_seconds(dt_val):
    if not dt_val:
        return 0
    if isinstance(dt_val, dict):
        dt_val = dt_val.get("started_at") or dt_val.get("called_at") or dt_val.get("created_at")
    try:
        dt = datetime.fromisoformat(str(dt_val))
        return max(0, int((now() - dt).total_seconds()))
    except Exception:
        return 0

def fmt_timer_seconds(sec):
    if sec is None or sec < 0:
        return "00:00"
    sec = int(sec)
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    if h > 0:
        return f"{h}h {m:02d}m {s:02d}s"
    return f"{m:02d}m {s:02d}s"

def render_timer_badge(sec):
    m = int(sec) // 60
    cls = "timer-pill-calm" if m < 10 else ("timer-pill-warn" if m < 20 else "timer-pill-alert")
    return f'<span class="timer-pill {cls}">{fmt_timer_seconds(sec)}</span>'

def render_live_clock_html(elapsed_sec, est_mins, token, customer_name):
    est_total_sec = (est_mins or 0) * 60
    return f"""
    <div style="font-family:'DM Sans',-apple-system,BlinkMacSystemFont,sans-serif; background:linear-gradient(135deg, #171a2b 0%, #252a42 100%); border-radius:14px; padding:20px 24px; color:white; border:1px solid #333a59; margin: 10px 0;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <div style="font-size:0.75rem; letter-spacing:1px; text-transform:uppercase; color:#9fa6cc; font-weight:700;">WAITING TIMER</div>
            <div style="background:rgba(255,255,255,0.12); padding:3px 10px; border-radius:4px; font-size:0.75rem; font-weight:700;">Token {token}</div>
        </div>
        <div style="display:flex; align-items:baseline; gap:12px; margin-top:2px;">
            <span id="live_clock_val" style="font-size:3.2rem; font-weight:800; font-family:'Manrope',sans-serif; letter-spacing:-1px; color:#ffffff;">{fmt_timer_seconds(elapsed_sec)}</span>
            <span style="color:#aeb5d6; font-size:0.95rem; font-weight:500;">waited</span>
        </div>
        <div style="margin-top:14px; padding-top:12px; border-top:1px solid rgba(255,255,255,0.12); display:flex; justify-content:space-between; font-size:0.85rem; color:#d2d6ee;">
            <div>Est. remaining: <b id="live_rem_val">{est_mins if est_mins is not None else '—'} min</b></div>
            <div>Customer: <b>{customer_name}</b></div>
        </div>
    </div>
    <script>
    (function() {{
        let elapsed = {int(elapsed_sec)};
        const estTotal = {int(est_total_sec)};
        function pad(n) {{ return n < 10 ? '0' + n : n; }}
        function update() {{
            elapsed++;
            const h = Math.floor(elapsed / 3600);
            const m = Math.floor((elapsed % 3600) / 60);
            const s = elapsed % 60;
            let str = pad(m) + ':' + pad(s);
            if (h > 0) str = h + 'h ' + str;
            const clockEl = document.getElementById('live_clock_val');
            if (clockEl) clockEl.innerText = str;
            const remEl = document.getElementById('live_rem_val');
            if (remEl && estTotal > 0) {{
                const rem = Math.max(0, estTotal - elapsed);
                const remM = Math.ceil(rem / 60);
                remEl.innerText = remM > 0 ? ('~' + remM + ' min') : 'Under 1 min';
            }}
        }}
        setInterval(update, 1000);
    }})();
    </script>
    """

def render_service_clock_html(elapsed_sec, duration_mins, token, customer_name, barber_name):
    return f"""
    <div style="font-family:'DM Sans',-apple-system,BlinkMacSystemFont,sans-serif; background:linear-gradient(135deg, #171a2b 0%, #1e3328 100%); border-radius:14px; padding:20px 24px; color:white; border:1px solid #2d5a3f; margin: 10px 0;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <div style="font-size:0.75rem; letter-spacing:1px; text-transform:uppercase; color:#86efac; font-weight:700;">SERVICE TIMER · IN PROGRESS</div>
            <div style="background:rgba(255,255,255,0.12); padding:3px 10px; border-radius:4px; font-size:0.75rem; font-weight:700;">Token {token}</div>
        </div>
        <div style="display:flex; align-items:baseline; gap:12px; margin-top:2px;">
            <span id="service_clock_val" style="font-size:3.2rem; font-weight:800; font-family:'Manrope',sans-serif; letter-spacing:-1px; color:#ffffff;">{fmt_timer_seconds(elapsed_sec)}</span>
            <span style="color:#bbf7d0; font-size:0.95rem; font-weight:500;">in service</span>
        </div>
        <div style="margin-top:14px; padding-top:12px; border-top:1px solid rgba(255,255,255,0.15); display:flex; justify-content:space-between; font-size:0.85rem; color:#dcfce7;">
            <div>Target duration: <b>{duration_mins} min</b></div>
            <div>Barber: <b>{barber_name}</b></div>
        </div>
    </div>
    <script>
    (function() {{
        let elapsed = {int(elapsed_sec)};
        function pad(n) {{ return n < 10 ? '0' + n : n; }}
        function update() {{
            elapsed++;
            const h = Math.floor(elapsed / 3600);
            const m = Math.floor((elapsed % 3600) / 60);
            const s = elapsed % 60;
            let str = pad(m) + ':' + pad(s);
            if (h > 0) str = h + 'h ' + str;
            const clockEl = document.getElementById('service_clock_val');
            if (clockEl) clockEl.innerText = str;
        }}
        setInterval(update, 1000);
    }})();
    </script>
    """

def get_setting(key, default=""):
    with db() as c:
        r = c.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
        return r["value"] if r else default

def set_setting(key, value):
    with db() as c:
        c.execute("INSERT INTO settings(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (key,str(value)))

def services(active_only=False):
    with db() as c:
        q = "SELECT * FROM services" + (" WHERE active=1" if active_only else "") + " ORDER BY name"
        return [dict(x) for x in c.execute(q).fetchall()]

def barbers():
    with db() as c:
        return [dict(x) for x in c.execute("SELECT * FROM barbers ORDER BY name").fetchall()]

def entries(statuses=None, today_only=False):
    sql = "SELECT * FROM queue_entries"
    clauses, args = [], []
    if statuses:
        clauses.append("status IN (" + ",".join("?" for _ in statuses) + ")")
        args.extend(statuses)
    if today_only:
        clauses.append("date(created_at)=date(?)")
        args.append(stamp()[:10])
    if clauses: sql += " WHERE " + " AND ".join(clauses)
    sql += " ORDER BY created_at, rowid"
    with db() as c:
        return [dict(x) for x in c.execute(sql,args).fetchall()]

def next_token(c):
    day = stamp()[:10]
    count = c.execute("SELECT COUNT(*) n FROM queue_entries WHERE date(created_at)=date(?)", (day,)).fetchone()["n"]
    return f"S-{count+1:03d}"

def auto_assign_entry(c, entry_id, preferred=None, fallback_to_any=False):
    if preferred:
        barber = c.execute("""
            SELECT * FROM barbers 
            WHERE id=? AND on_duty=1 AND on_break=0 AND current_entry_id IS NULL
        """, (preferred,)).fetchone()
        if barber:
            ts = stamp()
            c.execute("UPDATE queue_entries SET status='in_chair', called_at=?, started_at=?, assigned_barber=? WHERE id=?",
                      (ts, ts, barber["id"], entry_id))
            c.execute("UPDATE barbers SET current_entry_id=? WHERE id=?", (entry_id, barber["id"]))
            return True, dict(barber)
        if not fallback_to_any:
            return False, None

    free_barbers = c.execute("""
        SELECT b.*, 
               (SELECT COUNT(*) FROM queue_entries q 
                WHERE q.assigned_barber = b.id AND date(q.created_at) = date('now', 'localtime')) as served_count
        FROM barbers b
        WHERE b.on_duty=1 AND b.on_break=0 AND b.current_entry_id IS NULL
        ORDER BY served_count ASC, b.name ASC
    """).fetchall()
    if free_barbers:
        barber = free_barbers[0]
        ts = stamp()
        c.execute("UPDATE queue_entries SET status='in_chair', called_at=?, started_at=?, assigned_barber=? WHERE id=?",
                  (ts, ts, barber["id"], entry_id))
        c.execute("UPDATE barbers SET current_entry_id=? WHERE id=?", (entry_id, barber["id"]))
        return True, dict(barber)
    return False, None

def dispatch_waiting_queue(c=None):
    def _run(conn):
        assignments = []
        free = [dict(b) for b in conn.execute(
            "SELECT * FROM barbers WHERE on_duty=1 AND on_break=0 AND current_entry_id IS NULL ORDER BY name"
        ).fetchall()]
        if not free:
            return assignments

        free_by_id = {b["id"]: b for b in free}
        waiting = [dict(e) for e in conn.execute(
            "SELECT * FROM queue_entries WHERE status='waiting' ORDER BY created_at ASC, rowid ASC"
        ).fetchall()]
        if not waiting:
            return assignments

        assigned_entry_ids = set()

        # Pass 1: Customers with preferred barber who is free
        for e in waiting:
            pref = e.get("preferred_barber")
            if pref and pref in free_by_id:
                barber = free_by_id.pop(pref)
                ts = stamp()
                conn.execute("UPDATE queue_entries SET status='in_chair', called_at=?, started_at=?, assigned_barber=? WHERE id=?",
                             (ts, ts, barber["id"], e["id"]))
                conn.execute("UPDATE barbers SET current_entry_id=? WHERE id=?", (e["id"], barber["id"]))
                assigned_entry_ids.add(e["id"])
                assignments.append({
                    "token": e["token"],
                    "customer_name": e["customer_name"],
                    "barber_name": barber["name"]
                })

        # Pass 2: Customers with no preference to remaining free barbers
        for e in waiting:
            if not free_by_id:
                break
            if e["id"] in assigned_entry_ids:
                continue
            if not e.get("preferred_barber"):
                barber_id, barber = free_by_id.popitem()
                ts = stamp()
                conn.execute("UPDATE queue_entries SET status='in_chair', called_at=?, started_at=?, assigned_barber=? WHERE id=?",
                             (ts, ts, barber["id"], e["id"]))
                conn.execute("UPDATE barbers SET current_entry_id=? WHERE id=?", (e["id"], barber["id"]))
                assigned_entry_ids.add(e["id"])
                assignments.append({
                    "token": e["token"],
                    "customer_name": e["customer_name"],
                    "barber_name": barber["name"]
                })

        return assignments

    if c:
        return _run(c)
    else:
        with db() as conn:
            return _run(conn)

def add_customer(name, phone, service_ids, preferred=None, source="Online"):
    name, phone = name.strip(), "".join(ch for ch in phone if ch.isdigit())
    if len(name) < 2: raise ValueError("Please enter the customer's name.")
    if len(phone) < 10 or len(phone) > 13: raise ValueError("Enter a valid phone number.")
    if isinstance(service_ids, str):
        service_ids = [service_ids]
    service_ids = list(dict.fromkeys(service_ids))
    if not service_ids: raise ValueError("Choose at least one service.")
    with db() as c:
        active = c.execute("SELECT token, id FROM queue_entries WHERE phone=? AND status IN ('waiting','called','in_chair') AND date(created_at)=date(?)", (phone,stamp()[:10])).fetchone()
        if active: raise ValueError(f"This number already has an active spot today: Token {active['token']}.")
        placeholders = ",".join("?" for _ in service_ids)
        selected = c.execute(f"SELECT * FROM services WHERE id IN ({placeholders}) AND active=1", service_ids).fetchall()
        if len(selected) != len(service_ids):
            raise ValueError("One or more selected services are unavailable. Refresh and try again.")
        selected = sorted(selected, key=lambda s: service_ids.index(s["id"]))
        service_name = " + ".join(s["name"] for s in selected)
        total_duration = sum(s["minutes"] for s in selected)
        total_price = sum(s["price"] for s in selected)
        token = next_token(c)
        eid = str(uuid.uuid4())
        c.execute("""INSERT INTO queue_entries
          (id,token,customer_name,phone,service_id,service_name,duration,price,preferred_barber,status,created_at,source)
          VALUES(?,?,?,?,?,?,?,?,?,'waiting',?,?)""",
          (eid,token,name,phone,selected[0]["id"],service_name,total_duration,total_price,preferred,stamp(),source))
        c.executemany("""INSERT INTO queue_entry_services
          (entry_id,service_id,service_name,duration,price) VALUES(?,?,?,?,?)""",
          [(eid,s["id"],s["name"],s["minutes"],s["price"]) for s in selected])

        # Automatically assign customer: if free, start service and timer immediately
        assigned, barber = auto_assign_entry(c, eid, preferred, fallback_to_any=False)
        assigned_name = barber["name"] if assigned else None
        return token, eid, assigned_name

def update_entry(eid, status):
    allowed = {"waiting":{"called","in_chair","cancelled"}, "called":{"in_chair","done","no_show","cancelled"},
               "in_chair":{"done","no_show","cancelled"}, "done":set(), "cancelled":set(), "no_show":set()}
    with db() as c:
        row = c.execute("SELECT * FROM queue_entries WHERE id=?", (eid,)).fetchone()
        if not row: raise ValueError("Queue entry not found.")
        if status not in allowed.get(row["status"], set()):
            raise ValueError(f"Cannot change {row['status']} to {status}.")
        ts = stamp()
        if status in ("called", "in_chair"):
            status = "in_chair"
            c.execute("UPDATE queue_entries SET status='in_chair', called_at=COALESCE(called_at, ?), started_at=? WHERE id=?", (ts, ts, eid))
        elif status == "done":
            c.execute("UPDATE queue_entries SET status='done', finished_at=? WHERE id=?", (ts, eid))
        elif status == "no_show":
            c.execute("UPDATE queue_entries SET status='no_show', no_show_at=? WHERE id=?", (ts, eid))
        else:
            c.execute("UPDATE queue_entries SET status=? WHERE id=?", (status, eid))

        if status in ("done","no_show","cancelled"):
            c.execute("UPDATE barbers SET current_entry_id=NULL WHERE current_entry_id=?", (eid,))
            c.execute("UPDATE barbers SET on_break=0 WHERE current_entry_id IS NULL AND on_duty=1 AND on_break=1")
            dispatch_waiting_queue(c)
        return dict(row)

def call_next(barber_id):
    with db() as c:
        barber = c.execute("SELECT * FROM barbers WHERE id=?", (barber_id,)).fetchone()
        if not barber or not barber["on_duty"] or barber["on_break"] or barber["current_entry_id"]:
            raise ValueError("This barber is not available for a new customer.")
        waiting = c.execute("SELECT * FROM queue_entries WHERE status='waiting' ORDER BY created_at,rowid").fetchall()
        selected = next((e for e in waiting if not e["preferred_barber"] or e["preferred_barber"]==barber_id), None)
        if not selected: raise ValueError("No waiting customer is eligible for this barber.")
        ts = stamp()
        c.execute("UPDATE queue_entries SET status='in_chair', called_at=?, started_at=?, assigned_barber=? WHERE id=?", 
                  (ts, ts, barber_id, selected["id"]))
        c.execute("UPDATE barbers SET current_entry_id=? WHERE id=?", (selected["id"], barber_id))
        return selected["token"]

def barber_for_entry(eid):
    with db() as c:
        r = c.execute("SELECT name FROM barbers WHERE current_entry_id=?", (eid,)).fetchone()
        if r: return r["name"]
        r2 = c.execute("SELECT assigned_barber, preferred_barber FROM queue_entries WHERE id=?", (eid,)).fetchone()
        if r2:
            bid = r2["assigned_barber"] or r2["preferred_barber"]
            if bid:
                b = c.execute("SELECT name FROM barbers WHERE id=?", (bid,)).fetchone()
                if b: return b["name"]
        return "—"

def set_barber(bid, on_duty=None, on_break=None):
    with db() as c:
        b=c.execute("SELECT * FROM barbers WHERE id=?", (bid,)).fetchone()
        if not b: return
        if (on_duty is False or on_break is True) and b["current_entry_id"]:
            raise ValueError("Finish or resolve the current customer before changing this barber's availability.")
        if on_duty is not None: c.execute("UPDATE barbers SET on_duty=? WHERE id=?", (int(on_duty),bid))
        if on_break is not None: c.execute("UPDATE barbers SET on_break=? WHERE id=?", (int(on_break),bid))
        if (on_duty is True or on_break is False):
            dispatch_waiting_queue(c)

def fmt_wait(minutes):
    if minutes is None: return "—"
    if minutes < 1: return "Under 1 min"
    return f"{minutes} min"

def estimate(entry):
    queue = entries(["waiting","called","in_chair"], True)
    staff = barbers()
    active = [b for b in staff if b["on_duty"] and not b["on_break"]]
    if not active: return None
    workloads = {b["id"]: 0 for b in active}
    for b in active:
        if b["current_entry_id"]:
            cur = next((e for e in queue if e["id"]==b["current_entry_id"]), None)
            if cur:
                start_val = cur.get("started_at") or cur.get("called_at")
                workloads[b["id"]] += max(1, cur["duration"] - (int((now()-datetime.fromisoformat(start_val)).total_seconds()/60) if start_val else 0))
    target = entry["id"]
    for e in queue:
        if e["id"] == target: break
        if e["status"] == "waiting":
            eligible = [b for b in active if not e["preferred_barber"] or e["preferred_barber"]==b["id"]]
            if eligible:
                chosen=min(eligible,key=lambda b:workloads[b["id"]])
                workloads[chosen["id"]] += e["duration"]
    eligible = [b for b in active if not entry["preferred_barber"] or entry["preferred_barber"]==b["id"]]
    if not eligible: return None
    return max(0,min(workloads[b["id"]] for b in eligible))

def metric(label, value, sub=None):
    st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div>{f"<div class=small-muted>{sub}</div>" if sub else ""}</div>', unsafe_allow_html=True)

def page_header(title, subtitle):
    st.markdown(f'<div class="hero"><h1>{title}</h1><p>{subtitle}</p></div>', unsafe_allow_html=True)

def status_pill(status):
    return f'<span class="status status-{status}">{status.replace("_"," ").title()}</span>'

def queue_table(rows):
    if not rows:
        st.info("Nothing here yet.")
        return
    data=[]
    for e in rows:
        is_wait = e["status"] == "waiting"
        is_active = e["status"] in ("called", "in_chair")

        if is_wait:
            waited = fmt_timer_seconds(elapsed_seconds(e.get("created_at")))
            est = fmt_wait(estimate(e))
        elif is_active:
            started_sec = elapsed_seconds(e.get("started_at") or e.get("called_at") or e.get("created_at"))
            waited = f"In service ({fmt_timer_seconds(started_sec)} / {e['duration']}m)"
            est = "In service"
        else:
            waited = "—"
            est = "—"

        barber_name = barber_for_entry(e["id"])
        if barber_name == "—" and e.get("preferred_barber"):
            pref_b = next((b["name"] for b in staff if b["id"] == e["preferred_barber"]), e["preferred_barber"])
            barber_name = f"Pref: {pref_b}"
        elif barber_name == "—":
            barber_name = "Any free barber"

        data.append({
            "Token": e["token"],
            "Customer": e["customer_name"],
            "Service": e["service_name"],
            "Status": "In Chair" if e["status"] in ("called", "in_chair") else e["status"].replace("_"," ").title(),
            "Joined": e["created_at"][11:16],
            "Timer": waited,
            "Est. wait": est,
            "Barber": barber_name
        })
    st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)

# ---------- Navigation Setup ----------
PAGES = ["Overview", "Join Queue", "Reception", "Barber Desk", "Live Display", "Admin Settings", "Track Token"]

if "workspace_nav_radio" not in st.session_state:
    st.session_state["workspace_nav_radio"] = "Overview"

if "nav_page" in st.session_state:
    target = st.session_state.pop("nav_page")
    if target in PAGES:
        st.session_state["workspace_nav_radio"] = target

def set_workspace(name):
    st.session_state["workspace_nav_radio"] = name

def navigate_to(name):
    st.session_state["workspace_nav_radio"] = name
    st.rerun()

def track_token_action(token_eid):
    st.session_state["track_id"] = token_eid
    st.session_state["lookup_id"] = token_eid
    st.session_state["workspace_nav_radio"] = "Track Token"

with st.sidebar:
    st.markdown(f"## {t('title')}")
    st.caption(t('tagline'))
    page = st.radio("Workspace", PAGES, key="workspace_nav_radio", label_visibility="collapsed")
    st.divider()
    
    # Language Toggle (English / Gujarati)
    st.markdown("**Language / ભાષા**")
    st.radio("Lang", ["English", "ગુજરાતી"], key="lang_choice", horizontal=True, label_visibility="collapsed")
    
    st.divider()
    st.markdown(f"**{get_setting('salon_name','The Salon')}**")
    st.caption(f"Salon time · {now().strftime('%d %b %Y, %I:%M %p')}")
    st.caption("Prototype mode · SQLite storage")

all_today = entries(today_only=True)
waiting = [e for e in all_today if e["status"]=="waiting"]
serving = [e for e in all_today if e["status"] in ("called","in_chair")]
done = [e for e in all_today if e["status"]=="done"]
staff = barbers()
available = [b for b in staff if b["on_duty"] and not b["on_break"] and not b["current_entry_id"]]

# ---------- Overview ----------
if page == "Overview":
    page_header(t("hero_title"), t("hero_sub"))
    
    # 4 Primary Metrics
    c1,c2,c3,c4=st.columns(4)
    with c1: metric(t("waiting"), len(waiting), "Customers in queue")
    with c2: metric(t("in_service"), len(serving), "In chair now")
    with c3: metric(t("served_today"), len(done), "Completed appointments")
    with c4: metric(t("available_barbers"), len(available), f"of {len(staff)} team members")
    st.write("")
    
    # Main split: Live Queue on Left (70%), Team & Operational shortcuts on Right (30%)
    left, right = st.columns([1.5, 1])
    
    with left:
        # Contextual Action Bar right above the table
        t_col1, t_col2, t_col3 = st.columns([1.5, 1, 1])
        with t_col1:
            st.subheader(t("queue_right_now"))
        with t_col2:
            st.button(f"+ {t('add_customer')}", on_click=set_workspace, args=("Join Queue",), type="primary", use_container_width=True)
        with t_col3:
            if st.button(t("auto_assign"), use_container_width=True, help="Auto-assign waiting customers to free chairs"):
                dispatched = dispatch_waiting_queue()
                if dispatched:
                    st.success(f"Assigned {len(dispatched)} customer(s): " + ", ".join(f"{d['token']} -> {d['barber_name']}" for d in dispatched))
                else:
                    st.info("No customers eligible or no free barbers right now.")
                st.rerun()

        # Inline Quick Walk-in Form (Contextual above table)
        with st.expander(f"Quick walk-in registration form"):
            active_svcs = services(True)
            with st.form("overview_walkin", clear_on_submit=True):
                qw_name = st.text_input("Customer name")
                qw_phone = st.text_input("Mobile number (10 digits)")
                qw_map = {f'{s["name"]} · {s["minutes"]} min · ₹{s["price"]}': s["id"] for s in active_svcs}
                qw_chosen = st.multiselect("Services (max 3)", list(qw_map), max_selections=3)
                qw_pref = st.selectbox(t("preferred_barber"), [t("no_preference")] + [b["name"] for b in staff if b["on_duty"]])
                qw_submit = st.form_submit_button("Confirm walk-in", type="primary", use_container_width=True)
            if qw_submit:
                try:
                    pref_bid = next((b["id"] for b in staff if b["name"] == qw_pref), None)
                    s_ids = [qw_map[k] for k in qw_chosen]
                    token, _, assigned_barber = add_customer(qw_name, qw_phone, s_ids, pref_bid, "Walk-in")
                    if assigned_barber:
                        st.success(f"Walk-in added & service started with {assigned_barber}. Token: {token}")
                    else:
                        st.success(f"Walk-in added to queue. Token: {token}")
                    st.rerun()
                except Exception as ex:
                    st.error(str(ex))

        queue_table(waiting+serving)

    with right:
        st.subheader(t("team_availability"))
        for b in staff:
            state = "Serving" if b["current_entry_id"] else ("On break" if b["on_break"] else ("Available" if b["on_duty"] else "Off duty"))
            st.markdown(f'<div class="panel"><b>{b["name"]}</b><br><span class="small-muted">{state}</span></div>', unsafe_allow_html=True)
        
        st.write("")
        st.subheader("Workspace links")
        st.button(f"{t('reception_desk')} →", on_click=set_workspace, args=("Reception",), use_container_width=True)
        st.button(f"{t('barber_desk_title')} →", on_click=set_workspace, args=("Barber Desk",), use_container_width=True)
        st.button(f"{t('live_display')} ↗", on_click=set_workspace, args=("Live Display",), use_container_width=True)

# ---------- Join Queue ----------
elif page == "Join Queue":
    page_header(t("join_title"), t("join_sub"))
    open_online = get_setting("online_open","1")=="1"
    closing = get_setting("closing_time","21:00")
    cutoff = (datetime.combine(now().date(),time.fromisoformat(closing))-timedelta(minutes=30)).time()
    if now().time() >= cutoff: open_online=False
    
    if not open_online:
        st.warning("Online queue is currently closed (closes 30 minutes before closing time). Please contact reception for walk-in availability.")
    else:
        active_services=services(True)
        with st.form("join_form", clear_on_submit=False):
            name = st.text_input(t("your_name"), placeholder="e.g. John Doe")
            phone = st.text_input(t("mobile_number"), placeholder="10-digit mobile number")
            svc_map = {f'{s["name"]} · {s["minutes"]} min · ₹{s["price"]}': s["id"] for s in active_services}
            chosen_labels = st.multiselect(t("select_services"), list(svc_map), max_selections=3)
            
            # Live summary calculations directly inside the form above submit button
            if chosen_labels:
                chosen_svcs = [s for s in active_services if s["id"] in [svc_map[l] for l in chosen_labels]]
                total_m = sum(s["minutes"] for s in chosen_svcs)
                total_p = sum(s["price"] for s in chosen_svcs)
                st.markdown(f'<div class="summary-box"><b>Live Summary:</b> Total {total_m} min · ₹{total_p}</div>', unsafe_allow_html=True)
            
            pref = st.selectbox(t("preferred_barber"), [t("no_preference")] + [b["name"] for b in staff if b["on_duty"] and not b["on_break"]])
            submit = st.form_submit_button(t("get_token"), type="primary", use_container_width=True)
        
        if submit:
            try:
                pref_id = next((b["id"] for b in staff if b["name"]==pref), None)
                chosen_ids = [svc_map[l] for l in chosen_labels]
                token, eid, assigned_barber = add_customer(name, phone, chosen_ids, pref_id, "Online")
                st.session_state["new_token"] = (token, eid, assigned_barber)
            except Exception as ex: 
                err_msg = str(ex)
                st.error(err_msg)
                if "already has an active spot" in err_msg:
                    with db() as c:
                        active_row = c.execute("SELECT id FROM queue_entries WHERE phone=? AND status IN ('waiting','called','in_chair') AND date(created_at)=date(?)", ("".join(ch for ch in phone if ch.isdigit()), stamp()[:10])).fetchone()
                    if active_row:
                        st.button("View my active token", on_click=track_token_action, args=(active_row["id"],), type="primary")

        # Instant progressive transition to tracking screen
        if "new_token" in st.session_state:
            token, eid, assigned_barber = st.session_state["new_token"]
            st.divider()
            if assigned_barber:
                st.success(f"You're in! Assigned to {assigned_barber} — service and timer started.")
                st.markdown(f'<div class="panel"><div class="small-muted">ASSIGNED BARBER</div><div style="font-size:2rem;font-weight:800;color:#166534">{assigned_barber}</div><b>Please proceed directly to {assigned_barber}\'s chair.</b></div>', unsafe_allow_html=True)
            else:
                st.success("You're in the queue! We will call your token as soon as a chair opens.")
            
            st.markdown(f'<div class="panel"><div class="small-muted">YOUR TOKEN</div><div style="font-size:3.2rem;font-weight:800;color:#4a3fc5">{token}</div><b>Keep this token handy.</b></div>', unsafe_allow_html=True)
            
            # Direct tracking action
            st.button("Track live queue status now →", on_click=track_token_action, args=(eid,), type="primary", use_container_width=True)

# ---------- Reception ----------
elif page == "Reception":
    page_header(t("reception_title"), t("reception_sub"))
    
    # Top Metrics Bar
    a,b,c=st.columns(3)
    with a: metric(t("waiting"), len(waiting))
    with b: metric(t("in_service"), len(serving))
    with c: metric(t("available_barbers"), len(available))
    st.write("")

    # 2-Column Operational Grid (Tablet landscape optimized as in Doc 2 Screen 4)
    left_panel, right_panel = st.columns([1.1, 1.4])

    with left_panel:
        # Left Panel: Barber Chairs & Master Dispatch
        st.subheader("Barber chairs")
        if st.button("Auto-dispatch all waiting", use_container_width=True, type="primary", help="Automatically matches waiting customers with free barbers"):
            dispatched = dispatch_waiting_queue()
            if dispatched:
                st.success(f"Dispatched {len(dispatched)}: " + ", ".join(f"{d['token']} -> {d['barber_name']}" for d in dispatched))
            else:
                st.info("No eligible waiting customer or no free barbers.")
            st.rerun()

        for barber in staff:
            is_serving = bool(barber["current_entry_id"])
            card_class = "chair-card-serving" if is_serving else ("chair-card-break" if barber["on_break"] else "chair-card-available")
            state_text = "Serving" if is_serving else ("On break" if barber["on_break"] else ("Available" if barber["on_duty"] else "Off duty"))
            
            with st.container():
                st.markdown(f"""
                <div class="chair-card {card_class}">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <b>{barber['name']}</b>
                        <span class="status status-{'in_chair' if is_serving else ('waiting' if barber['on_break'] else 'done')}">{state_text}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if is_serving:
                    curr_entry = next((e for e in all_today if e["id"] == barber["current_entry_id"]), None)
                    if curr_entry:
                        s_time = elapsed_seconds(curr_entry.get("started_at") or curr_entry.get("called_at"))
                        st.caption(f"Customer: **{curr_entry['customer_name']}** ({curr_entry['token']}) · {curr_entry['service_name']}")
                        st.markdown(f"<span class='timer-pill timer-pill-calm'>In service: {fmt_timer_seconds(s_time)} / {curr_entry['duration']}m</span>", unsafe_allow_html=True)
                        b_col1, b_col2 = st.columns(2)
                        with b_col1:
                            if st.button("Complete", key=f"rec_done_{barber['id']}", use_container_width=True):
                                update_entry(curr_entry["id"], "done")
                                st.rerun()
                        with b_col2:
                            if st.button("No-show", key=f"rec_noshow_{barber['id']}", use_container_width=True):
                                update_entry(curr_entry["id"], "no_show")
                                st.rerun()
                elif barber["on_duty"] and not barber["on_break"]:
                    if st.button(f"Call next for {barber['name']}", key=f"call_{barber['id']}", use_container_width=True):
                        try:
                            tkn = call_next(barber['id'])
                            st.success(f"Called {tkn} for {barber['name']}")
                            st.rerun()
                        except Exception as ex:
                            st.error(str(ex))

    with right_panel:
        # Right Panel: Queue Management & Walk-in Intake
        w_top1, w_top2 = st.columns([1.2, 1])
        with w_top1:
            st.subheader(t("queue_right_now"))
        with w_top2:
            show_walkin = st.checkbox("+ Register walk-in", key="show_walkin_toggle")

        if show_walkin:
            with st.container(border=True):
                st.markdown("**Register Walk-in Customer**")
                active_services = services(True)
                with st.form("rec_walkin_form", clear_on_submit=True):
                    n = st.text_input("Customer name")
                    p = st.text_input("Mobile number")
                    sm = {f'{s["name"]} · {s["minutes"]} min · ₹{s["price"]}': s["id"] for s in active_services}
                    selected_labels = st.multiselect("Services (max 3)", list(sm), max_selections=3)
                    selected_ids = [sm[label] for label in selected_labels]
                    if selected_labels:
                        chosen_rows = [s for s in active_services if s["id"] in selected_ids]
                        st.caption(f"Combined duration: {sum(s['minutes'] for s in chosen_rows)} min · Total: ₹{sum(s['price'] for s in chosen_rows)}")
                    bp = st.selectbox(t("preferred_barber"), [t("no_preference")] + [b["name"] for b in staff if b["on_duty"]])
                    ok = st.form_submit_button("Add to queue", type="primary", use_container_width=True)
                if ok:
                    try:
                        bid = next((b["id"] for b in staff if b["name"]==bp), None)
                        token, _, asgn = add_customer(n, p, selected_ids, bid, "Walk-in")
                        if asgn:
                            st.success(f"Walk-in added & service started with {asgn}! Token: {token}")
                        else:
                            st.success(f"Walk-in added to queue. Token: {token}")
                        st.rerun()
                    except Exception as ex:
                        st.error(str(ex))

        # Waiting List Rows
        if not waiting:
            st.info("No customers currently waiting in queue.")
        else:
            for e in waiting:
                with st.container(border=True):
                    wx, wy, wz = st.columns([1, 2.5, 1.5])
                    wx.markdown(f"**{e['token']}**")
                    waited_sec = elapsed_seconds(e.get("created_at"))
                    wy.write(f"**{e['customer_name']}** · {e['service_name']}")
                    pref_text = e['preferred_barber'].title() if e.get('preferred_barber') else "Any free barber"
                    wy.markdown(f"{render_timer_badge(waited_sec)} &nbsp; <span class='small-muted'>Joined {e['created_at'][11:16]} · Pref: <b>{pref_text}</b></span>", unsafe_allow_html=True)
                    
                    with wz:
                        st.caption(f"Est: {fmt_wait(estimate(e))}")
                        z1, z2 = st.columns(2)
                        with z1:
                            if st.button("Call", key=f"callnow_{e['id']}", use_container_width=True):
                                with db() as conn:
                                    assigned, b_assigned = auto_assign_entry(conn, e["id"], e.get("preferred_barber"), fallback_to_any=True)
                                if assigned:
                                    st.success(f"Called to {b_assigned['name']}!")
                                else:
                                    st.warning("No chair free.")
                                st.rerun()
                        with z2:
                            if st.button("Cancel", key=f"cancel_{e['id']}", use_container_width=True):
                                update_entry(e["id"], "cancelled")
                                st.rerun()

# ---------- Barber desk ----------
elif page == "Barber Desk":
    page_header(t("barber_desk_title"), t("barber_desk_sub"))
    
    # Ergonomic top bar: Barber selector & break controls
    b_top1, b_top2 = st.columns([2, 1])
    with b_top1:
        selected = st.selectbox("Choose your station", [b["name"] for b in staff])
    
    barber = next(b for b in staff if b["name"]==selected)
    current = next((e for e in all_today if e["id"]==barber["current_entry_id"]), None)
    
    with b_top2:
        st.write("")
        st.write("")
        if barber["on_break"]:
            if st.button(t("end_break"), use_container_width=True, type="primary"):
                set_barber(barber["id"], on_break=False)
                st.rerun()
        else:
            if st.button(t("take_break"), use_container_width=True, disabled=bool(current)):
                try: 
                    set_barber(barber["id"], on_break=True)
                    st.rerun()
                except Exception as ex: 
                    st.error(str(ex))

    # Active Customer Hero Card (Mobile thumb-zone layout)
    if current:
        s_elapsed = elapsed_seconds(current.get("started_at") or current.get("called_at") or current.get("created_at"))
        st.markdown(f"""
        <div class="panel" style="border-left: 4px solid #166534; padding:1.4rem;">
            <div class="small-muted">CURRENT CUSTOMER · CHAIR ACTIVE</div>
            <h1 style="margin:0.2rem 0; font-size:2.4rem;">{current['customer_name']}</h1>
            <div style="font-size:1.1rem; color:#475569; margin-bottom:0.6rem;">{current['service_name']} · {current['duration']} min · ₹{current['price']}</div>
            <span class="timer-pill timer-pill-calm" style="font-size:0.9rem;">In service: {fmt_timer_seconds(s_elapsed)} / {current['duration']} min</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Primary Dominant Action Button (Full-width 48px target)
        if st.button(t("complete_service"), type="primary", use_container_width=True):
            update_entry(current["id"], "done")
            st.success("Service completed.")
            st.rerun()
        
        # Subtle secondary option below
        col_sub1, col_sub2 = st.columns([2, 1])
        with col_sub2:
            if st.button("Mark no-show / cancel", use_container_width=True):
                update_entry(current["id"], "no_show")
                st.rerun()
    else:
        st.info("Chair is currently available. When free, eligible waiting customers will automatically be assigned here.")
        if barber["on_duty"] and not barber["on_break"]:
            if st.button(t("call_next"), type="primary", use_container_width=True):
                try:
                    tkn = call_next(barber["id"])
                    st.success(f"Called {tkn} — service started.")
                    st.rerun()
                except Exception as ex:
                    st.error(str(ex))

    st.write("")
    st.subheader("Next eligible customers for your chair")
    eligible = [e for e in waiting if not e["preferred_barber"] or e["preferred_barber"]==barber["id"]]
    queue_table(eligible[:5])

# ---------- Live Display ----------
elif page == "Live Display":
    page_header(t("display_title"), t("display_sub"))
    
    @st.fragment(run_every="5s")
    def render_live_display():
        today_data = entries(today_only=True)
        live_waiting = [e for e in today_data if e["status"]=="waiting"]
        live_serving = [e for e in today_data if e["status"] in ("called","in_chair")]
        
        if live_serving:
            cols = st.columns(min(3, max(1, len(live_serving))))
            for i,e in enumerate(live_serving):
                with cols[i]:
                    serv_sec = elapsed_seconds(e.get("started_at") or e.get("called_at") or e.get("created_at"))
                    st.markdown(f'<div class="panel" style="text-align:center;padding:1.7rem"><div class="small-muted">NOW SERVING</div><div style="font-size:2.8rem;font-weight:800;color:#4a3fc5">{e["token"]}</div><h3>{barber_for_entry(e["id"])}</h3><div class="small-muted">In service: {fmt_timer_seconds(serv_sec)} / {e["duration"]}m</div></div>',unsafe_allow_html=True)
        else:
            st.info("No customers are being served right now.")
        
        st.subheader("Up next in queue")
        if not live_waiting:
            st.info("No customers waiting right now.")
        else:
            for e in live_waiting[:6]:
                w_sec = elapsed_seconds(e.get("created_at"))
                est_m = estimate(e)
                st.markdown(f'<div class="panel"><span class="token">{e["token"]}</span> &nbsp; <b>{e["customer_name"]}</b> &nbsp; {render_timer_badge(w_sec)} <span style="float:right;color:#777">{e["service_name"]} · Est: {fmt_wait(est_m)}</span></div>',unsafe_allow_html=True)

    render_live_display()
    st.caption("Live digital display automatically synchronizes every 5 seconds.")

    # Waiting Lounge Ambience (Deluxe Saloon Radio)
    st.divider()
    lounge_col_left, lounge_col_right = st.columns([3, 1])
    with lounge_col_left:
        st.subheader(t("lounge_radio_title"))
        st.caption(t("lounge_radio_sub"))
    with lounge_col_right:
        st.write("")
        st.caption("Floating player active at bottom right.")

# ---------- Admin ----------
elif page == "Admin Settings":
    page_header(t("admin_title"), t("admin_sub"))
    
    # Unified Salon Hours Section
    with st.container(border=True):
        st.markdown("**Salon Operating Hours**")
        salon = st.text_input("Salon name", get_setting("salon_name","The Salon"))
        c_time_col1, c_time_col2 = st.columns(2)
        with c_time_col1:
            closing = st.time_input("Closing time", time.fromisoformat(get_setting("closing_time","21:00")))
        with c_time_col2:
            st.write("")
            st.write("")
            online = st.toggle("Accept online queue entries", get_setting("online_open","1")=="1")
        if st.button("Save operating settings", type="primary"):
            set_setting("salon_name", salon)
            set_setting("closing_time", closing.strftime("%H:%M"))
            set_setting("online_open", "1" if online else "0")
            st.success("Operating settings saved.")
    
    st.write("")
    # Unified Batch Service Catalogue Management (No per-row save buttons)
    with st.container(border=True):
        st.markdown("**Services Catalogue**")
        all_svcs = services()
        edited_services = []
        for s in all_svcs:
            c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
            nm = c1.text_input("Name", s["name"], key=f"asn_{s['id']}")
            mins = c2.number_input("Minutes", 10, 240, s["minutes"], 5, key=f"asm_{s['id']}")
            price = c3.number_input("Price (₹)", 0, 10000, s["price"], 50, key=f"asp_{s['id']}")
            active = c4.toggle("Active", bool(s["active"]), key=f"asa_{s['id']}")
            edited_services.append((s["id"], nm, int(mins), int(price), active))
        
        # Single Unified Save Button for all services
        if st.button(t("save_services"), type="primary", use_container_width=True):
            with db() as c:
                for sid, nm, mins, price, active in edited_services:
                    c.execute("UPDATE services SET name=?, minutes=?, price=?, active=? WHERE id=?", 
                              (nm, mins, price, int(active), sid))
            st.success("All service changes saved successfully.")
            st.rerun()

    st.write("")
    # Unified Team Roster Management
    with st.container(border=True):
        st.markdown("**Team Roster & Duty Availability**")
        all_barbers = barbers()
        duty_changes = []
        for b in all_barbers:
            c1, c2, c3 = st.columns([2, 1.5, 1])
            c1.markdown(f"**{b['name']}**")
            c2.write("Serving" if b["current_entry_id"] else ("On break" if b["on_break"] else ("On duty" if b["on_duty"] else "Off duty")))
            duty = c3.toggle("On duty", bool(b["on_duty"]), key=f"aduty_{b['id']}")
            duty_changes.append((b["id"], duty))
        
        if st.button("Apply team changes", type="primary", use_container_width=True):
            try:
                for bid, duty in duty_changes:
                    set_barber(bid, on_duty=duty)
                st.success("Team roster updated.")
                st.rerun()
            except Exception as ex:
                st.error(str(ex))

    st.write("")
    # Today's Activity & Export
    st.subheader("Today's activity summary")
    d1, d2, d3 = st.columns(3)
    d1.metric("Joined", len(all_today))
    d2.metric("Completed", len(done))
    d3.metric("No-shows", sum(e["status"]=="no_show" for e in all_today))
    st.download_button("Download today's queue CSV", pd.DataFrame(all_today).to_csv(index=False).encode("utf-8"), file_name=f"salon-queue-{now().date()}.csv", mime="text/csv", use_container_width=True)

# ---------- Track Token ----------
elif page == "Track Token":
    page_header(t("track_title"), t("track_sub"))
    
    col_in1, col_in2 = st.columns([3, 1])
    with col_in1:
        eid = st.text_input("Enter your tracking ID", value=st.session_state.get("track_id",""), placeholder="Paste the tracking ID shown after joining")
    with col_in2:
        st.write("")
        st.write("")
        if st.button("Check status", type="primary", use_container_width=True):
            st.session_state["lookup_id"] = eid.strip()
    
    if st.session_state.get("lookup_id"):
        @st.fragment(run_every="5s")
        def render_track_status(lookup_eid):
            with db() as c:
                row = c.execute("SELECT * FROM queue_entries WHERE id=?", (lookup_eid,)).fetchone()
            if not row:
                st.error("We couldn't find that tracking ID.")
                return
            
            e = dict(row)
            st.markdown(f'<div class="panel"><div class="small-muted">TOKEN</div><div style="font-size:3rem;font-weight:800;color:#4a3fc5">{e["token"]}</div><h2>{e["customer_name"]}</h2>{status_pill("in_chair" if e["status"] in ("called","in_chair") else e["status"])}</div>', unsafe_allow_html=True)
            
            if e["status"]=="waiting":
                current_waiting = [x for x in entries(today_only=True) if x["status"]=="waiting"]
                pos = sum(1 for x in current_waiting if x["created_at"]<=e["created_at"])
                est_m = estimate(e)
                w_sec = elapsed_seconds(e.get("created_at"))
                
                # 2nd in line alert banner (Doc 2 Screen 3)
                if pos == 2:
                    st.markdown(f'<div class="alert-box-warn">{t("start_coming")}</div>', unsafe_allow_html=True)
                
                # Live Interactive Browser Clock
                components.html(render_live_clock_html(w_sec, est_m, e["token"], e["customer_name"]), height=180)
                
                t1, t2, t3 = st.columns(3)
                with t1: st.metric(t("people_ahead"), max(0, pos-1))
                with t2: st.metric(t("est_wait"), fmt_wait(est_m))
                with t3: st.metric(t("elapsed_wait"), fmt_timer_seconds(w_sec))
                
                barber_pref = e.get("preferred_barber")
                if barber_pref:
                    b_name = next((b["name"] for b in staff if b["id"] == barber_pref), barber_pref)
                    st.info(f"Preferred barber: {b_name}. You will be assigned as soon as {b_name} is free.")
                else:
                    st.info("No preferred barber selected. You will be automatically assigned to the first free barber.")
                
                # Safe Destructive Cancellation Area at the bottom
                st.write("")
                with st.expander(t("cancel_spot")):
                    st.warning("Are you sure you want to cancel your spot in the queue?")
                    if st.button(t("confirm_cancel"), type="primary"):
                        update_entry(e["id"], "cancelled")
                        st.success("Your spot in the queue has been cancelled.")
                        st.rerun()

            elif e["status"] in ("called", "in_chair"):
                assigned_to = barber_for_entry(e["id"])
                s_sec = elapsed_seconds(e.get("started_at") or e.get("called_at") or e.get("created_at"))
                
                # Live Interactive Service Clock
                components.html(render_service_clock_html(s_sec, e["duration"], e["token"], e["customer_name"], assigned_to), height=180)
                
                st.success(f"Service in progress with **{assigned_to}**.")
                st.markdown(f"<div class='panel'><b>Time in chair:</b> <span class='timer-pill timer-pill-calm'>{fmt_timer_seconds(s_sec)}</span> / {e['duration']} min<br><span class='small-muted'>Service and timer started automatically.</span></div>", unsafe_allow_html=True)

            elif e["status"]=="done": 
                st.success("Your service is complete. Thank you for visiting.")
            elif e["status"]=="no_show": 
                st.warning("This token was marked as a no-show.")
            else: 
                st.info("This token is no longer active.")

        render_track_status(st.session_state["lookup_id"])

# ---------- Floating Rotating Vinyl Radio Pill (saloon.wtf) ----------
st.markdown("""
<div id="saloon-audio-anchor"></div>
<style>
div:has(#saloon-audio-anchor) + div iframe {
    position: fixed !important;
    bottom: 24px !important;
    right: 24px !important;
    width: 360px !important;
    height: 68px !important;
    z-index: 999999 !important;
    border: none !important;
    background: transparent !important;
    box-shadow: none !important;
}
@media (max-width: 480px) {
    div:has(#saloon-audio-anchor) + div iframe {
        width: calc(100vw - 32px) !important;
        right: 16px !important;
        bottom: 16px !important;
    }
}
</style>
""", unsafe_allow_html=True)

_player_html_file = APP_DIR / "floating_player.html"
if _player_html_file.exists():
    with open(_player_html_file, "r", encoding="utf-8") as _pf:
        _player_html = _pf.read()
else:
    _player_html = "<div>Saloon Radio</div>"

components.html(_player_html, height=68)

st.markdown("<div style='text-align:center;color:#9aa0af;padding-top:2rem;font-size:.8rem'>SALON QUEUE · Built with Python + Streamlit</div>",unsafe_allow_html=True)
