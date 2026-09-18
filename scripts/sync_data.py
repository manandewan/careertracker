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

# 2. Update SRCC Card
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
          Under the New Tax Regime (Sec 87A), taxable income up to ₹12.0L incurs <strong>₹0 tax</strong>. With ₹9.90L cash (₹9.0L fixed + ₹90k bonus), an SRCC decent placement pays <strong>ZERO tax</strong> in Year 1, taking home the full <strong>₹82,500/month</strong>! Under organic promotions at the same firm (Path B), zero-debt cash reaches <strong>₹1.16L/mo</strong> in Year 3 and compounds to <strong>₹5.92 Crores</strong> over 20 years (beating Baby IIMs by +₹1.34 Cr).
        </p>
      </div>\n\n      """

if srcc_card_pattern.search(html):
    html = srcc_card_pattern.sub(lambda m: new_srcc_card, html)
    print("Updated SRCC Decent Placement card.")

# 3. Update Baby IIM Card
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
          With a ₹17.5L fee and ₹25.5k/mo EMI, an IIM Amritsar grad takes home <strong>₹82k/month</strong> in Year 3 (lagging SRCC's ₹1.16L/mo). Over 20 years, their ₹4.58 Cr wealth trails SRCC's ₹5.92 Cr by <strong>₹1.34 Crores</strong> because early zero-debt cash compounding creates an insurmountable surplus lead.
        </p>
      </div>\n\n      """

if baby_card_pattern.search(html):
    html = baby_card_pattern.sub(lambda m: new_baby_card, html)
    print("Updated Baby IIM card.")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)
print("index.html synced successfully!")

# 4. Update README.md
with open(README_PATH, "r", encoding="utf-8") as f:
    readme = f.read()

# Replace SRCC table row and descriptions
readme = re.sub(
    r'\|\s*\*\*SRCC Decent Placement\*\*.*?\n',
    '| **SRCC Decent Placement** | Direct Undergrad | **₹1.2 L** | **₹0 / mo** | **₹0.83 L / mo** | **₹1.16 L / mo** | **₹2.47 L / mo** | **₹5.08 L / mo** | **₹5.92 Crores** |\n',
    readme
)
readme = readme.replace('₹6.69 Crores', '₹5.92 Crores')
readme = readme.replace('₹1.21 L / mo', '₹1.16 L / mo')
readme = readme.replace('₹1.21L/mo', '₹1.16L/mo')
readme = readme.replace('₹2.11 Crores', '₹1.34 Crores')
readme = readme.replace('₹2.11 Cr', '₹1.34 Cr')

with open(README_PATH, "w", encoding="utf-8") as f:
    readme = f.write(readme)
print("README.md synced successfully!")
