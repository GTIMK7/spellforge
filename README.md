# SpellForge

A spelling practice app for adults who read voraciously but struggle to spell.

Built for the "knows the word, can't spell it" profile. Three categories
(everyday · professional · trending slang), three difficulty tiers (easy ·
medium · hard), text-to-speech, orthographic memory drills, error-pattern
tracking.

## What's in this folder

- `spellforge.py` — the app itself, a single Python file
- `requirements.txt` — one line, tells the host to install Streamlit
- `README.md` — this file

## Running it locally (optional — skip if you only have a phone)

```bash
pip install streamlit
streamlit run spellforge.py
```

Opens at `http://localhost:8501` in your browser.

## Putting it on your iPhone — no App Store needed

You don't have a developer account and you're on a phone. Good news: you can
deploy this app to the web for free and use it like a native app. It takes
about 10 minutes end-to-end.

### Step 1 — Create a free GitHub account

Go to https://github.com and sign up. This is where your code will live.

### Step 2 — Create a new repository

On GitHub, click the **+** icon → **New repository**.
- Name it whatever you like (e.g. `spellforge`)
- Make it **Public** (required for free Streamlit Cloud hosting)
- Click **Create repository**

### Step 3 — Upload the three files

On the empty repo page, click **uploading an existing file** (or the
"Add file" dropdown → "Upload files"). Drag in:
- `spellforge.py`
- `requirements.txt`
- `README.md`

Click **Commit changes**.

### Step 4 — Deploy to Streamlit Cloud

Go to https://share.streamlit.io and sign in with your GitHub account.
- Click **Create app**
- Pick your `spellforge` repo
- Main file path: `spellforge.py`
- Click **Deploy**

After about 2 minutes, you'll get a URL like
`https://yourname-spellforge-xyz.streamlit.app`.

### Step 5 — Add to your iPhone home screen

On your iPhone:
1. Open the Streamlit URL in **Safari** (must be Safari, not Chrome)
2. Tap the **Share** button (square with arrow pointing up)
3. Scroll and tap **Add to Home Screen**
4. Name it "SpellForge" and tap **Add**

You'll now have a SpellForge icon on your home screen that launches
full-screen like any other app — no browser bars, no address bar.

## What works, what doesn't

**Works on iPhone:**
- Text-to-speech (uses the phone's built-in voice, no data cost)
- All drills, hints, error tracking
- Persists progress during your session

**Doesn't persist yet:**
- Progress resets if you close the tab completely. This is a Streamlit
  session-state limitation. The v1.1 fix is adding a lightweight database
  (Firebase, Supabase, or even a Google Sheet) so scores persist across
  visits. Not hard to add — just more scope than v1.

## Editing the word bank

Open `spellforge.py` and scroll to the `WORD_BANK` dictionary near the top.
Add or remove words in any category / difficulty — the app auto-adapts.

Each word needs:
- `word` — the correct spelling
- `syllables` — a list breaking it into chunks
- `hint` — what the word means
- `mnemonic` — a memory trick (the most important field!)
- `common_error` — a typical misspelling (for reference)

Example:
```python
{"word": "necessary", "syllables": ["nec", "es", "sar", "y"],
 "hint": "needed, required",
 "mnemonic": "one Collar, two Socks (1 C, 2 S's)",
 "common_error": "neccessary"}
```

After editing, commit the change to GitHub — Streamlit Cloud auto-redeploys.
