import os
import math
from PIL import Image, ImageDraw, ImageFilter

ROOT_DIR = "/Users/manandewan/.gemini/antigravity/scratch/careertracker"
ASSETS_DIR = os.path.join(ROOT_DIR, "assets/images")
os.makedirs(ASSETS_DIR, exist_ok=True)

# 1. Pristine Minimalist Vector SVG Logo
SVG_CONTENT = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="100%" height="100%">
  <defs>
    <!-- Background Obsidian Gradient -->
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f172a" />
      <stop offset="50%" stop-color="#0b101b" />
      <stop offset="100%" stop-color="#030712" />
    </linearGradient>
    
    <!-- Luminous Upward Trajectory Gradient (Emerald -> Cyan -> Indigo -> Violet) -->
    <linearGradient id="curveGrad" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#10b981" />
      <stop offset="35%" stop-color="#06b6d4" />
      <stop offset="70%" stop-color="#6366f1" />
      <stop offset="100%" stop-color="#a855f7" />
    </linearGradient>

    <!-- Beacon Radial Gradient -->
    <radialGradient id="beaconGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="1" />
      <stop offset="35%" stop-color="#6366f1" stop-opacity="0.8" />
      <stop offset="100%" stop-color="#6366f1" stop-opacity="0" />
    </radialGradient>

    <!-- Blur & Glow Filters -->
    <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="16" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>

    <filter id="ambientGlow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="40" />
    </filter>
  </defs>

  <!-- Squircle Base with Border -->
  <rect x="24" y="24" width="464" height="464" rx="112" fill="url(#bgGrad)" stroke="#1e293b" stroke-width="6" />
  
  <!-- Subtle Ambient Wealth Glow -->
  <circle cx="380" cy="140" r="160" fill="url(#beaconGlow)" opacity="0.35" filter="url(#ambientGlow)" />

  <!-- Minimalist Upward Growth Milestone Pillars -->
  <rect x="130" y="340" width="22" height="50" rx="6" fill="#10b981" opacity="0.35" />
  <rect x="180" y="310" width="22" height="80" rx="6" fill="#06b6d4" opacity="0.4" />
  <rect x="230" y="270" width="22" height="120" rx="6" fill="#38bdf8" opacity="0.45" />
  <rect x="280" y="210" width="22" height="180" rx="6" fill="#6366f1" opacity="0.5" />
  <rect x="330" y="140" width="22" height="250" rx="6" fill="#8b5cf6" opacity="0.55" />

  <!-- Upward Compounding Trajectory S-Curve (Underglow) -->
  <path d="M 105 385 C 200 380, 240 310, 280 230 C 320 150, 350 125, 385 125" 
        fill="none" stroke="url(#curveGrad)" stroke-width="32" stroke-linecap="round" opacity="0.4" filter="url(#glow)" />
  
  <!-- Upward Compounding Trajectory S-Curve (Crisp Core) -->
  <path d="M 105 385 C 200 380, 240 310, 280 230 C 320 150, 350 125, 385 125" 
        fill="none" stroke="url(#curveGrad)" stroke-width="18" stroke-linecap="round" />

  <!-- Apex Star / Beacon Node -->
  <circle cx="385" cy="125" r="32" fill="#38bdf8" opacity="0.25" filter="url(#glow)" />
  <circle cx="385" cy="125" r="18" fill="#ffffff" />
  <circle cx="385" cy="125" r="11" fill="#38bdf8" />
  <circle cx="385" cy="125" r="5" fill="#0b101b" />

  <!-- Minimalist Terminal Arrow Accent -->
  <path d="M 390 92 L 420 122 L 390 152" fill="none" stroke="#38bdf8" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" />
</svg>
"""

svg_path = os.path.join(ASSETS_DIR, "logo.svg")
with open(svg_path, "w", encoding="utf-8") as f:
    f.write(SVG_CONTENT)
print(f"Wrote {svg_path}")

# 2. High-Fidelity Raster Rendering Engine with Anti-Aliased Supersampling
def render_logo(size, is_maskable=False):
    scale = 4
    canvas_sz = size * scale
    
    # Maskable icons fill entire background with brand dark color
    # Standard icons have transparent margins
    bg_color = (11, 16, 27, 255) if is_maskable else (0, 0, 0, 0)
    img = Image.new("RGBA", (canvas_sz, canvas_sz), bg_color)
    draw = ImageDraw.Draw(img)

    # Safe zone for maskable icons is central 80% (10% padding on each side)
    # Standard icons use a sleek 5% margin
    margin = int(canvas_sz * 0.12) if is_maskable else int(canvas_sz * 0.05)
    x0, y0 = margin, margin
    x1, y1 = canvas_sz - margin, canvas_sz - margin
    radius = int((x1 - x0) * 0.23)

    # Base squircle
    draw.rounded_rectangle(
        [x0, y0, x1, y1],
        radius=radius,
        fill=(11, 16, 27, 255),
        outline=(30, 41, 59, 255),
        width=max(2, int(6 * (x1 - x0) / 512.0))
    )

    box_w = x1 - x0
    box_h = y1 - y0

    # Compounding pillars
    pillars = [
        (0.25, 0.67, 0.043, 0.12, (16, 185, 129, 90)),
        (0.35, 0.61, 0.043, 0.18, (6, 182, 212, 105)),
        (0.45, 0.53, 0.043, 0.26, (56, 189, 248, 120)),
        (0.55, 0.41, 0.043, 0.38, (99, 102, 241, 135)),
        (0.65, 0.27, 0.043, 0.52, (139, 92, 246, 150)),
    ]
    for px, py, pw, ph, col in pillars:
        bx = int(x0 + px * box_w)
        by = int(y0 + py * box_h)
        bw = int(pw * box_w)
        bh = int(ph * box_h)
        draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=max(2, int(6 * box_w / 512.0)), fill=col)

    # Cubic spline points for exponential S-curve
    steps = 120
    pts = []
    # Cubic Bezier: P0=(0.20, 0.75), P1=(0.39, 0.74), P2=(0.55, 0.45), P3=(0.76, 0.24)
    p0 = (x0 + 0.20 * box_w, y0 + 0.75 * box_h)
    p1 = (x0 + 0.39 * box_w, y0 + 0.74 * box_h)
    p2 = (x0 + 0.55 * box_w, y0 + 0.45 * box_h)
    p3 = (x0 + 0.76 * box_w, y0 + 0.24 * box_h)

    for i in range(steps + 1):
        t = i / float(steps)
        cx = (1-t)**3 * p0[0] + 3*(1-t)**2*t * p1[0] + 3*(1-t)*t**2 * p2[0] + t**3 * p3[0]
        cy = (1-t)**3 * p0[1] + 3*(1-t)**2*t * p1[1] + 3*(1-t)*t**2 * p2[1] + t**3 * p3[1]
        pts.append((cx, cy))

    # Glow under-curve
    glow_w = max(4, int(28 * box_w / 512.0))
    for i in range(len(pts) - 1):
        f = i / float(len(pts))
        r = int(16 + f * (168 - 16))
        g = int(185 - f * (185 - 85))
        b = int(129 + f * (247 - 129))
        draw.line([pts[i], pts[i+1]], fill=(r, g, b, 75), width=glow_w)

    # Crisp core trajectory line
    core_w = max(2, int(16 * box_w / 512.0))
    for i in range(len(pts) - 1):
        f = i / float(len(pts))
        r = int(16 + f * (168 - 16))
        g = int(185 - f * (185 - 85))
        b = int(129 + f * (247 - 129))
        draw.line([pts[i], pts[i+1]], fill=(r, g, b, 255), width=core_w)

    # Apex Beacon Node
    ax, ay = int(p3[0]), int(p3[1])
    r_halo = max(3, int(26 * box_w / 512.0))
    r_mid = max(2, int(16 * box_w / 512.0))
    r_core = max(1, int(9 * box_w / 512.0))
    r_center = max(1, int(4 * box_w / 512.0))

    draw.ellipse([ax - r_halo, ay - r_halo, ax + r_halo, ay + r_halo], fill=(56, 189, 248, 80))
    draw.ellipse([ax - r_mid, ay - r_mid, ax + r_mid, ay + r_mid], fill=(255, 255, 255, 255))
    draw.ellipse([ax - r_core, ay - r_core, ax + r_core, ay + r_core], fill=(56, 189, 248, 255))
    draw.ellipse([ax - r_center, ay - r_center, ax + r_center, ay + r_center], fill=(11, 16, 27, 255))

    return img.resize((size, size), Image.Resampling.LANCZOS)

# 3. Generate All Assets
print("Generating complete icon suite...")

# Standard icons
icon_192 = render_logo(192, is_maskable=False)
icon_512 = render_logo(512, is_maskable=False)
apple_180 = render_logo(180, is_maskable=False)
apple_152 = render_logo(152, is_maskable=False)
apple_167 = render_logo(167, is_maskable=False)
fav_16 = render_logo(16, is_maskable=False)
fav_32 = render_logo(32, is_maskable=False)
fav_48 = render_logo(48, is_maskable=False)

# Maskable icons (for Android adaptive icons)
maskable_192 = render_logo(192, is_maskable=True)
maskable_512 = render_logo(512, is_maskable=True)

# Save to assets/images
icon_192.save(os.path.join(ASSETS_DIR, "icon-192.png"))
icon_512.save(os.path.join(ASSETS_DIR, "icon-512.png"))
maskable_192.save(os.path.join(ASSETS_DIR, "icon-maskable-192.png"))
maskable_512.save(os.path.join(ASSETS_DIR, "icon-maskable-512.png"))
apple_180.save(os.path.join(ASSETS_DIR, "apple-touch-icon.png"))
apple_180.save(os.path.join(ASSETS_DIR, "apple-touch-icon-precomposed.png"))
apple_152.save(os.path.join(ASSETS_DIR, "apple-touch-icon-152.png"))
apple_167.save(os.path.join(ASSETS_DIR, "apple-touch-icon-167.png"))
fav_16.save(os.path.join(ASSETS_DIR, "favicon-16.png"))
fav_32.save(os.path.join(ASSETS_DIR, "favicon-32.png"))
fav_48.save(os.path.join(ASSETS_DIR, "favicon-48.png"))
fav_48.save(os.path.join(ASSETS_DIR, "favicon.png"))

# Multi-resolution ICO (16, 24, 32, 48, 64, 128, 256)
ico_base = render_logo(256, is_maskable=False)
ico_sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
ico_base.save(os.path.join(ASSETS_DIR, "favicon.ico"), format="ICO", sizes=ico_sizes)

# ALSO SAVE DIRECTLY TO REPO ROOT (Ensures hardcoded browser requests like /favicon.ico and /apple-touch-icon.png succeed!)
ico_base.save(os.path.join(ROOT_DIR, "favicon.ico"), format="ICO", sizes=ico_sizes)
apple_180.save(os.path.join(ROOT_DIR, "apple-touch-icon.png"))
apple_180.save(os.path.join(ROOT_DIR, "apple-touch-icon-precomposed.png"))
icon_192.save(os.path.join(ROOT_DIR, "icon-192.png"))
icon_512.save(os.path.join(ROOT_DIR, "icon-512.png"))
print("Saved root icons (favicon.ico, apple-touch-icon.png, icon-192.png, icon-512.png)")

# 4. Open Graph Social Card (1200 x 630)
def generate_og_card():
    width, height = 1200, 630
    bg = Image.new("RGBA", (width, height), (11, 16, 27, 255))

    # Glow circles
    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    d_glow = ImageDraw.Draw(glow)
    d_glow.ellipse([750, -120, 1300, 420], fill=(99, 102, 241, 45))
    d_glow.ellipse([-100, 280, 450, 820], fill=(16, 185, 129, 40))
    glow = glow.filter(ImageFilter.GaussianBlur(70))
    bg = Image.alpha_composite(bg, glow)

    # Render prominent logo on right
    logo_img = render_logo(360, is_maskable=False)
    bg.paste(logo_img, (760, 135), logo_img)

    og_path = os.path.join(ASSETS_DIR, "og-preview.png")
    bg.save(og_path, format="PNG")
    print(f"Generated {og_path} (1200x630)")

generate_og_card()
print("All icon assets successfully created and synchronized!")
