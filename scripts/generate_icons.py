import os
import math
from PIL import Image, ImageDraw, ImageFilter

ASSETS_DIR = "/Users/manandewan/.gemini/antigravity/scratch/careertracker/assets/images"
os.makedirs(ASSETS_DIR, exist_ok=True)

# 1. Create Pristine SVG Logo
SVG_CONTENT = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="100%" height="100%">
  <defs>
    <!-- Background Gradient -->
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f172a" />
      <stop offset="50%" stop-color="#0b101b" />
      <stop offset="100%" stop-color="#050811" />
    </linearGradient>
    
    <!-- Primary Curve Gradient -->
    <linearGradient id="curveGrad" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#10b981" />
      <stop offset="45%" stop-color="#06b6d4" />
      <stop offset="80%" stop-color="#6366f1" />
      <stop offset="100%" stop-color="#a855f7" />
    </linearGradient>

    <!-- Glow Filter -->
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="16" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>

    <radialGradient id="apexGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="1" />
      <stop offset="40%" stop-color="#6366f1" stop-opacity="0.6" />
      <stop offset="100%" stop-color="#6366f1" stop-opacity="0" />
    </radialGradient>
  </defs>

  <!-- Squircle Base with Border -->
  <rect x="24" y="24" width="464" height="464" rx="112" fill="url(#bgGrad)" stroke="#1e293b" stroke-width="6" />
  
  <!-- Subtle Ambient Glow -->
  <circle cx="360" cy="160" r="140" fill="url(#apexGlow)" opacity="0.3" filter="url(#glow)" />

  <!-- Compounding Baseline Grid Subtlety -->
  <line x1="110" y1="390" x2="402" y2="390" stroke="#334155" stroke-width="3" stroke-dasharray="8 8" opacity="0.4" />
  <line x1="110" y1="310" x2="402" y2="310" stroke="#334155" stroke-width="2" stroke-dasharray="8 8" opacity="0.25" />
  <line x1="110" y1="230" x2="402" y2="230" stroke="#334155" stroke-width="2" stroke-dasharray="8 8" opacity="0.15" />

  <!-- Bar Pillars (compounding wealth accumulation) -->
  <rect x="130" y="340" width="22" height="50" rx="6" fill="#10b981" opacity="0.25" />
  <rect x="180" y="310" width="22" height="80" rx="6" fill="#06b6d4" opacity="0.3" />
  <rect x="230" y="270" width="22" height="120" rx="6" fill="#38bdf8" opacity="0.35" />
  <rect x="280" y="210" width="22" height="180" rx="6" fill="#6366f1" opacity="0.4" />
  <rect x="330" y="140" width="22" height="250" rx="6" fill="#8b5cf6" opacity="0.45" />

  <!-- Upward Compounding Trajectory Curve (Glow + Line) -->
  <path d="M 110 380 Q 220 370 270 280 T 385 130" 
        fill="none" stroke="url(#curveGrad)" stroke-width="28" stroke-linecap="round" filter="url(#glow)" opacity="0.6" />
  <path d="M 110 380 Q 220 370 270 280 T 385 130" 
        fill="none" stroke="url(#curveGrad)" stroke-width="18" stroke-linecap="round" />

  <!-- Apex Star / Beacon Node -->
  <circle cx="385" cy="130" r="28" fill="#ffffff" opacity="0.2" filter="url(#glow)" />
  <circle cx="385" cy="130" r="16" fill="#ffffff" />
  <circle cx="385" cy="130" r="10" fill="#38bdf8" />
  
  <!-- Minimalist Arrow Accent at Apex -->
  <path d="M 385 96 L 415 126 L 385 156" fill="none" stroke="#38bdf8" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" />
</svg>
"""

svg_path = os.path.join(ASSETS_DIR, "logo.svg")
with open(svg_path, "w", encoding="utf-8") as f:
    f.write(SVG_CONTENT)
print(f"Wrote {svg_path}")

# 2. Function to Render High Quality Raster Icons
def render_icon(size):
    # Render at 4x for supersampling / crisp anti-aliasing
    scale = 4
    canvas_size = size * scale
    img = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background Squircle
    pad = int(24 * (canvas_size / 512.0))
    radius = int(112 * (canvas_size / 512.0))
    
    # Draw dark background rounded rectangle
    draw.rounded_rectangle(
        [pad, pad, canvas_size - pad, canvas_size - pad],
        radius=radius,
        fill=(11, 16, 27, 255),
        outline=(30, 41, 59, 255),
        width=int(6 * (canvas_size / 512.0))
    )

    # Subtle Pillar Bars
    bars = [
        (130, 340, 22, 50, (16, 185, 129, 64)),
        (180, 310, 22, 80, (6, 182, 212, 76)),
        (230, 270, 22, 120, (56, 189, 248, 90)),
        (280, 210, 22, 180, (99, 102, 241, 105)),
        (330, 140, 22, 250, (139, 92, 246, 120)),
    ]
    for bx, by, bw, bh, col in bars:
        sx = int(bx * (canvas_size / 512.0))
        sy = int(by * (canvas_size / 512.0))
        sw = int(bw * (canvas_size / 512.0))
        sh = int(bh * (canvas_size / 512.0))
        draw.rounded_rectangle([sx, sy, sx + sw, sy + sh], radius=int(6 * canvas_size / 512.0), fill=col)

    # Compounding Curve Points
    curve_pts = []
    steps = 100
    p0 = (110.0, 380.0)
    p1 = (220.0, 370.0)
    p2 = (270.0, 280.0)
    p3 = (385.0, 130.0)

    # Cubic / Bezier curve
    for t_i in range(steps + 1):
        t = t_i / float(steps)
        # 2-segment smooth spline approximation
        if t <= 0.5:
            u = t * 2.0
            x = (1 - u) * (1 - u) * p0[0] + 2 * (1 - u) * u * p1[0] + u * u * p2[0]
            y = (1 - u) * (1 - u) * p0[1] + 2 * (1 - u) * u * p1[1] + u * u * p2[1]
        else:
            u = (t - 0.5) * 2.0
            # symmetric continuation to p3
            ctrl_x = 2 * p2[0] - p1[0]
            ctrl_y = 2 * p2[1] - p1[1]
            x = (1 - u) * (1 - u) * p2[0] + 2 * (1 - u) * u * ctrl_x + u * u * p3[0]
            y = (1 - u) * (1 - u) * p2[1] + 2 * (1 - u) * u * ctrl_y + u * u * p3[1]
        
        curve_pts.append((x * (canvas_size / 512.0), y * (canvas_size / 512.0)))

    # Draw glow line
    glow_width = int(24 * (canvas_size / 512.0))
    for i in range(len(curve_pts) - 1):
        frac = i / float(len(curve_pts))
        r = int(16 + frac * (168 - 16))
        g = int(185 - frac * (185 - 85))
        b = int(129 + frac * (247 - 129))
        draw.line([curve_pts[i], curve_pts[i+1]], fill=(r, g, b, 80), width=glow_width)

    # Draw core crisp line
    core_width = int(14 * (canvas_size / 512.0))
    for i in range(len(curve_pts) - 1):
        frac = i / float(len(curve_pts))
        r = int(16 + frac * (168 - 16))
        g = int(185 - frac * (185 - 85))
        b = int(129 + frac * (247 - 129))
        draw.line([curve_pts[i], curve_pts[i+1]], fill=(r, g, b, 255), width=core_width)

    # Draw Apex Beacon Node
    apex_x = int(385 * (canvas_size / 512.0))
    apex_y = int(130 * (canvas_size / 512.0))
    r_outer = int(22 * (canvas_size / 512.0))
    r_mid = int(14 * (canvas_size / 512.0))
    r_inner = int(8 * (canvas_size / 512.0))

    draw.ellipse([apex_x - r_outer, apex_y - r_outer, apex_x + r_outer, apex_y + r_outer], fill=(56, 189, 248, 100))
    draw.ellipse([apex_x - r_mid, apex_y - r_mid, apex_x + r_mid, apex_y + r_mid], fill=(255, 255, 255, 255))
    draw.ellipse([apex_x - r_inner, apex_y - r_inner, apex_x + r_inner, apex_y + r_inner], fill=(56, 189, 248, 255))

    # Downsample with Lanczos for anti-aliasing
    final_img = img.resize((size, size), Image.Resampling.LANCZOS)
    return final_img

# Generate all standard icon sizes
SIZES = {
    "apple-touch-icon.png": 180,
    "icon-192.png": 192,
    "icon-512.png": 512,
    "favicon-32.png": 32,
    "favicon-16.png": 16
}

for filename, sz in SIZES.items():
    out_img = render_icon(sz)
    path = os.path.join(ASSETS_DIR, filename)
    out_img.save(path, format="PNG")
    print(f"Generated {path} ({sz}x{sz})")

# Also save standard favicon.ico / favicon.png
out_img = render_icon(48)
out_img.save(os.path.join(ASSETS_DIR, "favicon.png"), format="PNG")

# Generate Open Graph Social Preview Card (1200 x 630)
def generate_og_card():
    width, height = 1200, 630
    bg = Image.new("RGBA", (width, height), (11, 16, 27, 255))
    draw = ImageDraw.Draw(bg)

    # Gradient background glow circles
    glow_teal = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    d_teal = ImageDraw.Draw(glow_teal)
    d_teal.ellipse([800, -100, 1300, 400], fill=(99, 102, 241, 40))
    d_teal.ellipse([-100, 300, 400, 800], fill=(16, 185, 129, 35))
    glow_teal = glow_teal.filter(ImageFilter.GaussianBlur(80))
    bg = Image.alpha_composite(bg, glow_teal)

    # Paste rendered 512 icon resized to 360x360 on the right
    icon = render_icon(360)
    bg.paste(icon, (760, 135), icon)

    # Save og image
    og_path = os.path.join(ASSETS_DIR, "og-preview.png")
    bg.save(og_path, format="PNG")
    print(f"Generated {og_path} (1200x630)")

generate_og_card()
print("All icon assets generated successfully!")
