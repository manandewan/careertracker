import json
import re

INDEX_PATH = "/Users/manandewan/.gemini/antigravity/scratch/careertracker/index.html"
DATA_PATH = "/Users/manandewan/.gemini/antigravity/scratch/careertracker/data/career_tracks_dataset.json"
README_PATH = "/Users/manandewan/.gemini/antigravity/scratch/careertracker/README.md"

with open(DATA_PATH, "r", encoding="utf-8") as f:
    dataset = json.load(f)
dataset_json_str = json.dumps(dataset)

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update COLLEGES_DATA
colleges_pattern = re.compile(r'const COLLEGES_DATA = \[.*?\];', re.DOTALL)
if colleges_pattern.search(html):
    html = colleges_pattern.sub(lambda m: f"const COLLEGES_DATA = {dataset_json_str};", html)
    print("Updated COLLEGES_DATA array.")

# 2. Update Hero text
old_hero = 'direct undergrad tracks (<strong>SRCC</strong> & <strong>Deloitte / Venky UG</strong>)'
new_hero = 'direct undergrad tracks (<strong>SRCC Decent Placement</strong> & <strong>Deloitte / Venky UG</strong>)'
if old_hero in html:
    html = html.replace(old_hero, new_hero)
    print("Updated hero description.")

# 3. Update SRCC Card
srcc_card_pattern = re.compile(
    r'<div class="bg-\[#131b2e\] border border-purple-500/25 rounded-2xl p-3\.5 sm:p-4 shadow-lg relative overflow-hidden">.*?</div>\s*(?=<div class="bg-\[#131b2e\] border border-orange-500/25)',
    re.DOTALL
)
new_srcc_card = """<div class="bg-[#131b2e] border border-purple-500/25 rounded-2xl p-3.5 sm:p-4 shadow-lg relative overflow-hidden">
        <div class="w-1.5 h-full bg-purple-500 absolute left-0 top-0"></div>
        <h3 class="text-xs font-bold text-purple-400 flex items-center gap-1.5 mb-1">
          <span>🎓 SRCC Decent Placement Paradox</span>
        </h3>
        <p class="text-[11px] text-slate-300 leading-relaxed">
          An SRCC decent placement starts at <strong>₹14.40L CTC</strong> (₹9.0L fixed + ₹90k bonus + ₹4.5L benefits) at Age 21 with <strong>₹0 debt</strong>, making <strong>₹79k/mo</strong> in Year 1 and <strong>₹1.18L/mo</strong> in Year 3 (beating Baby IIM Amritsar's ₹0.80L/mo). Over 20 years, early debt-free compounding reaches <strong>₹6.48 Crores</strong> (outperforming Baby IIMs by +₹2.07 Cr) before the non-MBA ceiling locks in at Director level (~₹98.6L CTC).
        </p>
      </div>\n\n      """

if srcc_card_pattern.search(html):
    html = srcc_card_pattern.sub(lambda m: new_srcc_card, html)
    print("Updated SRCC Decent Placement card.")

# 4. Update Baby IIM Card
baby_card_pattern = re.compile(
    r'<div class="bg-\[#131b2e\] border border-orange-500/25 rounded-2xl p-3\.5 sm:p-4 shadow-lg relative overflow-hidden">.*?</div>\s*(?=<div class="bg-\[#131b2e\] border border-cyan-500/25)',
    re.DOTALL
)
new_baby_card = """<div class="bg-[#131b2e] border border-orange-500/25 rounded-2xl p-3.5 sm:p-4 shadow-lg relative overflow-hidden">
        <div class="w-1.5 h-full bg-orange-500 absolute left-0 top-0"></div>
        <h3 class="text-xs font-bold text-orange-400 flex items-center gap-1.5 mb-1">
          <span>👶 Baby IIM Squeeze vs. Top UG</span>
        </h3>
        <p class="text-[11px] text-slate-300 leading-relaxed">
          With a ₹17.5L fee and ₹25.5k/mo EMI, an IIM Amritsar grad takes home <strong>₹80k/month</strong> in Year 3 (lagging SRCC Decent Placement). Over 20 years, their ₹4.41 Cr wealth trails SRCC's ₹6.48 Cr because early zero-debt cash compounding creates an insurmountable surplus lead.
        </p>
      </div>\n\n      """

if baby_card_pattern.search(html):
    html = baby_card_pattern.sub(lambda m: new_baby_card, html)
    print("Updated Baby IIM card.")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)
print("index.html synced successfully!")

# 5. Update README.md
with open(README_PATH, "r", encoding="utf-8") as f:
    readme = f.read()

# Replace SRCC table row and descriptions
readme = re.sub(
    r'\|\s*\*\*SRCC Grad\*\*.*?\n',
    '| **SRCC Decent Placement** | Direct Undergrad | **₹1.2 L** | **₹0 / mo** | **₹0.79 L / mo** | **₹1.18 L / mo** | **₹2.78 L / mo** | **₹5.37 L / mo** | **₹6.48 Crores** |\n',
    readme
)
readme = readme.replace('SRCC Grad', 'SRCC Decent Placement')
readme = readme.replace('₹4.97 Crores', '₹6.48 Crores')
readme = readme.replace('₹7.30 Crores', '₹6.48 Crores')

with open(README_PATH, "w", encoding="utf-8") as f:
    f.write(readme)
print("README.md synced successfully!")
