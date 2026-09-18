import json
import re

INDEX_PATH = 'index.html'
DATA_PATH = 'data/career_tracks_dataset.json'

with open(DATA_PATH, 'r', encoding='utf-8') as f:
    dataset = json.load(f)
dataset_json = json.dumps(dataset)

with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update COLLEGES_DATA
colleges_pattern = re.compile(r'const COLLEGES_DATA = \[.*?\];', re.DOTALL)
assert colleges_pattern.search(html), 'COLLEGES_DATA not found'
html = colleges_pattern.sub(lambda m: f'const COLLEGES_DATA = {dataset_json};', html)

# 2. Update activeCollegeIds default
html = html.replace(
    "let activeCollegeIds = new Set(['iima', 'fms', 'isb', 'iimt', 'iim_amritsar', 'srcc', 'venky']);",
    "let activeCollegeIds = new Set(['iima', 'fms', 'isb', 'iimt', 'iim_amritsar', 'srcc', 'srcc_median', 'venky']);"
)

# 3. Update preset mba_vs_ug
html = html.replace(
    "activeCollegeIds = new Set(['iima', 'fms', 'isb', 'iimt', 'iim_amritsar', 'srcc', 'venky']);",
    "activeCollegeIds = new Set(['iima', 'fms', 'isb', 'iimt', 'iim_amritsar', 'srcc', 'srcc_median', 'venky']);"
)

# 4. Update preset counts from 23 to 24
html = html.replace('All 23', 'All 24')
html = html.replace('0 / 23 Selected', '0 / 24 Selected')
html = html.replace('0 / 23', '0 / 24')
html = html.replace('MBA vs SRCC / Venky', 'MBA vs Undergrad Tracks')

# 5. Update the 5 strategic cards section
old_cards_pattern = re.compile(
    r'<!-- Strategic Takeaways & Analytical Cards -->.*?<!-- Portfolio & Investment Methodology Callout -->',
    re.DOTALL
)

new_cards_html = '''<!-- Main Model Pillars (Quick Reference) -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3 sm:gap-4">
      <!-- Card 1: Starting Points (Medians) -->
      <div class="bg-[#111827] border border-purple-500/35 rounded-2xl p-4 sm:p-5 shadow-xl relative overflow-hidden flex flex-col justify-between">
        <div class="w-1.5 h-full bg-purple-500 absolute left-0 top-0"></div>
        <div>
          <div class="text-[10px] font-bold text-purple-400 uppercase tracking-widest flex items-center gap-1 mb-1.5">
            <span>🎯 Starting Points</span>
          </div>
          <div class="text-base sm:text-lg font-black text-white tracking-tight leading-snug">
            Campus Median CTC
          </div>
          <p class="text-xs text-slate-300 font-medium leading-relaxed mt-2">
            Audited campus median CTC for all MBA colleges (e.g. ₹34.5L IIM-A, ₹32L FMS, ₹15.5L Baby IIMs) and official SRCC placement benchmarks.
          </p>
        </div>
      </div>

      <!-- Card 2: 7 Year EMIs for MBA -->
      <div class="bg-[#111827] border border-amber-500/35 rounded-2xl p-4 sm:p-5 shadow-xl relative overflow-hidden flex flex-col justify-between">
        <div class="w-1.5 h-full bg-amber-500 absolute left-0 top-0"></div>
        <div>
          <div class="text-[10px] font-bold text-amber-400 uppercase tracking-widest flex items-center gap-1 mb-1.5">
            <span>💳 MBA Debt Service</span>
          </div>
          <div class="text-base sm:text-lg font-black text-white tracking-tight leading-snug">
            7-Year Loan EMIs
          </div>
          <p class="text-xs text-slate-300 font-medium leading-relaxed mt-2">
            84 monthly EMIs deducted across Years 3–9 at 8.5%–9.0% interest (₹47.5k/mo IIM-A, ₹25.5k/mo Amritsar, ₹0 FMS &amp; Direct UG).
          </p>
        </div>
      </div>

      <!-- Card 3: PV Discounted -->
      <div class="bg-[#111827] border border-cyan-500/35 rounded-2xl p-4 sm:p-5 shadow-xl relative overflow-hidden flex flex-col justify-between">
        <div class="w-1.5 h-full bg-cyan-500 absolute left-0 top-0"></div>
        <div>
          <div class="text-[10px] font-bold text-cyan-400 uppercase tracking-widest flex items-center gap-1 mb-1.5">
            <span>⏱️ Today's Purchasing Power</span>
          </div>
          <div id="pillar-pv-headline" class="text-base sm:text-lg font-black text-white tracking-tight leading-snug">
            6.0% Inflation PV
          </div>
          <p id="pillar-pv-desc" class="text-xs text-slate-300 font-medium leading-relaxed mt-2">
            All future salaries and net wealth discounted back to Day 1 purchasing power, showing actual real-terms value in today’s rupees.
          </p>
        </div>
      </div>

      <!-- Card 4: How much is saved -->
      <div class="bg-[#111827] border border-emerald-500/35 rounded-2xl p-4 sm:p-5 shadow-xl relative overflow-hidden flex flex-col justify-between">
        <div class="w-1.5 h-full bg-emerald-500 absolute left-0 top-0"></div>
        <div>
          <div class="text-[10px] font-bold text-emerald-400 uppercase tracking-widest flex items-center gap-1 mb-1.5">
            <span>💰 Cash Saved</span>
          </div>
          <div class="text-base sm:text-lg font-black text-white tracking-tight leading-snug">
            35% &rarr; 45% &rarr; 60%
          </div>
          <p class="text-xs text-slate-300 font-medium leading-relaxed mt-2">
            Progressive savings rate of net in-hand cash after rent, taxes &amp; living costs: 35% (&lt;₹30L CTC), 45% (₹30–75L), 60% (&gt;₹75L).
          </p>
        </div>
      </div>

      <!-- Card 5: Portfolio Investing -->
      <div class="bg-[#111827] border border-indigo-500/35 rounded-2xl p-4 sm:p-5 shadow-xl relative overflow-hidden flex flex-col justify-between">
        <div class="w-1.5 h-full bg-indigo-500 absolute left-0 top-0"></div>
        <div>
          <div class="text-[10px] font-bold text-indigo-400 uppercase tracking-widest flex items-center gap-1 mb-1.5">
            <span>📈 Wealth Compounding</span>
          </div>
          <div class="text-base sm:text-lg font-black text-white tracking-tight leading-snug">
            9.0% Net Portfolio
          </div>
          <p class="text-xs text-slate-300 font-medium leading-relaxed mt-2">
            Annual surplus invested in 65% Equity Index (11.5%), 25% Debt/EPF (7.5%), 10% Gold for a post-tax net blended CAGR.
          </p>
        </div>
      </div>
    </div>

    <!-- Portfolio & Investment Methodology Callout -->'''

assert old_cards_pattern.search(html), 'old_cards_pattern not found'
html = old_cards_pattern.sub(new_cards_html, html)

# 6. Update updateStrategicCards()
old_fn_pattern = re.compile(r'function updateStrategicCards\(\) \{.*?\}\n\n    const pillsContainer', re.DOTALL)
new_fn_str = '''function updateStrategicCards() {
      const pvHeadline = document.getElementById('pillar-pv-headline');
      const pvDesc = document.getElementById('pillar-pv-desc');
      if (pvHeadline && pvDesc) {
        if (discountRate === 0.0) {
          pvHeadline.innerText = '0.0% Nominal Mode';
          pvDesc.innerText = 'Face-value cash flows without inflation adjustments. Reflects unadjusted nominal figures across all 20 years.';
        } else {
          pvHeadline.innerText = `${discountRate.toFixed(1)}% Inflation PV`;
          pvDesc.innerText = `All future salaries and net wealth discounted back to Day 1 purchasing power at ${discountRate.toFixed(1)}% annual rate.`;
        }
      }
    }

    const pillsContainer'''

assert old_fn_pattern.search(html), 'old_fn_pattern not found'
html = old_fn_pattern.sub(new_fn_str, html)

with open(INDEX_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print('Successfully updated index.html with 24 tracks, new headline cards, and updated updateStrategicCards!')
