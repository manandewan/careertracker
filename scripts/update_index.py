import json
import re

INDEX_PATH = "/Users/manandewan/.gemini/antigravity/scratch/careertracker/index.html"
DATA_PATH = "/Users/manandewan/.gemini/antigravity/scratch/careertracker/data/career_tracks_dataset.json"

with open(DATA_PATH, "r", encoding="utf-8") as f:
    dataset = json.load(f)
dataset_json_str = json.dumps(dataset)

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update <head> to add icon, manifest, and Open Graph tags
old_head_marker = '<title>CareerTracker: India Top MBA & Undergrad 20-Year Compensation Simulator</title>'
new_head_content = """<title>CareerTracker: India Top MBA & Undergrad 20-Year Compensation Simulator</title>

  <!-- Website Icon, Favicon & PWA Shortcut Assets -->
  <link rel="icon" type="image/svg+xml" href="assets/images/logo.svg">
  <link rel="icon" type="image/png" sizes="32x32" href="assets/images/favicon-32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="assets/images/favicon-16.png">
  <link rel="apple-touch-icon" sizes="180x180" href="assets/images/apple-touch-icon.png">
  <link rel="manifest" href="manifest.json">
  <meta name="theme-color" content="#0b101b">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="apple-mobile-web-app-title" content="CareerTracker">

  <!-- Open Graph & Social Preview Meta Tags (GitHub link preview) -->
  <meta property="og:type" content="website">
  <meta property="og:title" content="CareerTracker: India Top MBA & Undergrad Wealth Simulator">
  <meta property="og:description" content="Interactive 20-year post-tax compensation, loan EMI, and 9.0% portfolio wealth simulator comparing Top 20 Indian MBAs vs Direct Undergrad routes.">
  <meta property="og:image" content="assets/images/og-preview.png">
  <meta property="og:url" content="https://github.com/manandewan/careertracker">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="CareerTracker: India Top MBA & Undergrad Wealth Simulator">
  <meta name="twitter:description" content="Interactive 20-year post-tax compensation, loan EMI, and 9.0% portfolio wealth simulator comparing Top 20 Indian MBAs vs Direct Undergrad routes.">
  <meta name="twitter:image" content="assets/images/og-preview.png">"""

if old_head_marker in content and 'rel="apple-touch-icon"' not in content:
    content = content.replace(old_head_marker, new_head_content, 1)
    print("Injected head icon and meta tags.")

# 2. Update Header branding with logo and GitHub button
header_target_start = '<div class="flex flex-col lg:flex-row lg:items-center justify-between gap-3 sm:gap-4 relative z-10">'
header_target_end = '<!-- Presets & Quick Select Bar -->'

new_header_content = """<div class="flex flex-col lg:flex-row lg:items-center justify-between gap-3 sm:gap-4 relative z-10">
        <div class="flex items-start sm:items-center gap-3.5">
          <!-- Minimalist Website Brand Logo linking to GitHub -->
          <a href="https://github.com/manandewan/careertracker" target="_blank" rel="noopener noreferrer" 
             title="CareerTracker on GitHub (Star & Fork)"
             class="group relative flex-shrink-0 flex items-center justify-center w-12 h-12 sm:w-14 sm:h-14 rounded-2xl bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700/80 hover:border-indigo-500/80 shadow-lg shadow-indigo-950/40 transition-all transform hover:scale-105 active:scale-95">
            <img src="assets/images/logo.svg" alt="CareerTracker Logo" class="w-8 h-8 sm:w-10 sm:h-10 object-contain drop-shadow" />
            <span class="absolute -bottom-1 -right-1 flex h-4 w-4">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-4 w-4 bg-[#10b981] border-2 border-[#131b2e] items-center justify-center text-[8px] text-white font-bold">★</span>
            </span>
          </a>

          <div>
            <div class="flex items-center gap-2 mb-1.5 flex-wrap">
              <span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] sm:text-xs font-semibold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                <span>🇮🇳 Top MBAs + UG Benchmarks</span>
              </span>
              <span class="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] sm:text-xs font-medium bg-slate-800 text-slate-300 border border-slate-700/60">
                20-Yr Horizon (Ages 21–41)
              </span>
              <span class="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] sm:text-xs font-medium bg-emerald-950/60 text-emerald-300 border border-emerald-700/50">
                📈 9.0% Diversified Portfolio Compounding
              </span>
            </div>

            <h1 class="text-lg sm:text-2xl md:text-3xl font-extrabold tracking-tight text-white leading-snug flex items-center gap-2">
              CareerTracker: MBA & Undergrad Wealth Simulator
            </h1>
            <p class="text-[11px] sm:text-sm text-slate-400 mt-1 max-w-3xl leading-relaxed">
              Compare <strong>Top 20 MBAs</strong>, <strong>Baby IIMs</strong>, and direct undergrad tracks (<strong>SRCC</strong> & <strong>Deloitte / Venky UG</strong>) 
              after deducting New Regime tax, 7-year loan EMIs, living costs, and compounding surplus savings at a <strong>9.0% diversified portfolio CAGR</strong>.
            </p>
          </div>
        </div>

        <!-- Right Side: Horizon Controls & GitHub Link -->
        <div class="flex items-center gap-2 self-start sm:self-auto flex-wrap">
          <!-- Horizon Controls -->
          <div class="flex items-center justify-between sm:justify-start gap-1.5 bg-[#0b101b] border border-slate-800 rounded-xl p-1 shadow-inner">
            <span class="text-[10px] sm:text-[11px] font-medium text-slate-400 px-1.5 uppercase tracking-wider">Years:</span>
            <button onclick="setHorizon(5)" id="hz-5" class="hz-btn px-2.5 py-1 text-xs font-semibold rounded-lg text-slate-400 hover:text-white transition">5Y</button>
            <button onclick="setHorizon(10)" id="hz-10" class="hz-btn px-2.5 py-1 text-xs font-semibold rounded-lg text-slate-400 hover:text-white transition">10Y</button>
            <button onclick="setHorizon(20)" id="hz-20" class="hz-btn px-3 py-1 text-xs font-semibold rounded-lg bg-indigo-600 text-white shadow transition">20Y Full</button>
          </div>

          <!-- GitHub Repo Link Button -->
          <a href="https://github.com/manandewan/careertracker" target="_blank" rel="noopener noreferrer"
             title="Open CareerTracker on GitHub"
             class="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 hover:text-white border border-slate-700 hover:border-slate-500 text-xs font-semibold shadow transition active:scale-95">
            <svg class="w-4 h-4 fill-current text-slate-300" viewBox="0 0 24 24"><path fill-rule="evenodd" clip-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/></svg>
            <span class="hidden sm:inline">GitHub</span>
          </a>
        </div>
      </div>
      """

header_pattern = re.compile(re.escape(header_target_start) + r'.*?' + re.escape(header_target_end), re.DOTALL)
if header_pattern.search(content):
    content = header_pattern.sub(lambda m: new_header_content + "\n      " + header_target_end, content)
    print("Updated header with logo and GitHub button.")

# 3. Add Dedicated Analytical Card for Pure UG / Deloitte Ceiling in Strategic Takeaways
old_cards_grid = '<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">'
new_cards_grid = '<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3 sm:gap-4">'

pure_ug_card = """      <div class="bg-[#131b2e] border border-amber-500/30 rounded-2xl p-3.5 sm:p-4 shadow-lg relative overflow-hidden">
        <div class="w-1.5 h-full bg-amber-500 absolute left-0 top-0"></div>
        <h3 class="text-xs font-bold text-amber-400 flex items-center gap-1.5 mb-1">
          <span>🏢 Pure UG / Deloitte Ceiling</span>
        </h3>
        <p class="text-[11px] text-slate-300 leading-relaxed">
          Staying strictly on the undergrad track without a CA, CPA, or elite MBA hits an institutional ceiling at ~18 years: <strong>Senior Manager / Associate Director</strong> (₹40L–₹58L CTC, ₹32L–₹45L fixed base). Transitioning to delivery lead / PMO yields <strong>₹2.71 Cr</strong> 20-year wealth—safe, but ₹9+ Cr below IIM-A.
        </p>
      </div>
"""

if old_cards_grid in content and 'Pure UG / Deloitte Ceiling' not in content:
    content = content.replace(old_cards_grid, new_cards_grid, 1)
    callout_marker = '<!-- Portfolio & Investment Methodology Callout -->'
    content = content.replace(callout_marker, pure_ug_card + "\n    </div>\n\n    " + callout_marker, 1)
    print("Injected Pure UG / Deloitte Route analytical card.")

# 4. Update COLLEGES_DATA in script tag using lambda to avoid escape issues
colleges_pattern = re.compile(r'const COLLEGES_DATA = \[.*?\];', re.DOTALL)
new_colleges_stmt = f"const COLLEGES_DATA = {dataset_json_str};"
if colleges_pattern.search(content):
    content = colleges_pattern.sub(lambda m: new_colleges_stmt, content)
    print("Updated COLLEGES_DATA array with calibrated dataset.")

# 5. In table rendering, add ceiling badge if present
old_td_name = '<span class="font-bold text-white whitespace-nowrap">${c.name}</span>'
new_td_name = """<span class="font-bold text-white whitespace-nowrap">${c.name}</span>
              ${c.ceiling_role ? `<span class="hidden md:inline-block ml-1.5 text-[9px] px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/30" title="${c.ceiling_notes}">Ceiling: SM/AD (₹40-58L)</span>` : ''}"""
if old_td_name in content and 'c.ceiling_role' not in content:
    content = content.replace(old_td_name, new_td_name, 1)
    print("Added ceiling badge support to table rows.")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully updated index.html!")
