import os
import math
from PIL import Image, ImageDraw, ImageFilter

ROOT_DIR = "/Users/manandewan/.gemini/antigravity/scratch/careertracker"
ASSETS_DIR = os.path.join(ROOT_DIR, "assets/images")
os.makedirs(ASSETS_DIR, exist_ok=True)

# 1. Minimalist Vector SVG
SVG_CONTENT = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="100%" height="100%">
  <defs>
    <!-- Background Obsidian Gradient -->
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f172a" />
      <stop offset="50%" stop-color="#0b101b" />
      <stop offset="100%" stop-color="#020617" />
    </linearGradient>
    
    <!-- Luminous Upward Trajectory Gradient -->
    <linearGradient id="curveGrad" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#10b981" />
      <stop offset="35%" stop-color="#06b6d4" />
      <stop offset="70%" stop-color="#6366f1" />
      <stop offset="100%" stop-color="#a855f7" />
    </linearGradient>

    <!-- Radial Beacon Glow -->
    <radialGradient id="beaconGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="1" />
      <stop offset="40%" stop-color="#6366f1" stop-opacity="0.8" />
      <stop offset="100%" stop-color="#6366f1" stop-opacity="0" />
    </radialGradient>

    <!-- Glow Filter -->
    <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="16" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>

    <filter id="softAmbient" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="40" />
    </filter>
  </defs>

  <!-- Full Background (Seamless for Shortcut Icons) -->
  <rect width="512" height="512" rx="112" fill="url(#bgGrad)" stroke="#1e293b" stroke-width="6" />
  
  <!-- Ambient Luminous Wealth Field -->
  <circle cx="375" cy="145" r="160" fill="url(#beaconGlow)" opacity="0.35" filter="url(#softAmbient)" />

  <!-- Minimalist Compounding Milestone Pillars -->
  <rect x="135" y="335" width="22" height="55" rx="6" fill="#10b981" opacity="0.4" />
  <rect x="185" y="305" width="22" height="85" rx="6" fill="#06b6d4" opacity="0.45" />
  <rect x="235" y="265" width="22" height="125" rx="6" fill="#38bdf8" opacity="0.5" />
  <rect x="285" y="205" width="22" height="185" rx="6" fill="#6366f1" opacity="0.55" />
  <rect x="335" y="135" width="22" height="255" rx="6" fill="#8b5cf6" opacity="0.6" />

  <!-- Exponential Trajectory S-Curve (Atmospheric Glow) -->
  <path d="M 110 380 C 195 375, 240 310, 275 235 C 315 150, 345 130, 380 130" 
        fill="none" stroke="url(#curveGrad)" stroke-width="32" stroke-linecap="round" opacity="0.4" filter="url(#glow)" />
  
  <!-- Exponential Trajectory S-Curve (Crisp Luminous Core) -->
  <path d="M 110 380 C 195 375, 240 310, 275 235 C 315 150, 345 130, 380 130" 
        fill="none" stroke="url(#curveGrad)" stroke-width="18" stroke-linecap="round" />

  <!-- Apex Beacon Node -->
  <circle cx="380" cy="130" r="30" fill="#38bdf8" opacity="0.25" filter="url(#glow)" />
  <circle cx="380" cy="130" r="17" fill="#ffffff" />
  <circle cx="380" cy="130" r="10" fill="#38bdf8" />
  <circle cx="380" cy="130" r="4.5" fill="#0b101b" />

  <!-- Minimalist Arrow Accent -->
  <path d="M 385 96 L 415 126 L 385 156" fill="none" stroke="#38bdf8" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" />
</svg>
"""

with open(os.path.join(ASSETS_DIR, "logo.svg"), "w", encoding="utf-8") as f:
    f.write(SVG_CONTENT)
print("Saved logo.svg")

# 2. Rendering Engine
def render_master_icon(size, is_opaque=True, safe_zone_scale=0.76):
    """
    Renders high-DPI icon with 4x supersampling.
    If is_opaque=True: Returns RGB mode image (100% solid, NO transparency, REQUIRED by Apple Touch Icon!).
    If is_opaque=False: Returns RGBA mode image (transparent background around squircle for favicons).
    safe_zone_scale controls how much of the canvas the icon graphic occupies (0.76 ensures zero clipping on iOS/Android).
    """
    scale = 4
    canvas_sz = size * scale
    
    # Background
    if is_opaque:
        # Full-bleed solid dark gradient
        img = Image.new("RGB", (canvas_sz, canvas_sz), (11, 16, 27))
        draw = ImageDraw.Draw(img)
        # Subtle diagonal gradient
        for y in range(canvas_sz):
            frac = y / float(canvas_sz)
            r = int(15 - frac * 12)
            g = int(23 - frac * 17)
            b = int(42 - frac * 20)
            draw.line([(0, y), (canvas_sz, y)], fill=(max(2, r), max(6, g), max(17, b)))
    else:
        img = Image.new("RGBA", (canvas_sz, canvas_sz), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        # Draw squircle container
        margin = int(canvas_sz * 0.05)
        x0, y0 = margin, margin
        x1, y1 = canvas_sz - margin, canvas_sz - margin
        radius = int((x1 - x0) * 0.23)
        draw.rounded_rectangle(
            [x0, y0, x1, y1],
            radius=radius,
            fill=(11, 16, 27, 255),
            outline=(30, 41, 59, 255),
            width=max(2, int(6 * (x1 - x0) / 512.0))
        )

    # Calculate content bounding box centered in canvas
    box_w = canvas_sz * safe_zone_scale
    box_h = canvas_sz * safe_zone_scale
    x0 = (canvas_sz - box_w) / 2.0
    y0 = (canvas_sz - box_h) / 2.0
    x1 = x0 + box_w
    y1 = y0 + box_h

    # Ambient Beacon Glow
    glow_x = x0 + 0.76 * box_w
    glow_y = y0 + 0.25 * box_h
    glow_r = box_w * 0.38
    
    # Pillars
    pillars = [
        (0.24, 0.67, 0.045, 0.13, (16, 185, 129)),
        (0.34, 0.60, 0.045, 0.20, (6, 182, 212)),
        (0.44, 0.52, 0.045, 0.28, (56, 189, 248)),
        (0.54, 0.40, 0.045, 0.40, (99, 102, 241)),
        (0.64, 0.26, 0.045, 0.54, (139, 92, 246)),
    ]
    for px, py, pw, ph, col in pillars:
        bx = int(x0 + px * box_w)
        by = int(y0 + py * box_h)
        bw = int(pw * box_w)
        bh = int(ph * box_h)
        # alpha blending manually for RGB
        fill_col = col if is_opaque else (*col, 160)
        draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=max(2, int(6 * box_w / 512.0)), fill=fill_col)

    # Cubic Bezier Points
    p0 = (x0 + 0.18 * box_w, y0 + 0.77 * box_h)
    p1 = (x0 + 0.38 * box_w, y0 + 0.75 * box_h)
    p2 = (x0 + 0.54 * box_w, y0 + 0.46 * box_h)
    p3 = (x0 + 0.76 * box_w, y0 + 0.24 * box_h)

    steps = 140
    pts = []
    for i in range(steps + 1):
        t = i / float(steps)
        cx = (1-t)**3 * p0[0] + 3*(1-t)**2*t * p1[0] + 3*(1-t)*t**2 * p2[0] + t**3 * p3[0]
        cy = (1-t)**3 * p0[1] + 3*(1-t)**2*t * p1[1] + 3*(1-t)*t**2 * p2[1] + t**3 * p3[1]
        pts.append((cx, cy))

    # Outer Glow Line
    glow_w = max(4, int(28 * box_w / 512.0))
    for i in range(len(pts) - 1):
        f = i / float(len(pts))
        r = int(16 + f * (168 - 16))
        g = int(185 - f * (185 - 85))
        b = int(129 + f * (247 - 129))
        draw.line([pts[i], pts[i+1]], fill=(r, g, b) if is_opaque else (r, g, b, 80), width=glow_w)

    # Core Sharp Trajectory Line
    core_w = max(2, int(16 * box_w / 512.0))
    for i in range(len(pts) - 1):
        f = i / float(len(pts))
        r = int(16 + f * (168 - 16))
        g = int(185 - f * (185 - 85))
        b = int(129 + f * (247 - 129))
        draw.line([pts[i], pts[i+1]], fill=(r, g, b) if is_opaque else (r, g, b, 255), width=core_w)

    # Apex Beacon
    ax, ay = int(p3[0]), int(p3[1])
    r_halo = max(3, int(26 * box_w / 512.0))
    r_mid = max(2, int(16 * box_w / 512.0))
    r_core = max(1, int(9 * box_w / 512.0))
    r_center = max(1, int(4 * box_w / 512.0))

    draw.ellipse([ax - r_halo, ay - r_halo, ax + r_halo, ay + r_halo], fill=(56, 189, 248) if is_opaque else (56, 189, 248, 100))
    draw.ellipse([ax - r_mid, ay - r_mid, ax + r_mid, ay + r_mid], fill=(255, 255, 255))
    draw.ellipse([ax - r_core, ay - r_core, ax + r_core, ay + r_core], fill=(56, 189, 248))
    draw.ellipse([ax - r_center, ay - r_center, ax + r_center, ay + r_center], fill=(11, 16, 27))

    # Downsample with Lanczos
    res = img.resize((size, size), Image.Resampling.LANCZOS)
    return res

print("Generating 100% OPAQUE Apple Touch Icons (RGB mode)...")
# Apple Touch Icons (180, 152, 167, 120)
apple_180 = render_master_icon(180, is_opaque=True, safe_zone_scale=0.74)
apple_152 = render_master_icon(152, is_opaque=True, safe_zone_scale=0.74)
apple_167 = render_master_icon(167, is_opaque=True, safe_zone_scale=0.74)
apple_120 = render_master_icon(120, is_opaque=True, safe_zone_scale=0.74)

# Save Apple Touch Icons in BOTH root AND assets/images
apple_180.save(os.path.join(ROOT_DIR, "apple-touch-icon.png"), format="PNG")
apple_180.save(os.path.join(ROOT_DIR, "apple-touch-icon-precomposed.png"), format="PNG")
apple_180.save(os.path.join(ASSETS_DIR, "apple-touch-icon.png"), format="PNG")
apple_180.save(os.path.join(ASSETS_DIR, "apple-touch-icon-precomposed.png"), format="PNG")
apple_180.save(os.path.join(ASSETS_DIR, "apple-touch-icon-180.png"), format="PNG")
apple_152.save(os.path.join(ASSETS_DIR, "apple-touch-icon-152.png"), format="PNG")
apple_167.save(os.path.join(ASSETS_DIR, "apple-touch-icon-167.png"), format="PNG")
apple_120.save(os.path.join(ASSETS_DIR, "apple-touch-icon-120.png"), format="PNG")

print("Generating Android & PWA shortcut icons (192, 512)...")
pwa_192 = render_master_icon(192, is_opaque=True, safe_zone_scale=0.74)
pwa_512 = render_master_icon(512, is_opaque=True, safe_zone_scale=0.74)
pwa_192.save(os.path.join(ROOT_DIR, "icon-192.png"), format="PNG")
pwa_512.save(os.path.join(ROOT_DIR, "icon-512.png"), format="PNG")
pwa_192.save(os.path.join(ASSETS_DIR, "icon-192.png"), format="PNG")
pwa_512.save(os.path.join(ASSETS_DIR, "icon-512.png"), format="PNG")

# Maskable Icons (Android Adaptive Icon safe zone: 65% scale)
maskable_192 = render_master_icon(192, is_opaque=True, safe_zone_scale=0.62)
maskable_512 = render_master_icon(512, is_opaque=True, safe_zone_scale=0.62)
maskable_192.save(os.path.join(ASSETS_DIR, "icon-maskable-192.png"), format="PNG")
maskable_512.save(os.path.join(ASSETS_DIR, "icon-maskable-512.png"), format="PNG")

print("Generating Favicons (ICO and PNG)...")
# Favicons with transparent squircle
fav_16 = render_master_icon(16, is_opaque=False, safe_zone_scale=0.88)
fav_32 = render_master_icon(32, is_opaque=False, safe_zone_scale=0.88)
fav_48 = render_master_icon(48, is_opaque=False, safe_zone_scale=0.88)
fav_16.save(os.path.join(ASSETS_DIR, "favicon-16.png"), format="PNG")
fav_32.save(os.path.join(ASSETS_DIR, "favicon-32.png"), format="PNG")
fav_48.save(os.path.join(ASSETS_DIR, "favicon-48.png"), format="PNG")
fav_48.save(os.path.join(ASSETS_DIR, "favicon.png"), format="PNG")

# Multi-resolution favicon.ico
ico_master = render_master_icon(256, is_opaque=True, safe_zone_scale=0.82)
ico_sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
ico_master.save(os.path.join(ROOT_DIR, "favicon.ico"), format="ICO", sizes=ico_sizes)
ico_master.save(os.path.join(ASSETS_DIR, "favicon.ico"), format="ICO", sizes=ico_sizes)

# 3. GitHub Social Preview (1280 x 640 - Exact GitHub Specs)
print("Generating GitHub Social Preview Card (1280x640)...")
gh_w, gh_h = 1280, 640
gh_bg = Image.new("RGB", (gh_w, gh_h), (11, 16, 27))
gh_draw = ImageDraw.Draw(gh_bg)

# Background subtle ambient glow
glow_layer = Image.new("RGBA", (gh_w, gh_h), (0, 0, 0, 0))
d_glow = ImageDraw.Draw(glow_layer)
d_glow.ellipse([780, -120, 1380, 480], fill=(99, 102, 241, 55))
d_glow.ellipse([-120, 260, 480, 860], fill=(16, 185, 129, 45))
glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(80))
gh_bg.paste(glow_layer, (0, 0), glow_layer)

# Paste prominent logo on right
logo_rendered = render_master_icon(380, is_opaque=True, safe_zone_scale=0.76)
gh_bg.paste(logo_rendered, (800, 130))

# Save GitHub Social Preview & OG Preview
gh_bg.save(os.path.join(ASSETS_DIR, "github-social-preview.png"), format="PNG")
gh_bg.resize((1200, 630), Image.Resampling.LANCZOS).save(os.path.join(ASSETS_DIR, "og-preview.png"), format="PNG")
print("Saved github-social-preview.png and og-preview.png")

print("All master assets generated flawlessly!")
