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
# TAGS
# A word can carry more than one tag (e.g. "privilege" is both professional and
# cyber) — tags are metadata for filtering, not exclusive folders.
# ==============================================================================

TAG_LABELS = {
    "everyday": "📖 Everyday",
    "professional": "💼 Pro",
    "mpd": "🚔 MPD",
    "cyber": "🛡 Cyber",
    "confused": "🔀 Confused",
    "trending": "📱 Slang",
}

TAG_COLORS = {
    "everyday": ("#e0f2fe", "#0369a1"),
    "professional": ("#f3e8ff", "#7e22ce"),
    "mpd": ("#e0e7ff", "#3730a3"),
    "cyber": ("#dcfce7", "#166534"),
    "confused": ("#fef9c3", "#854d0e"),
    "trending": ("#fce7f3", "#be185d"),
}

def theme_colors():
    """Small set of theme-aware colors, read fresh on every render. Cards that use
    a hardcoded light background (white/cream) need to switch to a dark card color
    in dark mode too — flipping only the page background would leave light-mode
    text illegible against a page background that no longer matches."""
    if st.session_state.get("dark_mode", False):
        return {"bg": "#0f1216", "card_bg": "#171b21", "text": "#e6e9ee",
                "text_dim": "#9aa4b2", "border": "#2a2f38"}
    return {"bg": "#fafaf7", "card_bg": "#ffffff", "text": "#1a1a1a",
            "text_dim": "#888", "border": "#e5e5e5"}

# ==============================================================================
# WORD BANK
# Flat list — each word has a "difficulty" and a "tags" list (one or more).
# Fields: syllables, hint (meaning), mnemonic (memory trick), common_error.
# ==============================================================================

WORD_BANK = [
    {"word": "friend", "difficulty": "easy", "tags": ["everyday"], "syllables": ["friend"], "hint": "someone you know and like", "mnemonic": "Fri + END — your week ENDs with a friend", "common_error": "freind"},
    {"word": "because", "difficulty": "easy", "tags": ["everyday"], "syllables": ["be", "cause"], "hint": "it tells you why", "mnemonic": "Big Elephants Can Always Understand Small Elephants", "common_error": "becuase"},
    {"word": "weird", "difficulty": "easy", "tags": ["everyday"], "syllables": ["weird"], "hint": "strange, unusual", "mnemonic": "weird breaks the i-before-e rule — WE are weird together", "common_error": "wierd"},
    {"word": "believe", "difficulty": "easy", "tags": ["everyday"], "syllables": ["be", "lieve"], "hint": "to think something is true", "mnemonic": "there's a LIE in beLIEve", "common_error": "belive"},
    {"word": "receive", "difficulty": "easy", "tags": ["everyday"], "syllables": ["re", "ceive"], "hint": "to get something", "mnemonic": "i before e EXCEPT after c — reCEIVE", "common_error": "recieve"},
    {"word": "tomorrow", "difficulty": "easy", "tags": ["everyday"], "syllables": ["to", "mor", "row"], "hint": "the day after today", "mnemonic": "two R's in TOMORROW — like two sunrises", "common_error": "tommorow"},
    {"word": "until", "difficulty": "easy", "tags": ["everyday"], "syllables": ["un", "til"], "hint": "up to the time that", "mnemonic": "only ONE L — un + til", "common_error": "untill"},
    {"word": "beginning", "difficulty": "easy", "tags": ["everyday"], "syllables": ["be", "gin", "ning"], "hint": "the start", "mnemonic": "double the N when you add -ING to beGIN", "common_error": "begining"},
    {"word": "profound", "difficulty": "easy", "tags": ["everyday"], "syllables": ["pro", "found"], "hint": "deep or highly meaningful", "mnemonic": "PRO + FOUND — you FOUND a deep truth", "common_error": "profund"},
    {"word": "diligent", "difficulty": "easy", "tags": ["everyday"], "syllables": ["dil", "i", "gent"], "hint": "consistently careful and hardworking", "mnemonic": "DIL + I + GENT — a diligent gentleman", "common_error": "delligent"},
    {"word": "astute", "difficulty": "easy", "tags": ["everyday"], "syllables": ["a", "stute"], "hint": "clever and perceptive", "mnemonic": "A + STUTE — an 'a-cute' observation", "common_error": "astude"},
    {"word": "candid", "difficulty": "easy", "tags": ["everyday"], "syllables": ["can", "did"], "hint": "honest and direct", "mnemonic": "CAN you be honest? I CANDID", "common_error": "canded"},
    {"word": "february", "difficulty": "easy", "tags": ["everyday"], "syllables": ["feb", "ru", "ar", "y"], "hint": "the second month of the year", "mnemonic": "FEB + RU + ARY — say the hidden R: Feb-RU-ary", "common_error": "febuary"},
    {"word": "jewelry", "difficulty": "easy", "tags": ["everyday"], "syllables": ["jew", "el", "ry"], "hint": "rings, necklaces, and similar accessories", "mnemonic": "JEWEL comes first, then RY — no extra E", "common_error": "jewelery"},
    {"word": "definitely", "difficulty": "medium", "tags": ["everyday"], "syllables": ["def", "i", "nite", "ly"], "hint": "for sure, 100%", "mnemonic": "defiNITEly has NITE in it — not defin-ATE-ly", "common_error": "definately"},
    {"word": "separate", "difficulty": "medium", "tags": ["everyday"], "syllables": ["sep", "a", "rate"], "hint": "to pull apart, divided", "mnemonic": "there's A RAT in sepARATe", "common_error": "seperate"},
    {"word": "embarrassed", "difficulty": "medium", "tags": ["everyday"], "syllables": ["em", "bar", "rassed"], "hint": "feeling awkward or ashamed", "mnemonic": "two R's, two S's — Really Red, Super Shy", "common_error": "embarassed"},
    {"word": "necessary", "difficulty": "medium", "tags": ["everyday"], "syllables": ["nec", "es", "sar", "y"], "hint": "needed, required", "mnemonic": "one Collar, two Socks (1 C, 2 S's)", "common_error": "neccessary"},
    {"word": "achievement", "difficulty": "medium", "tags": ["everyday"], "syllables": ["a", "chieve", "ment"], "hint": "a success or accomplishment", "mnemonic": "i before e — aCHIEVE", "common_error": "acheivement"},
    {"word": "argument", "difficulty": "medium", "tags": ["everyday"], "syllables": ["ar", "gu", "ment"], "hint": "a disagreement or debate", "mnemonic": "I lost an E in the argument", "common_error": "arguement"},
    {"word": "existence", "difficulty": "medium", "tags": ["everyday"], "syllables": ["ex", "is", "tence"], "hint": "the state of being", "mnemonic": "ends in -ENCE not -ANCE", "common_error": "existance"},
    {"word": "occasion", "difficulty": "medium", "tags": ["everyday"], "syllables": ["oc", "ca", "sion"], "hint": "a special event or time", "mnemonic": "two C's, one S — an ocCASion is a BIG deal", "common_error": "ocassion"},
    {"word": "meticulous", "difficulty": "medium", "tags": ["everyday"], "syllables": ["me", "tic", "u", "lous"], "hint": "very careful and precise about details", "mnemonic": "ME + TIC + U + LOUS — ticks off every detail", "common_error": "meticulus"},
    {"word": "eloquent", "difficulty": "medium", "tags": ["everyday"], "syllables": ["el", "o", "quent"], "hint": "clear and persuasive when speaking", "mnemonic": "EL + O + QUENT — like its cousin 'loquacious'", "common_error": "elequent"},
    {"word": "pragmatic", "difficulty": "medium", "tags": ["everyday"], "syllables": ["prag", "mat", "ic"], "hint": "practical and realistic", "mnemonic": "PRAG + MAT + IC — a practical MAT to stand on", "common_error": "pragmattic"},
    {"word": "ambiguous", "difficulty": "medium", "tags": ["everyday"], "syllables": ["am", "big", "u", "ous"], "hint": "unclear, having multiple meanings", "mnemonic": "AM + BIG + U + OUS — a BIG amount of uncertainty", "common_error": "ambigous"},
    {"word": "tedious", "difficulty": "medium", "tags": ["everyday"], "syllables": ["te", "di", "ous"], "hint": "long, repetitive, and boring", "mnemonic": "TE + DI + OUS — feels like it drags on forever", "common_error": "tedius"},
    {"word": "impeccable", "difficulty": "medium", "tags": ["everyday"], "syllables": ["im", "pec", "ca", "ble"], "hint": "without any noticeable faults", "mnemonic": "IM + PECC + ABLE — not even a peck of fault", "common_error": "impecable"},
    {"word": "plausible", "difficulty": "medium", "tags": ["everyday"], "syllables": ["plau", "si", "ble"], "hint": "reasonable or believable", "mnemonic": "PLAU + SI + BLE — you could apPLAUd the logic", "common_error": "plausable"},
    {"word": "resilient", "difficulty": "medium", "tags": ["everyday"], "syllables": ["re", "sil", "ient"], "hint": "able to recover from difficulty", "mnemonic": "RE + SIL + IENT — bounces back again (RE-)", "common_error": "resiliant"},
    {"word": "rhythm", "difficulty": "hard", "tags": ["everyday"], "syllables": ["rhy", "thm"], "hint": "a regular beat or pattern", "mnemonic": "Rhythm Helps Your Two Hips Move — Y is the only vowel", "common_error": "rythm"},
    {"word": "conscience", "difficulty": "hard", "tags": ["everyday"], "syllables": ["con", "science"], "hint": "your inner moral sense", "mnemonic": "con + SCIENCE — the science of right and wrong", "common_error": "conscence"},
    {"word": "acquiesce", "difficulty": "hard", "tags": ["everyday"], "syllables": ["ac", "qui", "esce"], "hint": "to reluctantly agree", "mnemonic": "AC + QUI + ESCE — the CQ together is rare", "common_error": "aquiesce"},
    {"word": "chrysanthemum", "difficulty": "hard", "tags": ["everyday"], "syllables": ["chry", "san", "the", "mum"], "hint": "a type of flower", "mnemonic": "CHRY + SAN + THE + MUM — Greek roots: gold flower", "common_error": "chrysantemum"},
    {"word": "onomatopoeia", "difficulty": "hard", "tags": ["everyday"], "syllables": ["on", "o", "ma", "to", "poe", "ia"], "hint": "words that sound like what they mean (buzz, hiss)", "mnemonic": "Old Nuns On Mopeds Are Tall, Often Pregnant, Often Eating Ice-cream Alone", "common_error": "onomatopeia"},
    {"word": "supersede", "difficulty": "hard", "tags": ["everyday"], "syllables": ["su", "per", "sede"], "hint": "to replace or take the place of", "mnemonic": "the only -SEDE word in English — all others use -CEDE or -CEED", "common_error": "supercede"},
    {"word": "succinct", "difficulty": "hard", "tags": ["everyday"], "syllables": ["suc", "cinct"], "hint": "brief but clearly expressed", "mnemonic": "SUC + CINCT — double C's, cinched tight", "common_error": "succint"},
    {"word": "mischievous", "difficulty": "hard", "tags": ["everyday"], "syllables": ["mis", "chie", "vous"], "hint": "playfully naughty", "mnemonic": "only 3 syllables — MIS-CHIE-VOUS, no extra I", "common_error": "mischevious"},
    {"word": "phenomenon", "difficulty": "hard", "tags": ["everyday"], "syllables": ["phe", "nom", "e", "non"], "hint": "a remarkable or notable occurrence", "mnemonic": "PHE + NOM + E + NON — ends in -NON not -NA", "common_error": "phenomenom"},
    {"word": "business", "difficulty": "easy", "tags": ["professional"], "syllables": ["busi", "ness"], "hint": "a commercial activity or company", "mnemonic": "busi + NESS — full of BUSY-ness", "common_error": "buisness"},
    {"word": "schedule", "difficulty": "easy", "tags": ["professional"], "syllables": ["sched", "ule"], "hint": "a plan of timed events", "mnemonic": "SCH at the start — like SCHool", "common_error": "schedual"},
    {"word": "career", "difficulty": "easy", "tags": ["professional"], "syllables": ["ca", "reer"], "hint": "a long-term profession", "mnemonic": "two R's, two E's — a long road", "common_error": "carreer"},
    {"word": "colleague", "difficulty": "easy", "tags": ["professional"], "syllables": ["col", "league"], "hint": "a work partner", "mnemonic": "col + LEAGUE — you're in the same league", "common_error": "collegue"},
    {"word": "benefit", "difficulty": "easy", "tags": ["professional"], "syllables": ["ben", "e", "fit"], "hint": "a helpful perk or advantage", "mnemonic": "one N, one F — a slim benefit", "common_error": "benifit"},
    {"word": "implement", "difficulty": "easy", "tags": ["professional"], "syllables": ["im", "ple", "ment"], "hint": "to put a plan into action", "mnemonic": "IM + PLE + MENT", "common_error": "impliment"},
    {"word": "evaluate", "difficulty": "easy", "tags": ["professional"], "syllables": ["e", "val", "u", "ate"], "hint": "to judge the value or worth of something", "mnemonic": "E + VALU + ATE — find the VALUe", "common_error": "evaluvate"},
    {"word": "objective", "difficulty": "easy", "tags": ["professional"], "syllables": ["ob", "jec", "tive"], "hint": "a goal, or free from personal bias", "mnemonic": "OB + JEC + TIVE", "common_error": "objectiv"},
    {"word": "concise", "difficulty": "easy", "tags": ["professional"], "syllables": ["con", "cise"], "hint": "brief and clear", "mnemonic": "CON + CISE — cut (cise) it short", "common_error": "consise"},
    {"word": "accommodate", "difficulty": "medium", "tags": ["professional"], "syllables": ["ac", "com", "mo", "date"], "hint": "to make room for", "mnemonic": "two C's AND two M's — room for everyone", "common_error": "accomodate"},
    {"word": "maintenance", "difficulty": "medium", "tags": ["professional"], "syllables": ["main", "ten", "ance"], "hint": "keeping things running", "mnemonic": "mainTENance has TEN in it, not TAIN", "common_error": "maintainance"},
    {"word": "questionnaire", "difficulty": "medium", "tags": ["professional"], "syllables": ["ques", "tion", "naire"], "hint": "a survey", "mnemonic": "double N before AIRE — French import", "common_error": "questionaire"},
    {"word": "occurrence", "difficulty": "medium", "tags": ["professional"], "syllables": ["oc", "cur", "rence"], "hint": "something that happens", "mnemonic": "two C's, two R's — it occurred twice", "common_error": "occurence"},
    {"word": "liaison", "difficulty": "medium", "tags": ["professional"], "syllables": ["li", "ai", "son"], "hint": "a person who connects two groups", "mnemonic": "LI-AI-SON — three vowel clusters in a row", "common_error": "liason"},
    {"word": "privilege", "difficulty": "medium", "tags": ["professional", "cyber"], "syllables": ["priv", "i", "lege"], "hint": "a special right or advantage", "mnemonic": "priv + i + LEGE — no D anywhere", "common_error": "priviledge"},
    {"word": "recommend", "difficulty": "medium", "tags": ["professional"], "syllables": ["rec", "om", "mend"], "hint": "to suggest as good", "mnemonic": "one C, two M's — I reComMend", "common_error": "reccomend"},
    {"word": "initiative", "difficulty": "medium", "tags": ["professional"], "syllables": ["i", "ni", "tia", "tive"], "hint": "the ability to act independently", "mnemonic": "I + NI + TIA + TIVE", "common_error": "innitiative"},
    {"word": "facilitate", "difficulty": "medium", "tags": ["professional"], "syllables": ["fa", "cil", "i", "tate"], "hint": "to make a process easier", "mnemonic": "FA + CIL + I + TATE — makes it FACILe (easy)", "common_error": "facilliate"},
    {"word": "collaborate", "difficulty": "medium", "tags": ["professional"], "syllables": ["col", "lab", "o", "rate"], "hint": "to work together with others", "mnemonic": "CO + LABOR + ATE — LABOR together", "common_error": "colaborate"},
    {"word": "strategic", "difficulty": "medium", "tags": ["professional"], "syllables": ["stra", "te", "gic"], "hint": "planned to achieve a long-term goal", "mnemonic": "STRA + TE + GIC — a STRATEGY made adjective", "common_error": "stratigic"},
    {"word": "bureaucracy", "difficulty": "hard", "tags": ["professional"], "syllables": ["bu", "reau", "cra", "cy"], "hint": "government or corporate red tape", "mnemonic": "BU-REAU (French) + CRACY — rule by desks", "common_error": "beaurocracy"},
    {"word": "entrepreneur", "difficulty": "hard", "tags": ["professional"], "syllables": ["en", "tre", "pre", "neur"], "hint": "someone who starts a business", "mnemonic": "French word — ends in NEUR not NUER", "common_error": "entreprenuer"},
    {"word": "consensus", "difficulty": "hard", "tags": ["professional"], "syllables": ["con", "sen", "sus"], "hint": "general agreement among a group", "mnemonic": "CON + SENSUS — common sense", "common_error": "concensus"},
    {"word": "conscientious", "difficulty": "hard", "tags": ["professional"], "syllables": ["con", "scien", "tious"], "hint": "careful and diligent", "mnemonic": "CON + SCIENCE + TIOUS — guided by conscience", "common_error": "conscientous"},
    {"word": "itinerary", "difficulty": "hard", "tags": ["professional"], "syllables": ["i", "tin", "er", "ar", "y"], "hint": "a travel plan", "mnemonic": "I + TIN + ER + ARY — five parts, like five stops", "common_error": "itenerary"},
    {"word": "discrepancy", "difficulty": "hard", "tags": ["professional", "mpd"], "syllables": ["dis", "crep", "an", "cy"], "hint": "a difference between things that should match", "mnemonic": "DIS + CREP + AN + CY", "common_error": "discrepency"},
    {"word": "comprehensive", "difficulty": "hard", "tags": ["professional"], "syllables": ["com", "pre", "hen", "sive"], "hint": "complete, covering everything", "mnemonic": "COM + PRE + HEN + SIVE", "common_error": "comprehensiv"},
    {"word": "affect", "difficulty": "medium", "tags": ["confused"], "syllables": ["af", "fect"], "hint": "verb: to influence or change something", "mnemonic": "Affect is Action — both start with A", "common_error": "effect"},
    {"word": "effect", "difficulty": "medium", "tags": ["confused"], "syllables": ["ef", "fect"], "hint": "noun: a result or consequence", "mnemonic": "Effect is the End result — both start with E", "common_error": "affect"},
    {"word": "than", "difficulty": "medium", "tags": ["confused"], "syllables": ["than"], "hint": "used to compare two things", "mnemonic": "thAn is for compArisons — same A", "common_error": "then"},
    {"word": "then", "difficulty": "medium", "tags": ["confused"], "syllables": ["then"], "hint": "refers to time, what happens next", "mnemonic": "thEn tells whEn something happens", "common_error": "than"},
    {"word": "accept", "difficulty": "medium", "tags": ["confused"], "syllables": ["ac", "cept"], "hint": "verb: to agree to receive or take something", "mnemonic": "ACCept — you take it in", "common_error": "except"},
    {"word": "except", "difficulty": "medium", "tags": ["confused"], "syllables": ["ex", "cept"], "hint": "preposition: excluding, other than", "mnemonic": "EXcept EXcludes something", "common_error": "accept"},
    {"word": "your", "difficulty": "medium", "tags": ["confused"], "syllables": ["your"], "hint": "belonging to you", "mnemonic": "YOUR shows ownership, no apostrophe", "common_error": "you're"},
    {"word": "you're", "difficulty": "medium", "tags": ["confused"], "syllables": ["you're"], "hint": "contraction meaning 'you are'", "mnemonic": "the apostrophe stands in for the A in 'you ARE'", "common_error": "your"},
    {"word": "its", "difficulty": "medium", "tags": ["confused"], "syllables": ["its"], "hint": "belonging to it — no apostrophe", "mnemonic": "ITS is possessive, like HIS or HERS", "common_error": "it's"},
    {"word": "it's", "difficulty": "medium", "tags": ["confused"], "syllables": ["it's"], "hint": "contraction meaning 'it is' or 'it has'", "mnemonic": "the apostrophe stands in for the I in 'it IS'", "common_error": "its"},
    {"word": "complement", "difficulty": "medium", "tags": ["confused"], "syllables": ["com", "ple", "ment"], "hint": "something that completes or pairs well with another", "mnemonic": "compleMENT — it compleTES the set", "common_error": "compliment"},
    {"word": "compliment", "difficulty": "medium", "tags": ["confused"], "syllables": ["com", "pli", "ment"], "hint": "a nice remark that praises someone", "mnemonic": "complIment — I like getting compliments", "common_error": "complement"},
    {"word": "principal", "difficulty": "medium", "tags": ["confused"], "syllables": ["prin", "ci", "pal"], "hint": "the person in charge, or most important", "mnemonic": "the principAL is your PAL", "common_error": "principle"},
    {"word": "principle", "difficulty": "medium", "tags": ["confused"], "syllables": ["prin", "ci", "ple"], "hint": "a fundamental rule or belief", "mnemonic": "a principLE is a ruLE", "common_error": "principal"},
    {"word": "lose", "difficulty": "medium", "tags": ["confused"], "syllables": ["lose"], "hint": "to fail to win, or to misplace something", "mnemonic": "LOSE has one O — you lOSE it", "common_error": "loose"},
    {"word": "loose", "difficulty": "medium", "tags": ["confused"], "syllables": ["loose"], "hint": "not tight, not firmly fixed", "mnemonic": "LOOSE has two O's — room to move", "common_error": "lose"},
    {"word": "stationary", "difficulty": "medium", "tags": ["confused"], "syllables": ["sta", "tion", "ar", "y"], "hint": "not moving, staying in place", "mnemonic": "stationAry — stAying still", "common_error": "stationery"},
    {"word": "stationery", "difficulty": "medium", "tags": ["confused"], "syllables": ["sta", "tion", "er", "y"], "hint": "paper and writing supplies", "mnemonic": "stationEry — lEtters written on it", "common_error": "stationary"},
    {"word": "rizz", "difficulty": "easy", "tags": ["trending"], "syllables": ["rizz"], "hint": "charisma, flirting skill (2024+ slang)", "mnemonic": "cha-RIZZ-ma, two Z's", "common_error": "riz"},
    {"word": "cringe", "difficulty": "easy", "tags": ["trending"], "syllables": ["cringe"], "hint": "secondhand embarrassment", "mnemonic": "crin + GE — G sounds like J here", "common_error": "crindge"},
    {"word": "vibe", "difficulty": "easy", "tags": ["trending"], "syllables": ["vibe"], "hint": "an atmosphere or feeling", "mnemonic": "V-I-B-E — four letters, one vibe", "common_error": "viebe"},
    {"word": "slay", "difficulty": "easy", "tags": ["trending"], "syllables": ["slay"], "hint": "to do something exceptionally well", "mnemonic": "S-L-A-Y — four letters, total win", "common_error": "slae"},
    {"word": "aesthetic", "difficulty": "medium", "tags": ["trending"], "syllables": ["aes", "thet", "ic"], "hint": "a visual style or vibe", "mnemonic": "starts with AE — Artistic Energy", "common_error": "asthetic"},
    {"word": "delulu", "difficulty": "medium", "tags": ["trending"], "syllables": ["de", "lu", "lu"], "hint": "playfully delusional (social media)", "mnemonic": "de + LU + LU, LU twice like seeing double", "common_error": "delooloo"},
    {"word": "brainrot", "difficulty": "medium", "tags": ["trending"], "syllables": ["brain", "rot"], "hint": "the feeling after too much scrolling", "mnemonic": "BRAIN + ROT, one word", "common_error": "brain-rot"},
    {"word": "crashout", "difficulty": "medium", "tags": ["trending"], "syllables": ["crash", "out"], "hint": "a dramatic meltdown", "mnemonic": "CRASH + OUT, one word", "common_error": "crash-out"},
    {"word": "synergize", "difficulty": "medium", "tags": ["trending"], "syllables": ["syn", "er", "gize"], "hint": "corporate: combine forces", "mnemonic": "syn (together) + ergy + ize", "common_error": "synergyze"},
    {"word": "leverage", "difficulty": "medium", "tags": ["trending"], "syllables": ["lev", "er", "age"], "hint": "to use as an advantage", "mnemonic": "LEVER + AGE — use the lever", "common_error": "leverege"},
    {"word": "millennial", "difficulty": "hard", "tags": ["trending"], "syllables": ["mil", "len", "ni", "al"], "hint": "generation born ~1981–1996", "mnemonic": "two L's, two N's — millennium = 1000 years", "common_error": "millenial"},
    {"word": "influencer", "difficulty": "hard", "tags": ["trending"], "syllables": ["in", "flu", "en", "cer"], "hint": "someone with a social media following", "mnemonic": "IN + FLU + EN + CER — four parts", "common_error": "influencier"},
    {"word": "algorithm", "difficulty": "hard", "tags": ["trending"], "syllables": ["al", "go", "rithm"], "hint": "a set of rules a computer follows", "mnemonic": "AL + GO + RITHM (like RHYTHM minus H)", "common_error": "algoritm"},
    {"word": "witness", "difficulty": "easy", "tags": ["mpd"], "syllables": ["wit", "ness"], "hint": "someone who saw an event happen", "mnemonic": "WIT + NESS — a sharp WIT sees everything", "common_error": "witnes"},
    {"word": "custody", "difficulty": "easy", "tags": ["mpd"], "syllables": ["cus", "to", "dy"], "hint": "official detention or care", "mnemonic": "CUS + TO + DY — three even parts", "common_error": "custady"},
    {"word": "juvenile", "difficulty": "easy", "tags": ["mpd"], "syllables": ["ju", "ve", "nile"], "hint": "a minor, someone under 18", "mnemonic": "JU + VE + NILE — like the NILE river", "common_error": "juvinile"},
    {"word": "patrol", "difficulty": "easy", "tags": ["mpd"], "syllables": ["pa", "trol"], "hint": "to actively monitor an area", "mnemonic": "PATROL rhymes with CONTROL — controlling the area", "common_error": "petrol"},
    {"word": "citation", "difficulty": "easy", "tags": ["mpd"], "syllables": ["ci", "ta", "tion"], "hint": "an official notice for a violation", "mnemonic": "CITE + ATION — you CITE the rule they broke", "common_error": "citiation"},
    {"word": "detective", "difficulty": "easy", "tags": ["mpd"], "syllables": ["de", "tec", "tive"], "hint": "an investigator, often plainclothes", "mnemonic": "DE + TEC + TIVE — DETECts the truth", "common_error": "detectave"},
    {"word": "allegation", "difficulty": "easy", "tags": ["mpd"], "syllables": ["al", "le", "ga", "tion"], "hint": "a claim made without proof yet", "mnemonic": "AL + LEGE + ATION — you ALLEGE it happened", "common_error": "allegetion"},
    {"word": "credible", "difficulty": "easy", "tags": ["mpd"], "syllables": ["cred", "i", "ble"], "hint": "believable, trustworthy", "mnemonic": "CRED + IBLE — it has CREDit (trust)", "common_error": "credable"},
    {"word": "vigilant", "difficulty": "easy", "tags": ["mpd"], "syllables": ["vig", "i", "lant"], "hint": "watchful and alert to danger", "mnemonic": "VIG + I + LANT — an ANT is always alert", "common_error": "vigilent"},
    {"word": "surveillance", "difficulty": "medium", "tags": ["mpd"], "syllables": ["sur", "veil", "lance"], "hint": "close monitoring of a person or place", "mnemonic": "SUR + VEIL + LANCE — a VEIL hides the watcher", "common_error": "surveilance"},
    {"word": "apprehend", "difficulty": "medium", "tags": ["mpd"], "syllables": ["ap", "pre", "hend"], "hint": "to arrest or seize someone", "mnemonic": "AP + PRE + HEND — two P's, from Latin 'to seize'", "common_error": "aprehend"},
    {"word": "interrogate", "difficulty": "medium", "tags": ["mpd"], "syllables": ["in", "ter", "ro", "gate"], "hint": "to formally question, especially a suspect", "mnemonic": "INTER + RO + GATE — INTERrupt with questions", "common_error": "interogate"},
    {"word": "perpetrator", "difficulty": "medium", "tags": ["mpd"], "syllables": ["per", "pe", "tra", "tor"], "hint": "the person who committed the offense", "mnemonic": "PER + PE + TRA + TOR — the one who PERpetrates", "common_error": "perpretrator"},
    {"word": "testimony", "difficulty": "medium", "tags": ["mpd"], "syllables": ["tes", "ti", "mo", "ny"], "hint": "a formal statement given as evidence", "mnemonic": "TEST + I + MO + NY — you TEST what they say", "common_error": "testamony"},
    {"word": "subpoena", "difficulty": "medium", "tags": ["mpd"], "syllables": ["sub", "poe", "na"], "hint": "a legal order to appear in court or produce evidence", "mnemonic": "SUB + POENA — silent P! sub-PEE-na", "common_error": "supeona"},
    {"word": "negligence", "difficulty": "medium", "tags": ["mpd"], "syllables": ["neg", "li", "gence"], "hint": "failure to take proper care, carelessness", "mnemonic": "NEG + LI + GENCE — NEGative attention to diligence", "common_error": "negligance"},
    {"word": "compliant", "difficulty": "medium", "tags": ["mpd"], "syllables": ["com", "pli", "ant"], "hint": "following rules or requirements", "mnemonic": "COM + PLI + ANT — COMPLies with the rule", "common_error": "complient"},
    {"word": "corroborate", "difficulty": "medium", "tags": ["mpd"], "syllables": ["cor", "rob", "o", "rate"], "hint": "to confirm or support with evidence", "mnemonic": "COR + ROB + O + RATE — co-confirms the story", "common_error": "corabborate"},
    {"word": "articulate", "difficulty": "medium", "tags": ["mpd"], "syllables": ["ar", "tic", "u", "late"], "hint": "able to express oneself clearly", "mnemonic": "AR + TIC + U + LATE — clear ARTICulation", "common_error": "artriculate"},
    {"word": "reconnaissance", "difficulty": "hard", "tags": ["mpd", "cyber"], "syllables": ["re", "con", "nais", "sance"], "hint": "preliminary scouting or information-gathering", "mnemonic": "RE + CON + NAIS + SANCE — French military term, double S", "common_error": "reconaissance"},
    {"word": "acquittal", "difficulty": "hard", "tags": ["mpd"], "syllables": ["ac", "quit", "tal"], "hint": "a legal decision of not guilty", "mnemonic": "AC + QUIT + TAL — you're QUIT of the charge", "common_error": "aquittal"},
    {"word": "jurisdiction", "difficulty": "hard", "tags": ["mpd", "professional"], "syllables": ["ju", "ris", "dic", "tion"], "hint": "the official authority or area of legal power", "mnemonic": "JURIS (law) + DICTION (speaking) — the law that speaks here", "common_error": "jurisdicton"},
    {"word": "circumstantial", "difficulty": "hard", "tags": ["mpd"], "syllables": ["cir", "cum", "stan", "tial"], "hint": "evidence based on inference, not direct proof", "mnemonic": "CIRCUM + STANTIAL — circles the fact instead of hitting it directly", "common_error": "circumstancial"},
    {"word": "indictment", "difficulty": "hard", "tags": ["mpd"], "syllables": ["in", "dict", "ment"], "hint": "a formal accusation of a serious crime", "mnemonic": "IN + DICT + MENT — silent C! in-DITE-ment", "common_error": "inditement"},
    {"word": "impartial", "difficulty": "hard", "tags": ["mpd"], "syllables": ["im", "par", "tial"], "hint": "unbiased, treating all sides fairly", "mnemonic": "IM + PAR + TIAL — not favoring either PARTy", "common_error": "impartual"},
    {"word": "de-escalate", "difficulty": "hard", "tags": ["mpd"], "syllables": ["de", "es", "ca", "late"], "hint": "to reduce the intensity of a conflict", "mnemonic": "DE + ESCALATE — the opposite of escalating (going up)", "common_error": "deescalate"},
    {"word": "authentication", "difficulty": "easy", "tags": ["cyber"], "syllables": ["au", "then", "ti", "ca", "tion"], "hint": "verifying that someone is who they claim to be", "mnemonic": "AUTH + EN + TIC + ATION — proving it's AUTHentic", "common_error": "authentification"},
    {"word": "persistence", "difficulty": "easy", "tags": ["cyber"], "syllables": ["per", "sis", "tence"], "hint": "maintaining access to a system over time", "mnemonic": "PER + SIST + ENCE — persists, keeps going", "common_error": "persistance"},
    {"word": "vulnerability", "difficulty": "medium", "tags": ["cyber"], "syllables": ["vul", "ner", "a", "bil", "i", "ty"], "hint": "a weakness that can be exploited", "mnemonic": "VUL + NER + A + BIL + I + TY — six parts, one weak spot", "common_error": "vulnerabiliy"},
    {"word": "remediation", "difficulty": "medium", "tags": ["cyber"], "syllables": ["re", "me", "di", "a", "tion"], "hint": "fixing or correcting a security issue", "mnemonic": "RE + MEDI + ATION — like MEDIcine to heal the flaw", "common_error": "remediaton"},
    {"word": "enumeration", "difficulty": "medium", "tags": ["cyber"], "syllables": ["e", "nu", "mer", "a", "tion"], "hint": "systematically discovering information about a target", "mnemonic": "E + NUM + ER + ATION — counts (NUMbers) everything found", "common_error": "enummeration"},
    {"word": "exploitation", "difficulty": "medium", "tags": ["cyber"], "syllables": ["ex", "ploi", "ta", "tion"], "hint": "taking advantage of a vulnerability", "mnemonic": "EX + PLOIT + ATION", "common_error": "exploitaton"},
    {"word": "obfuscation", "difficulty": "hard", "tags": ["cyber"], "syllables": ["ob", "fus", "ca", "tion"], "hint": "deliberately making something unclear or hard to understand", "mnemonic": "OB + FUS + CATION — a FOG (fus) of confusion", "common_error": "obsfucation"},
    {"word": "exfiltration", "difficulty": "hard", "tags": ["cyber"], "syllables": ["ex", "fil", "tra", "tion"], "hint": "stealing and moving data out of a system", "mnemonic": "EX + FIL + TRA + TION — EXits with the FILes", "common_error": "exfiltraton"},

    # --- Silent Letter Families ---
    # These teach a transferable pattern (e.g. every "kn-" word has a silent K),
    # not just one word in isolation. "silent_letter" groups them for the
    # Silent Letter Families screen and for pattern-aware wrong-answer feedback.
    {"word": "knife", "difficulty": "medium", "tags": ["everyday"], "silent_letter": "k", "syllables": ["knife"], "hint": "a tool with a sharp blade for cutting", "mnemonic": "Silent K family — the K used to be pronounced, same pattern as 'know'", "common_error": "nife"},
    {"word": "know", "difficulty": "medium", "tags": ["everyday"], "silent_letter": "k", "syllables": ["know"], "hint": "to have information or understanding about something", "mnemonic": "Silent K family — same pattern as 'knife', 'knee', 'knock'", "common_error": "now"},
    {"word": "knowledge", "difficulty": "medium", "tags": ["everyday"], "silent_letter": "k", "syllables": ["knowl", "edge"], "hint": "information and understanding gained through experience or study", "mnemonic": "Silent K family — same silent K as 'know'", "common_error": "nowledge"},
    {"word": "kneel", "difficulty": "medium", "tags": ["everyday"], "silent_letter": "k", "syllables": ["kneel"], "hint": "to go down on one or both knees", "mnemonic": "Silent K family — same pattern as 'knee'", "common_error": "neel"},
    {"word": "knee", "difficulty": "medium", "tags": ["everyday"], "silent_letter": "k", "syllables": ["knee"], "hint": "the joint where the leg bends", "mnemonic": "Silent K family — same pattern as 'kneel'", "common_error": "nee"},
    {"word": "knock", "difficulty": "medium", "tags": ["everyday"], "silent_letter": "k", "syllables": ["knock"], "hint": "to strike a surface to get attention", "mnemonic": "Silent K family — same pattern as 'knot'", "common_error": "nock"},
    {"word": "knot", "difficulty": "medium", "tags": ["everyday"], "silent_letter": "k", "syllables": ["knot"], "hint": "a fastening made by tying rope or string", "mnemonic": "Silent K family — same pattern as 'knock'", "common_error": "not"},

    {"word": "debt", "difficulty": "medium", "tags": ["everyday"], "silent_letter": "b", "syllables": ["debt"], "hint": "money that is owed", "mnemonic": "Silent B family — reflects the Latin root 'debitum', same pattern as 'doubt'", "common_error": "det"},
    {"word": "doubt", "difficulty": "medium", "tags": ["everyday"], "silent_letter": "b", "syllables": ["doubt"], "hint": "a feeling of uncertainty", "mnemonic": "Silent B family — same historical pattern as 'debt'", "common_error": "dout"},
    {"word": "subtle", "difficulty": "medium", "tags": ["everyday"], "silent_letter": "b", "syllables": ["sub", "tle"], "hint": "not obvious, delicate or precise", "mnemonic": "Silent B family — SUB + TLE, the B is silent", "common_error": "suttle"},
    {"word": "thumb", "difficulty": "medium", "tags": ["everyday"], "silent_letter": "b", "syllables": ["thumb"], "hint": "the short, thick finger next to the index finger", "mnemonic": "Silent B family — ends in -MB like 'climb' and 'lamb'", "common_error": "thum"},
    {"word": "lamb", "difficulty": "medium", "tags": ["everyday"], "silent_letter": "b", "syllables": ["lamb"], "hint": "a young sheep", "mnemonic": "Silent B family — ends in -MB like 'thumb' and 'climb'", "common_error": "lam"},
    {"word": "climb", "difficulty": "medium", "tags": ["everyday"], "silent_letter": "b", "syllables": ["climb"], "hint": "to go up using hands and feet", "mnemonic": "Silent B family — ends in -MB like 'thumb' and 'lamb'", "common_error": "clime"},

    {"word": "psychology", "difficulty": "medium", "tags": ["everyday"], "silent_letter": "p", "syllables": ["psy", "chol", "o", "gy"], "hint": "the scientific study of the mind and behavior", "mnemonic": "Silent P family — Greek 'ps-' start, like 'psychiatrist'", "common_error": "sychology"},
    {"word": "psychiatrist", "difficulty": "medium", "tags": ["everyday"], "silent_letter": "p", "syllables": ["psy", "chi", "a", "trist"], "hint": "a doctor who treats mental illness", "mnemonic": "Silent P family — same Greek 'ps-' as 'psychology'", "common_error": "sychiatrist"},
    {"word": "pneumonia", "difficulty": "medium", "tags": ["everyday"], "silent_letter": "p", "syllables": ["pneu", "mo", "nia"], "hint": "a lung infection", "mnemonic": "Silent P family — Greek 'pn-' start", "common_error": "neumonia"},
    {"word": "receipt", "difficulty": "medium", "tags": ["everyday"], "silent_letter": "p", "syllables": ["re", "ceipt"], "hint": "a printed record proving a purchase was made", "mnemonic": "Silent P family — related to 'receive' and 'reception', which explains the silent P", "common_error": "reciept"},

    {"word": "write", "difficulty": "medium", "tags": ["everyday"], "silent_letter": "w", "syllables": ["write"], "hint": "to form letters or words on a surface", "mnemonic": "Silent W family — WR- start, like 'wrist' and 'wrong'", "common_error": "rite"},
    {"word": "wrist", "difficulty": "medium", "tags": ["everyday"], "silent_letter": "w", "syllables": ["wrist"], "hint": "the joint connecting the hand and arm", "mnemonic": "Silent W family — same WR- as 'write'", "common_error": "rist"},
    {"word": "wreck", "difficulty": "medium", "tags": ["everyday"], "silent_letter": "w", "syllables": ["wreck"], "hint": "to destroy, or the remains of something destroyed", "mnemonic": "Silent W family — same WR- as 'wrap'", "common_error": "reck"},
    {"word": "wrong", "difficulty": "medium", "tags": ["everyday"], "silent_letter": "w", "syllables": ["wrong"], "hint": "incorrect or not true", "mnemonic": "Silent W family — same WR- as 'write'", "common_error": "rong"},
    {"word": "wrap", "difficulty": "medium", "tags": ["everyday"], "silent_letter": "w", "syllables": ["wrap"], "hint": "to cover something by folding material around it", "mnemonic": "Silent W family — same WR- as 'wreck'", "common_error": "rap"},

    {"word": "sign", "difficulty": "medium", "tags": ["everyday"], "silent_letter": "g", "syllables": ["sign"], "hint": "a symbol or notice conveying information", "mnemonic": "Silent G family — -GN ending, like 'design' and 'foreign'", "common_error": "sine"},
    {"word": "design", "difficulty": "medium", "tags": ["everyday"], "silent_letter": "g", "syllables": ["de", "sign"], "hint": "a plan or drawing showing how something will look or work", "mnemonic": "Silent G family — same -GN as 'sign'", "common_error": "desine"},
    {"word": "foreign", "difficulty": "medium", "tags": ["everyday"], "silent_letter": "g", "syllables": ["for", "eign"], "hint": "from a country other than one's own", "mnemonic": "Silent G family — same -GN as 'campaign'", "common_error": "foriegn"},
    {"word": "campaign", "difficulty": "medium", "tags": ["everyday"], "silent_letter": "g", "syllables": ["cam", "paign"], "hint": "an organized effort to achieve a goal", "mnemonic": "Silent G family — same -GN as 'foreign'", "common_error": "campain"},

    {"word": "castle", "difficulty": "medium", "tags": ["everyday"], "silent_letter": "t", "syllables": ["cas", "tle"], "hint": "a large fortified building", "mnemonic": "Silent T family — -STLE ending, like 'whistle'", "common_error": "cassle"},
    {"word": "whistle", "difficulty": "medium", "tags": ["everyday"], "silent_letter": "t", "syllables": ["whis", "tle"], "hint": "a device that makes a high-pitched sound when blown", "mnemonic": "Silent T family — same -STLE as 'castle'", "common_error": "whissle"},
    {"word": "listen", "difficulty": "medium", "tags": ["everyday"], "silent_letter": "t", "syllables": ["lis", "ten"], "hint": "to give attention to sound", "mnemonic": "Silent T family — same -STEN pattern as 'fasten'", "common_error": "lissen"},
    {"word": "fasten", "difficulty": "medium", "tags": ["everyday"], "silent_letter": "t", "syllables": ["fas", "ten"], "hint": "to attach or secure something firmly", "mnemonic": "Silent T family — same -STEN pattern as 'listen'", "common_error": "fassen"},

    {"word": "honest", "difficulty": "medium", "tags": ["everyday"], "silent_letter": "h", "syllables": ["hon", "est"], "hint": "truthful and sincere", "mnemonic": "Silent H family — same silent H as 'hour'", "common_error": "onest"},
    {"word": "hour", "difficulty": "medium", "tags": ["everyday"], "silent_letter": "h", "syllables": ["hour"], "hint": "a period of 60 minutes", "mnemonic": "Silent H family — same silent H as 'honest'", "common_error": "our"},

    {"word": "island", "difficulty": "medium", "tags": ["everyday"], "silent_letter": "s", "syllables": ["is", "land"], "hint": "land completely surrounded by water", "mnemonic": "Silent S family — the S was added historically and is never pronounced", "common_error": "iland"},
    {"word": "autumn", "difficulty": "medium", "tags": ["everyday"], "silent_letter": "n", "syllables": ["au", "tumn"], "hint": "the season between summer and winter", "mnemonic": "Silent N family — the final N is never pronounced", "common_error": "autum"},
    {"word": "salmon", "difficulty": "medium", "tags": ["everyday"], "silent_letter": "l", "syllables": ["salm", "on"], "hint": "a pink-fleshed fish", "mnemonic": "Silent L family — the L is never pronounced", "common_error": "samon"},
]

# ==============================================================================
# HELPERS
# ==============================================================================

VOWELS = set("aeiouAEIOU")

def get_filtered_bank(categories, difficulties):
    """Return list of word dicts matching the selected tags/difficulties.
    A word matches if ANY of its tags is in `categories` — words can belong to
    more than one category (e.g. "privilege" is tagged both professional and cyber)."""
    cat_set = set(categories)
    diff_set = set(difficulties)
    return [w for w in WORD_BANK if w["difficulty"] in diff_set and cat_set.intersection(w["tags"])]

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

def generate_typo_variant(word, avoid=None):
    """Create a plausible-looking misspelling of `word`, distinct from anything in `avoid`."""
    avoid = avoid or set()
    candidates = []
    if len(word) > 3:
        for _ in range(12):
            i = random.randint(0, len(word) - 2)
            variant = word[:i] + word[i + 1] + word[i] + word[i + 2:]
            if variant != word and variant not in avoid:
                candidates.append(variant)
    if len(word) > 2:
        i = random.randint(1, len(word) - 1)
        variant = word[:i] + word[i] + word[i:]
        if variant != word and variant not in avoid:
            candidates.append(variant)
    if len(word) > 4:
        i = random.randint(1, len(word) - 2)
        variant = word[:i] + word[i + 1:]
        if variant != word and variant not in avoid:
            candidates.append(variant)
    return random.choice(candidates) if candidates else word[::-1]

def pick_meaning_options(target, bank):
    """Return 4 shuffled meaning options (the real one + 3 decoys pulled from other words)."""
    correct = target["hint"]
    pool = [b["hint"] for b in bank if b["word"] != target["word"] and b["hint"] != correct]
    decoys = random.sample(pool, min(3, len(pool))) if pool else []
    options = [correct] + decoys
    random.shuffle(options)
    return options

def pick_spelling_options(target):
    """Return 3-4 shuffled spelling options (the real spelling + common_error + generated typos)."""
    correct = target["word"]
    options = [correct]
    common_err = target.get("common_error")
    if common_err and common_err != correct:
        options.append(common_err)
    seen = set(options)
    tries = 0
    while len(options) < 4 and tries < 20:
        variant = generate_typo_variant(correct, avoid=seen)
        if variant not in seen:
            options.append(variant)
            seen.add(variant)
        tries += 1
    random.shuffle(options)
    return options

def render_phonetic_html(word, accent="#0D8F7F"):
    """Return HTML where vowels are colored/underlined, consonants are plain."""
    t = theme_colors()
    chunks = []
    for ch in word:
        if ch in VOWELS:
            chunks.append(
                f'<span style="color:{accent};font-weight:800;border-bottom:3px solid {accent};padding-bottom:2px;">{ch}</span>'
            )
        else:
            chunks.append(f'<span style="color:{t["text"]};font-weight:700;">{ch}</span>')
    return (
        f'<div style="font-size:2.4rem;letter-spacing:0.05em;text-align:center;'
        f'font-family:Georgia,serif;margin:0.5rem 0 0.3rem 0;">{"".join(chunks)}</div>'
        f'<div style="font-size:0.7rem;text-align:center;color:{t["text_dim"]};letter-spacing:0.1em;'
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
        "categories": ["everyday", "professional", "mpd", "cyber", "confused"],
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
        "mc_options": None,  # choices for meaning_check / spot_spelling modes
        "dark_mode": False,
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
        # Don't call st.warning() here — the caller runs st.rerun() right after
        # this returns, which would wipe any message rendered inline before the
        # browser ever paints it. screen_home() shows its own warning instead,
        # driven live off bank_size, whenever the pool is empty.
        st.session_state.screen = "home"
        return
    st.session_state.current_word = w
    st.session_state.attempt = ""
    st.session_state.feedback = None
    st.session_state.error_info = None
    st.session_state.show_hint = False
    st.session_state.session_seen.add(w["word"])
    st.session_state.screen = "play"
    if st.session_state.game_mode == "meaning_check":
        bank = get_filtered_bank(st.session_state.categories, st.session_state.difficulties)
        st.session_state.mc_options = pick_meaning_options(w, bank)
    elif st.session_state.game_mode == "spot_spelling":
        st.session_state.mc_options = pick_spelling_options(w)
    else:
        st.session_state.mc_options = None

def apply_correct_result(w):
    st.session_state.feedback = "correct"
    gained = 10 + st.session_state.streak * 2
    st.session_state.xp += gained
    st.session_state.streak += 1
    st.session_state.best_streak = max(st.session_state.best_streak, st.session_state.streak)
    st.session_state.total_correct += 1
    correct = w["word"].lower()
    # Mark mastered if no recent errors for this word
    recent_misses = sum(1 for e in st.session_state.error_history[-15:] if e["word"] == correct)
    if recent_misses == 0:
        st.session_state.mastered.add(correct)

def apply_wrong_result(w, typed_spelling=None):
    st.session_state.feedback = "wrong"
    correct = w["word"].lower()
    st.session_state.streak = 0
    if typed_spelling is not None:
        err = analyze_error(correct, typed_spelling)
        st.session_state.error_info = err
        st.session_state.error_history.append({
            "word": correct,
            "attempt": typed_spelling,
            "error_type": err["type"] if err else "unknown",
            "timestamp": datetime.now().isoformat(),
        })
        st.session_state.recent_errors.append(correct)
        if len(st.session_state.recent_errors) > 20:
            st.session_state.recent_errors = st.session_state.recent_errors[-20:]
    else:
        st.session_state.error_info = None

def submit_attempt():
    w = st.session_state.current_word
    if not w:
        return
    guess_raw = st.session_state.attempt
    if not guess_raw:
        return
    st.session_state.total_attempts += 1
    mode = st.session_state.game_mode

    if mode == "meaning_check":
        if guess_raw == w["hint"]:
            apply_correct_result(w)
        else:
            apply_wrong_result(w, typed_spelling=None)
    elif mode == "spot_spelling":
        guess = guess_raw.strip().lower()
        if guess == w["word"].lower():
            apply_correct_result(w)
        else:
            apply_wrong_result(w, typed_spelling=guess)
    else:
        guess = guess_raw.strip().lower()
        if guess == w["word"].lower():
            apply_correct_result(w)
        else:
            apply_wrong_result(w, typed_spelling=guess)

# ==============================================================================
# PROGRESS BACKUP — no backend, so this is the real persistence mechanism.
# Streamlit session state resets when the tab fully closes; export/import lets
# progress survive that, across devices, or across browsers.
# ==============================================================================

PERSISTABLE_KEYS = [
    "streak", "best_streak", "xp", "total_correct", "total_attempts",
    "error_history", "recent_errors", "categories", "difficulties", "dark_mode",
]

def export_progress_dict():
    data = {k: st.session_state[k] for k in PERSISTABLE_KEYS}
    data["mastered"] = sorted(st.session_state.mastered)
    return data

def import_progress_dict(data):
    for k in PERSISTABLE_KEYS:
        if k in data:
            st.session_state[k] = data[k]
    if "mastered" in data:
        st.session_state.mastered = set(data["mastered"])

# ==============================================================================
# UI — GLOBAL STYLES
# ==============================================================================

def render_global_css():
    t = theme_colors()
    st.markdown(f"""
    <style>
      .stApp {{ background: {t['bg']}; }}
      .block-container {{ padding-top: 1.5rem; padding-bottom: 3rem; max-width: 640px; }}
      /* Make Streamlit's own text (markdown, captions, labels) follow the theme */
      .stApp, .stMarkdown, p, span, label, [data-testid="stCaptionContainer"] {{ color: {t['text']}; }}
      [data-testid="stCaptionContainer"] {{ color: {t['text_dim']} !important; }}
      /* Bigger, more tappable input for mobile */
      .stTextInput input {{
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        text-align: center !important;
        padding: 14px !important;
        border-radius: 14px !important;
        letter-spacing: 0.05em !important;
        background: {t['card_bg']} !important;
        color: {t['text']} !important;
        border-color: {t['border']} !important;
      }}
      /* Tappable buttons */
      .stButton button {{
        font-weight: 700 !important;
        border-radius: 12px !important;
        padding: 10px 18px !important;
        font-size: 0.95rem !important;
      }}
      /* Secondary (non-primary) buttons need theme-aware background/border too */
      .stButton button[kind="secondary"] {{
        background: {t['card_bg']} !important;
        color: {t['text']} !important;
        border-color: {t['border']} !important;
      }}
      /* Hide Streamlit footer/menu for cleaner app feel */
      #MainMenu {{ visibility: hidden; }}
      footer {{ visibility: hidden; }}
      header {{ visibility: hidden; }}
      /* Level/streak chips */
      .chip {{
        display: inline-block;
        padding: 6px 14px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 0.85rem;
        margin-right: 6px;
      }}
      .chip-streak {{ background: #fff7ed; color: #c2410c; border: 1px solid #fed7aa; }}
      .chip-level {{ background: #ecfdf5; color: #0D8F7F; border: 1px solid #a7f3d0; }}
      h1.logo {{
        font-family: Georgia, serif;
        font-weight: 900;
        letter-spacing: -0.02em;
        margin: 0;
        color: {t['text']};
      }}
    </style>
    """, unsafe_allow_html=True)

render_global_css()

# ==============================================================================
# SCREEN: HOME
# ==============================================================================

def toggle_pill_row(options, labels, state_key, per_row=3):
    """Render tap-to-toggle pills (wrapped into rows of `per_row`) bound to a list in
    st.session_state[state_key]. Mobile-friendlier than st.multiselect — one tap on/off
    instead of opening a dropdown and hunting for a tiny × to remove a selection."""
    selected = st.session_state[state_key]
    for row_start in range(0, len(options), per_row):
        row_opts = options[row_start:row_start + per_row]
        cols = st.columns(per_row)
        for i, opt in enumerate(row_opts):
            is_on = opt in selected
            with cols[i]:
                if st.button(labels[opt], key=f"{state_key}_{opt}", use_container_width=True,
                             type="primary" if is_on else "secondary"):
                    if is_on:
                        st.session_state[state_key] = [x for x in selected if x != opt]
                    else:
                        st.session_state[state_key] = selected + [opt]
                    st.rerun()

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
        if st.button("🌙 Dark" if not st.session_state.dark_mode else "☀️ Light",
                     key="dark_toggle", use_container_width=True):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()

    st.markdown("---")

    # Filters — tap-to-toggle pills, not dropdown multiselects (much easier on a phone)
    st.markdown('<p style="font-size:0.7rem;letter-spacing:0.2em;text-transform:uppercase;'
                'color:#888;font-weight:700;margin-bottom:0.3rem;">Categories</p>',
                unsafe_allow_html=True)
    toggle_pill_row(list(TAG_LABELS.keys()), TAG_LABELS, "categories")

    st.markdown('<p style="font-size:0.7rem;letter-spacing:0.2em;text-transform:uppercase;'
                'color:#888;font-weight:700;margin:0.8rem 0 0.3rem 0;">Difficulty</p>',
                unsafe_allow_html=True)
    toggle_pill_row(
        ["easy", "medium", "hard"],
        {"easy": "🟢 Easy", "medium": "🟡 Medium", "hard": "🔴 Hard"},
        "difficulties",
    )

    cats = st.session_state.categories
    diffs = st.session_state.difficulties
    bank_size = len(get_filtered_bank(cats, diffs))
    st.caption(f"Pool size: {bank_size} words  ·  Mastered: {len(st.session_state.mastered)}")
    if bank_size == 0:
        st.warning("No words match your filters. Pick at least one category and difficulty above before starting a drill.")

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

    # Drill 3: What's the Meaning?
    if st.button("🧠  What's the Meaning?  —  See the word, pick its true definition",
                 use_container_width=True):
        st.session_state.game_mode = "meaning_check"
        start_round()
        st.rerun()

    # Drill 4: Spot the Spelling
    if st.button("🔤  Spot the Spelling  —  Given the meaning, pick the correctly spelled word",
                 use_container_width=True):
        st.session_state.game_mode = "spot_spelling"
        start_round()
        st.rerun()

    # Silent Letter Families
    if st.button("🔇  Silent Letter Families  —  Learn the patterns behind knife, debt, psychology, and more",
                 use_container_width=True):
        st.session_state.screen = "silent"
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
# SCREEN: PLAY (multiple-choice modes — meaning_check / spot_spelling)
# ==============================================================================

def screen_play_mc(w):
    mode = st.session_state.game_mode
    options = st.session_state.mc_options or []

    if st.session_state.feedback is None:
        if mode == "meaning_check":
            # NOTE: the whole styled box must be built in ONE st.markdown call.
            # Streamlit renders each st.markdown()/components.html() call as its
            # own isolated block — opening a <div> in one call and closing it in
            # a later call does NOT nest them; the browser just auto-closes the
            # first (empty) div immediately, and later content renders outside
            # it, invisible-looking. This was a real bug, now fixed.
            st.markdown(
                f'<div style="background:linear-gradient(135deg,#0D8F7F08,#0D8F7F18);'
                f'border:1px solid #0D8F7F25;border-radius:20px;padding:25px 15px;text-align:center;">'
                f'<div style="font-size:2rem;font-weight:800;font-family:Georgia,serif;color:{theme_colors()["text"]};">{w["word"]}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
            tts_component(w["word"], label="🔊 Hear the word", rate=1.0, key=f"tts_mc_{w['word']}")
            st.markdown('<p style="font-size:0.7rem;letter-spacing:0.2em;text-transform:uppercase;'
                        'color:#888;font-weight:700;margin:15px 0 6px 0;">What does this mean?</p>',
                        unsafe_allow_html=True)
        else:  # spot_spelling
            st.markdown(
                f'<div style="background:linear-gradient(135deg,#0D8F7F08,#0D8F7F18);'
                f'border:1px solid #0D8F7F25;border-radius:20px;padding:20px 15px;text-align:center;">'
                f'<p style="font-size:0.7rem;letter-spacing:0.2em;text-transform:uppercase;color:#888;'
                f'font-weight:700;margin-bottom:8px;">This word means</p>'
                f'<p style="font-size:1.15rem;font-weight:700;margin:0;">{w["hint"]}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )
            st.markdown('<p style="font-size:0.7rem;letter-spacing:0.2em;text-transform:uppercase;'
                        'color:#888;font-weight:700;margin:15px 0 6px 0;">Which spelling is correct?</p>',
                        unsafe_allow_html=True)

        # Optional "sound it out" hint — syllables + audio, doesn't reveal which
        # option is correct, just gives phonetic scaffolding on request.
        if st.button("🗣 Sound it out (hint)", key=f"mc_hint_{w['word']}"):
            st.session_state.show_hint = not st.session_state.show_hint
            st.rerun()
        if st.session_state.show_hint:
            st.markdown(syllable_pills_html(w["syllables"]), unsafe_allow_html=True)
            tts_syllables_component(w["syllables"], key=f"mc_syl_{w['word']}")

        for opt in options:
            if st.button(opt, use_container_width=True, key=f"mcopt_{w['word']}_{opt}"):
                st.session_state.attempt = opt
                submit_attempt()
                st.rerun()

    elif st.session_state.feedback == "correct":
        st.success(f"✓ **Nailed it.**  +{10 + (st.session_state.streak - 1) * 2} XP  ·  {st.session_state.streak}× streak")
        if mode == "spot_spelling":
            st.markdown('<p style="font-size:0.7rem;letter-spacing:0.2em;text-transform:uppercase;'
                        'color:#888;font-weight:700;margin-bottom:0;">Phonetic shape</p>', unsafe_allow_html=True)
            st.markdown(render_phonetic_html(w["word"]), unsafe_allow_html=True)
        else:
            st.info(f"**{w['word']}** — {w['hint']}")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🏠 Home", use_container_width=True, key="mc_home_correct"):
                st.session_state.screen = "home"
                st.session_state.feedback = None
                st.rerun()
        with c2:
            if st.button("Next word →", use_container_width=True, type="primary", key="mc_next_correct"):
                start_round()
                st.rerun()

    elif st.session_state.feedback == "wrong":
        st.error(f'✗ **Not quite.**  You picked: "{st.session_state.attempt}"')
        if mode == "meaning_check":
            st.success(f"**{w['word']}** actually means: {w['hint']}")
        else:
            st.markdown('<p style="font-size:0.7rem;letter-spacing:0.2em;text-transform:uppercase;'
                        'color:#888;font-weight:700;margin:15px 0 0 0;text-align:center;">Correct spelling</p>',
                        unsafe_allow_html=True)
            st.markdown(render_phonetic_html(w["word"]), unsafe_allow_html=True)
        st.warning(f"💡 **Remember:** {w['mnemonic']}")
        tts_component(w["word"], label="🔊 Hear it again", rate=0.85, key=f"retry_mc_{w['word']}")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("↺ Try again", use_container_width=True, key="mc_retry_wrong"):
                st.session_state.feedback = None
                st.session_state.error_info = None
                st.session_state.attempt = ""
                st.rerun()
        with c2:
            if st.button("Skip →", use_container_width=True, type="primary", key="mc_skip_wrong"):
                start_round()
                st.rerun()

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
        # Tag badges — a word can carry more than one tag now (e.g. "privilege" is
        # both professional and cyber), so show all of them, not just one.
        tag_badges = ''.join(
            f'<span style="background:{TAG_COLORS.get(t, ("#eee","#555"))[0]};'
            f'color:{TAG_COLORS.get(t, ("#eee","#555"))[1]};padding:5px 12px;border-radius:999px;'
            f'font-size:0.75rem;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;margin-left:4px;">{t}</span>'
            for t in w["tags"]
        )
        st.markdown(
            f'<div style="text-align:right;">'
            f'{tag_badges}'
            f'<span style="background:#f3f4f6;color:#555;padding:5px 12px;border-radius:999px;'
            f'font-size:0.75rem;font-weight:700;margin-left:6px;">{len(w["word"])} letters</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("")  # spacer

    if st.session_state.game_mode in ("meaning_check", "spot_spelling"):
        screen_play_mc(w)
        return

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
            # Whole box built in one st.markdown call — see note in screen_play_mc()
            # about why splitting an open <div> across separate calls doesn't work.
            st.markdown(
                f'<div style="background:linear-gradient(135deg,#0D8F7F08,#0D8F7F18);'
                f'border:1px solid #0D8F7F25;border-radius:20px;padding:20px 15px;text-align:center;">'
                f'<p style="font-size:0.7rem;letter-spacing:0.2em;text-transform:uppercase;'
                f'color:#888;font-weight:700;margin:0 0 6px 0;">Sound it out</p>'
                f'{syllable_pills_html(w["syllables"])}'
                f'</div>',
                unsafe_allow_html=True,
            )
            tts_component(w["word"], label="🔊 Hear the word", rate=1.0, key=f"tts_{w['word']}")
            tts_syllables_component(w["syllables"], key=f"syl_{w['word']}")

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

        # Pattern-aware feedback: if the miss was dropping the word's known
        # silent letter, name the pattern and show sibling words instead of
        # treating it as a one-off mistake.
        err = st.session_state.error_info
        silent = w.get("silent_letter")
        if err and silent and err.get("type") == "missing_letter" and err.get("letter") == silent:
            siblings = [s["word"] for s in silent_letter_families().get(silent, []) if s["word"] != w["word"]][:4]
            st.info(f"🔍 **Pattern detected:** this is the **Silent {silent.upper()}** family — "
                    f"not a one-off, it shows up in {', '.join(siblings)} too.")

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
# SCREEN: SILENT LETTER FAMILIES
# ==============================================================================

def silent_letter_families():
    """Group words by their silent letter — the point is pattern recognition
    (every 'kn-' word has a silent K), not memorizing each word in isolation."""
    families = {}
    for w in WORD_BANK:
        letter = w.get("silent_letter")
        if letter:
            families.setdefault(letter, []).append(w)
    return families

def start_silent_family_practice(letter, words):
    """Lightweight alternative to start_round() — draws from this specific
    family's word list instead of the category/difficulty-filtered bank."""
    w = random.choice(words)
    st.session_state.game_mode = "dictation"
    st.session_state.current_word = w
    st.session_state.attempt = ""
    st.session_state.feedback = None
    st.session_state.error_info = None
    st.session_state.show_hint = False
    st.session_state.mc_options = None
    st.session_state.session_seen.add(w["word"])
    st.session_state.screen = "play"

def screen_silent_families():
    t = theme_colors()
    c1, c2 = st.columns([1, 3])
    with c1:
        if st.button("← Back", use_container_width=True):
            st.session_state.screen = "home"
            st.rerun()
    with c2:
        st.markdown('<h2 style="text-align:center;font-family:Georgia,serif;margin:0;">Silent Letter Families</h2>',
                    unsafe_allow_html=True)
    st.caption("Silent letters aren't random — they follow patterns. Learn the family, and you can spell words in it you've never seen before.")
    st.markdown("---")

    families = silent_letter_families()
    for letter in sorted(families.keys()):
        words = families[letter]
        st.markdown(
            f'<div style="background:{t["card_bg"]};border:1px solid {t["border"]};border-radius:12px;'
            f'padding:14px 16px;margin-bottom:10px;">'
            f'<div style="font-weight:800;font-size:1.1rem;color:{t["text"]};margin-bottom:6px;">'
            f'Silent {letter.upper()} <span style="font-weight:400;color:{t["text_dim"]};font-size:0.85rem;">({len(words)} words)</span></div>'
            f'<div style="color:{t["text_dim"]};">{", ".join(w["word"] for w in words)}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        if st.button(f"Practice Silent {letter.upper()} →", key=f"practice_silent_{letter}", use_container_width=True):
            start_silent_family_practice(letter, words)
            st.rerun()

# ==============================================================================
# SCREEN: STATS
# ==============================================================================

def screen_stats():
    t = theme_colors()
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
                f'<div style="background:{t["card_bg"]};border:1px solid {t["border"]};border-radius:12px;'
                f'padding:12px 16px;margin-bottom:8px;">'
                f'<div style="display:flex;justify-content:space-between;margin-bottom:6px;">'
                f'<span style="font-weight:700;color:{t["text"]};">{error_labels.get(err_type, err_type)}</span>'
                f'<span style="color:{t["text_dim"]};font-family:monospace;">{count}× · {pct}%</span>'
                f'</div>'
                f'<div style="height:6px;background:{t["border"]};border-radius:999px;overflow:hidden;">'
                f'<div style="height:100%;width:{pct}%;background:#0D8F7F;"></div>'
                f'</div></div>',
                unsafe_allow_html=True,
            )

    # Trouble Words — words you've missed that you haven't since gotten right
    trouble_counts = {}
    for e in st.session_state.error_history:
        if e["word"] not in st.session_state.mastered:
            trouble_counts[e["word"]] = trouble_counts.get(e["word"], 0) + 1
    if trouble_counts:
        st.markdown("### Your trouble words")
        st.caption("Missed at least once and not yet spelled correctly since. Keep drilling these until they drop off this list.")
        for word, count in sorted(trouble_counts.items(), key=lambda x: -x[1])[:12]:
            st.markdown(
                f'<div style="background:#fff7ed;border:1px solid #fed7aa;border-radius:8px;'
                f'padding:8px 14px;margin-bottom:6px;display:flex;justify-content:space-between;align-items:center;">'
                f'<span style="font-weight:700;color:#7c2d12;">{word}</span>'
                f'<span style="color:#c2410c;font-size:0.8rem;">missed {count}×</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # Recent misses
    if st.session_state.error_history:
        st.markdown("### Recent misses")
        for e in list(reversed(st.session_state.error_history))[:8]:
            st.markdown(
                f'<div style="background:{t["card_bg"]};border:1px solid {t["border"]};border-radius:8px;padding:10px 14px;margin-bottom:6px;'
                f'display:flex;justify-content:space-between;align-items:center;">'
                f'<span style="font-family:monospace;color:#dc2626;text-decoration:line-through;">{e["attempt"]}</span>'
                f'<span style="color:{t["text_dim"]};">→</span>'
                f'<span style="font-family:monospace;color:{t["text"]};font-weight:700;">{e["word"]}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown("---")
    st.markdown("### Backup your progress")
    st.caption("Progress lives only in this browser tab. Export it to a file so you don't lose it when the tab closes, or to move it to your phone/another browser.")
    c1, c2 = st.columns(2)
    with c1:
        st.download_button(
            "⬇ Export progress",
            data=json.dumps(export_progress_dict(), indent=2),
            file_name="spellforge_progress.json",
            mime="application/json",
            use_container_width=True,
        )
    with c2:
        uploaded = st.file_uploader("Restore from file", type=["json"], label_visibility="collapsed")
    if uploaded is not None:
        if st.button("Restore this file", use_container_width=True, type="primary"):
            try:
                data = json.loads(uploaded.read())
                import_progress_dict(data)
                st.success("Progress restored.")
                st.rerun()
            except Exception as e:
                st.error(f"Could not read that file: {e}")

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
elif st.session_state.screen == "silent":
    screen_silent_families()
