"""
SpellForge — a spelling practice app for adults who read but struggle to spell.

Run locally:
    pip install streamlit
    streamlit run spellforge.py

Deploy free to web (so you can use it on your phone):
    1. Push this file + requirements.txt to a GitHub repo
    2. Go to https://share.streamlit.io
    3. Connect the repo, click Deploy
    4. You get a public URL. Open it in Safari on your iPhone,
       tap Share > "Add to Home Screen" — now it's an app icon.
"""

import streamlit as st
import streamlit.components.v1 as components
import random
import json
from datetime import datetime

# ==============================================================================
# PAGE CONFIG — must be first Streamlit call
# ==============================================================================
st.set_page_config(
    page_title="SpellForge",
    page_icon="⚒",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ==============================================================================
# WORD BANK
# Three categories × three difficulty tiers.
# Each word: syllables, hint (meaning), mnemonic (memory trick), common_error.
# ==============================================================================

WORD_BANK = {
    "everyday": {
        "easy": [
            {"word": "friend", "syllables": ["friend"], "hint": "someone you know and like", "mnemonic": "Fri + END — your week ENDs with a friend", "common_error": "freind"},
            {"word": "because", "syllables": ["be", "cause"], "hint": "it tells you why", "mnemonic": "Big Elephants Can Always Understand Small Elephants", "common_error": "becuase"},
            {"word": "weird", "syllables": ["weird"], "hint": "strange, unusual", "mnemonic": "weird breaks the i-before-e rule — WE are weird together", "common_error": "wierd"},
            {"word": "believe", "syllables": ["be", "lieve"], "hint": "to think something is true", "mnemonic": "there's a LIE in beLIEve", "common_error": "belive"},
            {"word": "receive", "syllables": ["re", "ceive"], "hint": "to get something", "mnemonic": "i before e EXCEPT after c — reCEIVE", "common_error": "recieve"},
            {"word": "tomorrow", "syllables": ["to", "mor", "row"], "hint": "the day after today", "mnemonic": "two R's in TOMORROW — like two sunrises", "common_error": "tommorow"},
            {"word": "until", "syllables": ["un", "til"], "hint": "up to the time that", "mnemonic": "only ONE L — un + til", "common_error": "untill"},
            {"word": "beginning", "syllables": ["be", "gin", "ning"], "hint": "the start", "mnemonic": "double the N when you add -ING to beGIN", "common_error": "begining"},
        ],
        "medium": [
            {"word": "definitely", "syllables": ["def", "i", "nite", "ly"], "hint": "for sure, 100%", "mnemonic": "defiNITEly has NITE in it — not defin-ATE-ly", "common_error": "definately"},
            {"word": "separate", "syllables": ["sep", "a", "rate"], "hint": "to pull apart, divided", "mnemonic": "there's A RAT in sepARATe", "common_error": "seperate"},
            {"word": "embarrassed", "syllables": ["em", "bar", "rassed"], "hint": "feeling awkward or ashamed", "mnemonic": "two R's, two S's — Really Red, Super Shy", "common_error": "embarassed"},
            {"word": "necessary", "syllables": ["nec", "es", "sar", "y"], "hint": "needed, required", "mnemonic": "one Collar, two Socks (1 C, 2 S's)", "common_error": "neccessary"},
            {"word": "achievement", "syllables": ["a", "chieve", "ment"], "hint": "a success or accomplishment", "mnemonic": "i before e — aCHIEVE", "common_error": "acheivement"},
            {"word": "argument", "syllables": ["ar", "gu", "ment"], "hint": "a disagreement or debate", "mnemonic": "I lost an E in the argument", "common_error": "arguement"},
            {"word": "existence", "syllables": ["ex", "is", "tence"], "hint": "the state of being", "mnemonic": "ends in -ENCE not -ANCE", "common_error": "existance"},
            {"word": "occasion", "syllables": ["oc", "ca", "sion"], "hint": "a special event or time", "mnemonic": "two C's, one S — an ocCASion is a BIG deal", "common_error": "ocassion"},
        ],
        "hard": [
            {"word": "rhythm", "syllables": ["rhy", "thm"], "hint": "a regular beat or pattern", "mnemonic": "Rhythm Helps Your Two Hips Move — Y is the only vowel", "common_error": "rythm"},
            {"word": "conscience", "syllables": ["con", "science"], "hint": "your inner moral sense", "mnemonic": "con + SCIENCE — the science of right and wrong", "common_error": "conscence"},
            {"word": "acquiesce", "syllables": ["ac", "qui", "esce"], "hint": "to reluctantly agree", "mnemonic": "AC + QUI + ESCE — the CQ together is rare", "common_error": "aquiesce"},
            {"word": "chrysanthemum", "syllables": ["chry", "san", "the", "mum"], "hint": "a type of flower", "mnemonic": "CHRY + SAN + THE + MUM — Greek roots: gold flower", "common_error": "chrysantemum"},
            {"word": "onomatopoeia", "syllables": ["on", "o", "ma", "to", "poe", "ia"], "hint": "words that sound like what they mean (buzz, hiss)", "mnemonic": "Old Nuns On Mopeds Are Tall, Often Pregnant, Often Eating Ice-cream Alone", "common_error": "onomatopeia"},
            {"word": "supersede", "syllables": ["su", "per", "sede"], "hint": "to replace or take the place of", "mnemonic": "the only -SEDE word in English — all others use -CEDE or -CEED", "common_error": "supercede"},
        ],
    },
    "professional": {
        "easy": [
            {"word": "business", "syllables": ["busi", "ness"], "hint": "a commercial activity or company", "mnemonic": "busi + NESS — full of BUSY-ness", "common_error": "buisness"},
            {"word": "schedule", "syllables": ["sched", "ule"], "hint": "a plan of timed events", "mnemonic": "SCH at the start — like SCHool", "common_error": "schedual"},
            {"word": "career", "syllables": ["ca", "reer"], "hint": "a long-term profession", "mnemonic": "two R's, two E's — a long road", "common_error": "carreer"},
            {"word": "colleague", "syllables": ["col", "league"], "hint": "a work partner", "mnemonic": "col + LEAGUE — you're in the same league", "common_error": "collegue"},
            {"word": "benefit", "syllables": ["ben", "e", "fit"], "hint": "a helpful perk or advantage", "mnemonic": "one N, one F — a slim benefit", "common_error": "benifit"},
        ],
        "medium": [
            {"word": "accommodate", "syllables": ["ac", "com", "mo", "date"], "hint": "to make room for", "mnemonic": "two C's AND two M's — room for everyone", "common_error": "accomodate"},
            {"word": "maintenance", "syllables": ["main", "ten", "ance"], "hint": "keeping things running", "mnemonic": "mainTENance has TEN in it, not TAIN", "common_error": "maintainance"},
            {"word": "questionnaire", "syllables": ["ques", "tion", "naire"], "hint": "a survey", "mnemonic": "double N before AIRE — French import", "common_error": "questionaire"},
            {"word": "occurrence", "syllables": ["oc", "cur", "rence"], "hint": "something that happens", "mnemonic": "two C's, two R's — it occurred twice", "common_error": "occurence"},
            {"word": "liaison", "syllables": ["li", "ai", "son"], "hint": "a person who connects two groups", "mnemonic": "LI-AI-SON — three vowel clusters in a row", "common_error": "liason"},
            {"word": "privilege", "syllables": ["priv", "i", "lege"], "hint": "a special right or advantage", "mnemonic": "priv + i + LEGE — no D anywhere", "common_error": "priviledge"},
            {"word": "recommend", "syllables": ["rec", "om", "mend"], "hint": "to suggest as good", "mnemonic": "one C, two M's — I reComMend", "common_error": "reccomend"},
        ],
        "hard": [
            {"word": "bureaucracy", "syllables": ["bu", "reau", "cra", "cy"], "hint": "government or corporate red tape", "mnemonic": "BU-REAU (French) + CRACY — rule by desks", "common_error": "beaurocracy"},
            {"word": "entrepreneur", "syllables": ["en", "tre", "pre", "neur"], "hint": "someone who starts a business", "mnemonic": "French word — ends in NEUR not NUER", "common_error": "entreprenuer"},
            {"word": "consensus", "syllables": ["con", "sen", "sus"], "hint": "general agreement among a group", "mnemonic": "CON + SENSUS — common sense", "common_error": "concensus"},
            {"word": "conscientious", "syllables": ["con", "scien", "tious"], "hint": "careful and diligent", "mnemonic": "CON + SCIENCE + TIOUS — guided by conscience", "common_error": "conscientous"},
            {"word": "itinerary", "syllables": ["i", "tin", "er", "ar", "y"], "hint": "a travel plan", "mnemonic": "I + TIN + ER + ARY — five parts, like five stops", "common_error": "itenerary"},
        ],
    },
    "trending": {
        "easy": [
            {"word": "rizz", "syllables": ["rizz"], "hint": "charisma, flirting skill (2024+ slang)", "mnemonic": "cha-RIZZ-ma, two Z's", "common_error": "riz"},
            {"word": "cringe", "syllables": ["cringe"], "hint": "secondhand embarrassment", "mnemonic": "crin + GE — G sounds like J here", "common_error": "crindge"},
            {"word": "vibe", "syllables": ["vibe"], "hint": "an atmosphere or feeling", "mnemonic": "V-I-B-E — four letters, one vibe", "common_error": "viebe"},
            {"word": "slay", "syllables": ["slay"], "hint": "to do something exceptionally well", "mnemonic": "S-L-A-Y — four letters, total win", "common_error": "slae"},
        ],
        "medium": [
            {"word": "aesthetic", "syllables": ["aes", "thet", "ic"], "hint": "a visual style or vibe", "mnemonic": "starts with AE — Artistic Energy", "common_error": "asthetic"},
            {"word": "delulu", "syllables": ["de", "lu", "lu"], "hint": "playfully delusional (social media)", "mnemonic": "de + LU + LU, LU twice like seeing double", "common_error": "delooloo"},
            {"word": "brainrot", "syllables": ["brain", "rot"], "hint": "the feeling after too much scrolling", "mnemonic": "BRAIN + ROT, one word", "common_error": "brain-rot"},
            {"word": "crashout", "syllables": ["crash", "out"], "hint": "a dramatic meltdown", "mnemonic": "CRASH + OUT, one word", "common_error": "crash-out"},
            {"word": "synergize", "syllables": ["syn", "er", "gize"], "hint": "corporate: combine forces", "mnemonic": "syn (together) + ergy + ize", "common_error": "synergyze"},
            {"word": "leverage", "syllables": ["lev", "er", "age"], "hint": "to use as an advantage", "mnemonic": "LEVER + AGE — use the lever", "common_error": "leverege"},
        ],
        "hard": [
            {"word": "millennial", "syllables": ["mil", "len", "ni", "al"], "hint": "generation born ~1981–1996", "mnemonic": "two L's, two N's — millennium = 1000 years", "common_error": "millenial"},
            {"word": "influencer", "syllables": ["in", "flu", "en", "cer"], "hint": "someone with a social media following", "mnemonic": "IN + FLU + EN + CER — four parts", "common_error": "influencier"},
            {"word": "algorithm", "syllables": ["al", "go", "rithm"], "hint": "a set of rules a computer follows", "mnemonic": "AL + GO + RITHM (like RHYTHM minus H)", "common_error": "algoritm"},
        ],
    },
}

# ==============================================================================
# HELPERS
# ==============================================================================

VOWELS = set("aeiouAEIOU")

def get_filtered_bank(categories, difficulties):
    """Return flat list of word dicts matching selected filters."""
    words = []
    for cat in categories:
        for diff in difficulties:
            words.extend(WORD_BANK.get(cat, {}).get(diff, []))
    return words

def analyze_error(correct, attempt):
    """Return a dict describing how the attempt differs from the correct word."""
    if not attempt:
        return None
    c = correct.lower()
    a = attempt.lower()
    if c == a:
        return None
    # Missing letter
    if len(a) < len(c):
        for i in range(len(c) + 1):
            if c[:i] + c[i+1:] == a:
                return {"type": "missing_letter", "letter": c[i] if i < len(c) else ""}
        return {"type": "too_short"}
    # Extra letter
    if len(a) > len(c):
        for i in range(len(a) + 1):
            if a[:i] + a[i+1:] == c:
                return {"type": "extra_letter", "letter": a[i] if i < len(a) else ""}
        return {"type": "too_long"}
    # Swapped letters
    for i in range(len(c) - 1):
        if c[i] != a[i] and c[i+1] != a[i+1] and c[i] == a[i+1] and c[i+1] == a[i]:
            return {"type": "swapped_letters", "letters": [c[i], c[i+1]]}
    # Wrong letter
    for i in range(len(c)):
        if c[i] != a[i]:
            return {"type": "wrong_letter", "expected": c[i], "got": a[i]}
    return {"type": "unknown"}

def error_description(err):
    if not err:
        return ""
    t = err["type"]
    if t == "missing_letter":
        return f"You dropped the letter \"{err['letter']}\""
    if t == "extra_letter":
        return f"You added an extra \"{err['letter']}\""
    if t == "swapped_letters":
        return f"You swapped \"{err['letters'][0]}\" and \"{err['letters'][1]}\""
    if t == "wrong_letter":
        return f"You wrote \"{err['got']}\" where \"{err['expected']}\" belongs"
    if t == "too_short":
        return "Your answer is too short"
    if t == "too_long":
        return "Your answer has too many letters"
    return "Close, but not quite"

def render_phonetic_html(word, accent="#0D8F7F"):
    """Return HTML where vowels are colored/underlined, consonants are plain."""
    chunks = []
    for ch in word:
        if ch in VOWELS:
            chunks.append(
                f'<span style="color:{accent};font-weight:800;border-bottom:3px solid {accent};padding-bottom:2px;">{ch}</span>'
            )
        else:
            chunks.append(f'<span style="color:#1a1a1a;font-weight:700;">{ch}</span>')
    return (
        f'<div style="font-size:2.4rem;letter-spacing:0.05em;text-align:center;'
        f'font-family:Georgia,serif;margin:0.5rem 0 0.3rem 0;">{"".join(chunks)}</div>'
        f'<div style="font-size:0.7rem;text-align:center;color:#888;letter-spacing:0.1em;'
        f'text-transform:uppercase;">vowels underlined · consonants plain</div>'
    )

def tts_component(text, label="▶ Hear the word", rate=1.0, key=None):
    """
    Embedded HTML button that uses the browser's built-in speech synthesis.
    Works on iPhone Safari without autoplay issues because it's user-initiated.
    """
    safe_text = text.replace('"', '\\"').replace("'", "\\'")
    safe_label = label.replace('"', '&quot;')
    html = f"""
    <div style="text-align:center;margin:0.3rem 0;">
      <button
        onclick="
          window.speechSynthesis.cancel();
          var u = new SpeechSynthesisUtterance('{safe_text}');
          u.rate = {rate};
          u.pitch = 1.0;
          window.speechSynthesis.speak(u);
        "
        style="
          background:#0D8F7F;color:white;border:none;padding:12px 24px;
          border-radius:999px;font-size:15px;font-weight:700;cursor:pointer;
          box-shadow:0 4px 14px rgba(13,143,127,0.3);
          font-family:-apple-system,system-ui,sans-serif;
          transition:transform 0.1s;
        "
        onmousedown="this.style.transform='scale(0.96)';"
        onmouseup="this.style.transform='scale(1)';"
        ontouchstart="this.style.transform='scale(0.96)';"
        ontouchend="this.style.transform='scale(1)';"
      >{safe_label}</button>
    </div>
    """
    components.html(html, height=65)

def tts_syllables_component(syllables, key=None):
    """Button that speaks each syllable with a pause between them."""
    syl_json = json.dumps(syllables)
    html = f"""
    <div style="text-align:center;margin:0.3rem 0;">
      <button
        onclick="
          var syls = {syl_json};
          window.speechSynthesis.cancel();
          syls.forEach(function(s, i) {{
            setTimeout(function() {{
              var u = new SpeechSynthesisUtterance(s);
              u.rate = 0.65;
              window.speechSynthesis.speak(u);
            }}, i * 700);
          }});
        "
        style="
          background:#fef3c7;color:#92400e;border:1.5px solid #fde68a;padding:8px 18px;
          border-radius:999px;font-size:13px;font-weight:700;cursor:pointer;
          font-family:-apple-system,system-ui,sans-serif;
        "
      >▶ Sound out syllable by syllable</button>
    </div>
    """
    components.html(html, height=55)

def syllable_pills_html(syllables, accent="#0D8F7F"):
    """Render syllables as pill-style tiles separated by a visual dot."""
    pieces = []
    for i, syl in enumerate(syllables):
        pieces.append(
            f'<span style="display:inline-block;background:{accent}15;color:{accent};'
            f'border:1.5px solid {accent}40;padding:6px 14px;border-radius:10px;'
            f'font-weight:700;font-size:1.05rem;margin:3px;">{syl}</span>'
        )
        if i < len(syllables) - 1:
            pieces.append(
                '<span style="color:#ccc;font-size:1.4rem;margin:0 2px;vertical-align:middle;">·</span>'
            )
    return (
        f'<div style="text-align:center;line-height:2.2;margin:0.5rem 0;">{"".join(pieces)}</div>'
    )

# ==============================================================================
# SESSION STATE — persists across Streamlit reruns within a session
# ==============================================================================

def init_state():
    defaults = {
        "screen": "home",
        "categories": ["everyday", "professional"],
        "difficulties": ["easy", "medium"],
        "game_mode": "dictation",
        "current_word": None,
        "attempt": "",
        "feedback": None,   # None | "correct" | "wrong"
        "error_info": None,
        "show_hint": False,
        "streak": 0,
        "best_streak": 0,
        "xp": 0,
        "total_correct": 0,
        "total_attempts": 0,
        "error_history": [],
        "mastered": set(),
        "session_seen": set(),
        "recent_errors": [],  # list of recently-missed words for spaced repetition
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ==============================================================================
# CORE GAME LOGIC
# ==============================================================================

def pick_new_word():
    bank = get_filtered_bank(st.session_state.categories, st.session_state.difficulties)
    if not bank:
        return None
    # 50% chance: serve a recent error
    recent = [w for w in st.session_state.recent_errors[-8:] if any(b["word"] == w for b in bank)]
    if recent and random.random() < 0.5:
        target = random.choice(recent)
        return next(b for b in bank if b["word"] == target)
    # Else prefer unseen, unmastered
    unseen = [b for b in bank if b["word"] not in st.session_state.mastered
              and b["word"] not in st.session_state.session_seen]
    if unseen:
        return random.choice(unseen)
    unmastered = [b for b in bank if b["word"] not in st.session_state.mastered]
    if unmastered:
        return random.choice(unmastered)
    return random.choice(bank)

def start_round():
    w = pick_new_word()
    if w is None:
        st.session_state.screen = "home"
        st.warning("No words match your filters. Pick at least one category and difficulty.")
        return
    st.session_state.current_word = w
    st.session_state.attempt = ""
    st.session_state.feedback = None
    st.session_state.error_info = None
    st.session_state.show_hint = False
    st.session_state.session_seen.add(w["word"])
    st.session_state.screen = "play"

def submit_attempt():
    w = st.session_state.current_word
    if not w:
        return
    guess = st.session_state.attempt.strip().lower()
    if not guess:
        return
    correct = w["word"].lower()
    st.session_state.total_attempts += 1
    if guess == correct:
        st.session_state.feedback = "correct"
        gained = 10 + st.session_state.streak * 2
        st.session_state.xp += gained
        st.session_state.streak += 1
        st.session_state.best_streak = max(st.session_state.best_streak, st.session_state.streak)
        st.session_state.total_correct += 1
        # Mark mastered if no recent errors for this word
        recent_misses = sum(1 for e in st.session_state.error_history[-15:] if e["word"] == correct)
        if recent_misses == 0:
            st.session_state.mastered.add(correct)
    else:
        st.session_state.feedback = "wrong"
        err = analyze_error(correct, guess)
        st.session_state.error_info = err
        st.session_state.streak = 0
        st.session_state.error_history.append({
            "word": correct,
            "attempt": guess,
            "error_type": err["type"] if err else "unknown",
            "timestamp": datetime.now().isoformat(),
        })
        st.session_state.recent_errors.append(correct)
        if len(st.session_state.recent_errors) > 20:
            st.session_state.recent_errors = st.session_state.recent_errors[-20:]

# ==============================================================================
# UI — GLOBAL STYLES
# ==============================================================================

st.markdown("""
<style>
  .stApp { background: #fafaf7; }
  .block-container { padding-top: 1.5rem; padding-bottom: 3rem; max-width: 640px; }
  /* Bigger, more tappable input for mobile */
  .stTextInput input {
    font-size: 1.3rem !important;
    font-weight: 700 !important;
    text-align: center !important;
    padding: 14px !important;
    border-radius: 14px !important;
    letter-spacing: 0.05em !important;
  }
  /* Tappable buttons */
  .stButton button {
    font-weight: 700 !important;
    border-radius: 12px !important;
    padding: 10px 18px !important;
    font-size: 0.95rem !important;
  }
  /* Hide Streamlit footer/menu for cleaner app feel */
  #MainMenu { visibility: hidden; }
  footer { visibility: hidden; }
  header { visibility: hidden; }
  /* Level/streak chips */
  .chip {
    display: inline-block;
    padding: 6px 14px;
    border-radius: 999px;
    font-weight: 700;
    font-size: 0.85rem;
    margin-right: 6px;
  }
  .chip-streak { background: #fff7ed; color: #c2410c; border: 1px solid #fed7aa; }
  .chip-level { background: #ecfdf5; color: #0D8F7F; border: 1px solid #a7f3d0; }
  h1.logo {
    font-family: Georgia, serif;
    font-weight: 900;
    letter-spacing: -0.02em;
    margin: 0;
    color: #1a1a1a;
  }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# SCREEN: HOME
# ==============================================================================

def screen_home():
    col_title, col_stats = st.columns([3, 2])
    with col_title:
        st.markdown('<h1 class="logo">SpellForge</h1>', unsafe_allow_html=True)
        st.markdown('<p style="color:#888;margin:0;font-size:0.9rem;">you read them — now own them</p>',
                    unsafe_allow_html=True)
    with col_stats:
        level = st.session_state.xp // 100 + 1
        st.markdown(
            f'<div style="text-align:right;margin-top:6px;">'
            f'<span class="chip chip-streak">🔥 {st.session_state.streak}</span>'
            f'<span class="chip chip-level">⚡ Lvl {level}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Filters
    st.markdown('<p style="font-size:0.7rem;letter-spacing:0.2em;text-transform:uppercase;'
                'color:#888;font-weight:700;margin-bottom:0.3rem;">Categories</p>',
                unsafe_allow_html=True)
    cats = st.multiselect(
        "Categories",
        options=["everyday", "professional", "trending"],
        default=st.session_state.categories,
        label_visibility="collapsed",
        format_func=lambda x: {
            "everyday": "📖 Everyday",
            "professional": "💼 Professional",
            "trending": "📱 Trending slang",
        }[x],
    )
    st.session_state.categories = cats

    st.markdown('<p style="font-size:0.7rem;letter-spacing:0.2em;text-transform:uppercase;'
                'color:#888;font-weight:700;margin:0.8rem 0 0.3rem 0;">Difficulty</p>',
                unsafe_allow_html=True)
    diffs = st.multiselect(
        "Difficulty",
        options=["easy", "medium", "hard"],
        default=st.session_state.difficulties,
        label_visibility="collapsed",
        format_func=lambda x: {"easy": "🟢 Easy", "medium": "🟡 Medium", "hard": "🔴 Hard"}[x],
    )
    st.session_state.difficulties = diffs

    bank_size = len(get_filtered_bank(cats, diffs))
    st.caption(f"Pool size: {bank_size} words  ·  Mastered: {len(st.session_state.mastered)}")

    # Progress bar
    xp_in_level = st.session_state.xp % 100
    st.progress(xp_in_level / 100, text=f"{xp_in_level} / 100 XP to next level")

    st.markdown("### Pick a drill")

    # Drill 1: Listen & Spell
    if st.button("🔊  Listen & Spell  —  Hear the word, break it into syllables, type it",
                 use_container_width=True, type="primary"):
        st.session_state.game_mode = "dictation"
        start_round()
        st.rerun()

    # Drill 2: Flash & Recall
    if st.button("👁  Flash & Recall  —  See the word, type from memory (+5 XP)",
                 use_container_width=True):
        st.session_state.game_mode = "orthographic"
        start_round()
        st.rerun()

    # Stats view
    if st.button("📊  My Error Patterns  —  See your personal mistakes: dropped letters, swaps, substitutions",
                 use_container_width=True):
        st.session_state.screen = "stats"
        st.rerun()

    # Quick stats
    if st.session_state.total_attempts > 0:
        st.markdown("---")
        accuracy = round(100 * st.session_state.total_correct / st.session_state.total_attempts)
        c1, c2, c3 = st.columns(3)
        c1.metric("Accuracy", f"{accuracy}%")
        c2.metric("Mastered", len(st.session_state.mastered))
        c3.metric("Best streak", st.session_state.best_streak)

# ==============================================================================
# SCREEN: PLAY
# ==============================================================================

def screen_play():
    w = st.session_state.current_word
    if not w:
        st.session_state.screen = "home"
        st.rerun()
        return

    # Top bar
    c1, c2 = st.columns([1, 2])
    with c1:
        if st.button("← Exit", use_container_width=True):
            st.session_state.screen = "home"
            st.session_state.feedback = None
            st.rerun()
    with c2:
        # Category badge
        cat = None
        for category, diffs in WORD_BANK.items():
            for diff, words in diffs.items():
                if any(x["word"] == w["word"] for x in words):
                    cat = category
                    break
        badge_colors = {
            "everyday": ("#e0f2fe", "#0369a1"),
            "professional": ("#f3e8ff", "#7e22ce"),
            "trending": ("#fce7f3", "#be185d"),
        }
        bg, fg = badge_colors.get(cat, ("#eee", "#555"))
        st.markdown(
            f'<div style="text-align:right;">'
            f'<span style="background:{bg};color:{fg};padding:5px 12px;border-radius:999px;'
            f'font-size:0.75rem;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;">{cat or "?"}</span>'
            f'<span style="background:#f3f4f6;color:#555;padding:5px 12px;border-radius:999px;'
            f'font-size:0.75rem;font-weight:700;margin-left:6px;">{len(w["word"])} letters</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("")  # spacer

    # MODE: Flash & Recall (orthographic)
    if st.session_state.game_mode == "orthographic" and st.session_state.feedback is None:
        # Show the word glowing, then hide it after 2.5s using a JS timer.
        # Build the "dots" HTML in Python to keep the JS simple.
        word_len = len(w["word"])
        dots_html = "".join(
            '<span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#2a2a2a;margin:0 3px;"></span>'
            for _ in range(word_len)
        )
        # Escape any quotes/backslashes that might live in the word (none should, but be safe)
        word_safe = w["word"].replace("\\", "\\\\").replace("'", "\\'")
        flash_html = """
        <div id="flash-box" style="background:#0a0a0a;border-radius:20px;padding:40px 20px;text-align:center;min-height:160px;">
          <div id="flash-label" style="color:#fbbf24;font-size:10px;letter-spacing:0.3em;font-weight:700;text-transform:uppercase;opacity:0.6;margin-bottom:10px;">memorize the shape</div>
          <div id="flash-word" style="color:#fbbf24;font-size:3rem;font-weight:900;font-family:Georgia,serif;letter-spacing:0.04em;text-shadow:0 0 30px rgba(251,191,36,0.6),0 0 60px rgba(251,191,36,0.3);">__WORD__</div>
          <div id="flash-prompt" style="display:none;color:#666;font-size:10px;letter-spacing:0.3em;font-weight:700;text-transform:uppercase;">now type what you saw</div>
          <div id="flash-dots" style="display:none;margin-top:15px;">__DOTS__</div>
        </div>
        <script>
          setTimeout(function() {
            var fw = document.getElementById('flash-word');
            var fl = document.getElementById('flash-label');
            var fp = document.getElementById('flash-prompt');
            var fd = document.getElementById('flash-dots');
            if (fw) { fw.style.display = 'none'; }
            if (fl) { fl.style.display = 'none'; }
            if (fp) { fp.style.display = 'block'; }
            if (fd) { fd.style.display = 'block'; }
          }, 2500);
        </script>
        """.replace("__WORD__", word_safe).replace("__DOTS__", dots_html)
        components.html(flash_html, height=210)

    # MODE: Listen & Spell (dictation)
    else:
        if st.session_state.feedback is None:
            st.markdown(
                '<div style="background:linear-gradient(135deg,#0D8F7F08,#0D8F7F18);'
                'border:1px solid #0D8F7F25;border-radius:20px;padding:20px 15px;text-align:center;">',
                unsafe_allow_html=True,
            )
            tts_component(w["word"], label="🔊 Hear the word", rate=1.0, key=f"tts_{w['word']}")
            st.markdown(
                '<p style="font-size:0.7rem;letter-spacing:0.2em;text-transform:uppercase;'
                'color:#888;font-weight:700;margin:12px 0 6px 0;">Sound it out</p>',
                unsafe_allow_html=True,
            )
            st.markdown(syllable_pills_html(w["syllables"]), unsafe_allow_html=True)
            tts_syllables_component(w["syllables"], key=f"syl_{w['word']}")
            st.markdown("</div>", unsafe_allow_html=True)

    # Input
    st.markdown("")
    attempt_val = st.text_input(
        "Your spelling",
        value=st.session_state.attempt,
        key=f"input_{w['word']}_{st.session_state.total_attempts}",
        label_visibility="collapsed",
        placeholder="Type your spelling…",
        disabled=st.session_state.feedback is not None,
        autocomplete="off",
    )
    st.session_state.attempt = attempt_val

    # Action buttons
    if st.session_state.feedback is None:
        c1, c2 = st.columns([1, 2])
        with c1:
            if st.button("💡 Hint", use_container_width=True):
                st.session_state.show_hint = not st.session_state.show_hint
                st.rerun()
        with c2:
            if st.button("Check →", use_container_width=True, type="primary",
                         disabled=not st.session_state.attempt.strip()):
                submit_attempt()
                st.rerun()

        if st.session_state.show_hint:
            st.info(f"**Hint:** {w['hint']}\n\n💡 {w['mnemonic']}")

    # Feedback: CORRECT
    elif st.session_state.feedback == "correct":
        st.success(f"✓ **Nailed it.**  +{10 + (st.session_state.streak - 1) * 2} XP  ·  {st.session_state.streak}× streak")
        st.markdown('<p style="font-size:0.7rem;letter-spacing:0.2em;text-transform:uppercase;'
                    'color:#888;font-weight:700;margin-bottom:0;">Phonetic shape</p>',
                    unsafe_allow_html=True)
        st.markdown(render_phonetic_html(w["word"]), unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🏠 Home", use_container_width=True):
                st.session_state.screen = "home"
                st.session_state.feedback = None
                st.rerun()
        with c2:
            if st.button("Next word →", use_container_width=True, type="primary"):
                start_round()
                st.rerun()

    # Feedback: WRONG
    elif st.session_state.feedback == "wrong":
        err_desc = error_description(st.session_state.error_info)
        st.error(f"✗ **Not quite.**  {err_desc}")
        st.markdown(f'<div style="font-size:0.8rem;color:#999;text-align:center;margin-top:4px;">'
                    f'You typed: <span style="text-decoration:line-through;color:#dc2626;font-weight:700;">{st.session_state.attempt}</span>'
                    f'</div>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:0.7rem;letter-spacing:0.2em;text-transform:uppercase;'
                    'color:#888;font-weight:700;margin:15px 0 0 0;text-align:center;">Correct spelling</p>',
                    unsafe_allow_html=True)
        st.markdown(render_phonetic_html(w["word"]), unsafe_allow_html=True)
        st.warning(f"💡 **Remember:** {w['mnemonic']}")
        # Hear it again
        tts_component(w["word"], label="🔊 Hear it again", rate=0.85, key=f"retry_{w['word']}")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("↺ Try again", use_container_width=True):
                st.session_state.feedback = None
                st.session_state.error_info = None
                st.session_state.attempt = ""
                st.rerun()
        with c2:
            if st.button("Skip →", use_container_width=True, type="primary"):
                start_round()
                st.rerun()

# ==============================================================================
# SCREEN: STATS
# ==============================================================================

def screen_stats():
    c1, c2, c3 = st.columns([1, 2, 1])
    with c1:
        if st.button("← Back", use_container_width=True):
            st.session_state.screen = "home"
            st.rerun()
    with c2:
        st.markdown('<h2 style="text-align:center;font-family:Georgia,serif;margin:0;">Your Patterns</h2>',
                    unsafe_allow_html=True)

    st.markdown("---")

    if st.session_state.total_attempts == 0:
        st.info("No data yet. Play a few rounds to see your error patterns.")
        return

    accuracy = round(100 * st.session_state.total_correct / st.session_state.total_attempts)
    c1, c2 = st.columns(2)
    c1.metric("Accuracy", f"{accuracy}%")
    c1.metric("Best streak", st.session_state.best_streak)
    c2.metric("Mastered", len(st.session_state.mastered))
    c2.metric("Total attempts", st.session_state.total_attempts)

    # Error breakdown
    st.markdown("### Where you slip up")
    error_labels = {
        "missing_letter": "Dropped letters",
        "extra_letter": "Extra letters",
        "swapped_letters": "Swapped letters",
        "wrong_letter": "Wrong letter",
        "too_short": "Too short",
        "too_long": "Too long",
        "unknown": "Other",
    }
    counts = {}
    for e in st.session_state.error_history:
        counts[e["error_type"]] = counts.get(e["error_type"], 0) + 1

    if not counts:
        st.caption("No errors yet — keep going!")
    else:
        total = sum(counts.values())
        sorted_errors = sorted(counts.items(), key=lambda x: -x[1])
        for err_type, count in sorted_errors:
            pct = round(100 * count / total)
            st.markdown(
                f'<div style="background:white;border:1px solid #e5e5e5;border-radius:12px;'
                f'padding:12px 16px;margin-bottom:8px;">'
                f'<div style="display:flex;justify-content:space-between;margin-bottom:6px;">'
                f'<span style="font-weight:700;">{error_labels.get(err_type, err_type)}</span>'
                f'<span style="color:#888;font-family:monospace;">{count}× · {pct}%</span>'
                f'</div>'
                f'<div style="height:6px;background:#f3f4f6;border-radius:999px;overflow:hidden;">'
                f'<div style="height:100%;width:{pct}%;background:#0D8F7F;"></div>'
                f'</div></div>',
                unsafe_allow_html=True,
            )

    # Recent misses
    if st.session_state.error_history:
        st.markdown("### Recent misses")
        for e in list(reversed(st.session_state.error_history))[:8]:
            st.markdown(
                f'<div style="background:#fafaf7;border-radius:8px;padding:10px 14px;margin-bottom:6px;'
                f'display:flex;justify-content:space-between;align-items:center;">'
                f'<span style="font-family:monospace;color:#dc2626;text-decoration:line-through;">{e["attempt"]}</span>'
                f'<span style="color:#ccc;">→</span>'
                f'<span style="font-family:monospace;color:#1a1a1a;font-weight:700;">{e["word"]}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown("---")
    if st.button("⚠ Reset all progress", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        init_state()
        st.rerun()

# ==============================================================================
# ROUTER
# ==============================================================================

if st.session_state.screen == "home":
    screen_home()
elif st.session_state.screen == "play":
    screen_play()
elif st.session_state.screen == "stats":
    screen_stats()
