"""Part 1: base utilities and draw_variant1 (front-page layout)."""

import sys
from PIL import Image, ImageDraw, ImageFont

FONT_BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

_PAPER = "#F7F1E3"
_INK = "#14213D"
_RED = "#C1272D"
_NAVY = "#1B2A4A"
_TEAL = "#0E7C7B"
_GOLD = "#D9A441"
_LIGHT = "#36455F"

_CATEGORY_COLORS = {
    "CHESS": "#C1272D",
    "SPACE": "#1B2A4A",
    "Soccer": "#0E7C7B",
    "Football": "#0E7C7B",
    "Politics": "#1B2A4A",
    "Weather": "#0E7C7B",
    "Markets": "#D9A441",
    "Ticker": "#D9A441",
    "Vatican": "#1B2A4A",
    "Power": "#0E7C7B",
    "Media": "#C1272D",
}



def _category_color(category):
    return _CATEGORY_COLORS.get(category, "#1B2A4A")


def font_bold(size):
    return ImageFont.truetype(FONT_BOLD_PATH, int(size))


def font_regular(size):
    return ImageFont.truetype(FONT_REG_PATH, int(size))



def wrap_text(draw, text, font, max_width):
    words = text.split(" ")
    lines = []
    current = ""
    for word in words:
        test = (current + " " + word).strip()
        if draw.textlength(test, font=font) <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines



def draw_wrapped(draw, xy, lines, font, fill, leading):
    x, y = int(xy[0]), int(xy[1])
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += int(leading)
    return y



def draw_chip(draw, xy, label, bg, fg="white", pad=6, font_size=12):
    font = font_bold(font_size)
    tw = int(draw.textlength(label, font=font))
    th = int(font_size * 1.15)
    x, y = int(xy[0]), int(xy[1])
    w = tw + pad * 2
    h = th + pad
    radius = h // 2
    draw.rounded_rectangle([x, y, x + w, y + h], radius=radius, fill=bg)
    draw.text((x + pad, y + (h - th) // 2 - 1), label, font=font, fill=fg)
    return (w, h)



def draw_icon(draw, kind, bbox, accent):
    left, top, right, bottom = bbox
    cx = (left + right) // 2
    cy = (top + bottom) // 2
    w = right - left
    h = bottom - top
    mini = min(w, h)
    if kind == "chess":
        corner = int(mini * 0.22)
        base = int(mini * 0.06)
        stem_top = top + int(mini * 0.28)
        stem_bot = bottom - int(mini * 0.10)
        head_base = bottom - int(mini * 0.24)
        draw.rectangle([cx - corner, stem_top, cx + corner, head_base], fill=accent)
        draw.rectangle([cx - corner - base, head_base, cx + corner + base, head_base + base], fill=accent)
        draw.rectangle([cx - corner - base, bottom - base, cx + corner + base, bottom], fill=accent)
        draw.ellipse([cx - corner, stem_top - int(corner * 0.95), cx + corner, stem_top + int(corner * 0.6)], fill=accent)
    elif kind == "space":
        R = int(mini * 0.35)
        draw.ellipse([cx - int(mini * 0.30), top + int(mini * 0.10), cx + int(mini * 0.22), top + int(mini * 0.60)], outline=accent, width=max(2, mini // 20))
        draw.ellipse([cx - R, cy - R, cx + R, cy + R], outline=accent, width=max(2, mini // 22))
        sx = cx - int(mini * 0.20)
        sy = cy - int(mini * 0.22)
        for (dx, dy) in [(0, 0), (5, 4), (-5, 3), (3, -5), (-3, -5), (8, 8), (10, 2)]:
            draw.ellipse([sx + dx - 2, sy + dy - 2, sx + dx + 2, sy + dy + 2], fill=accent)
    elif kind == "football":
        r = int(mini * 0.34)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=accent, width=max(2, mini // 24))
        for ang_deg in range(0, 360, 72):
            import math
            rad = ang_deg * 3.141592653589793 / 180
            px = int(cx + r * 0.8 * (0.983 * (1 - math.sin(rad)) ))
            py = int(cy + r * 0.8 * 0.5)
            tw = 8
            th = 10
            draw.polygon([px, py - tw, px + th, py, px, py + tw, px - th, py], outline=accent, width=2)
        for a in range(5):
            import math
            rad = (a * 72 - 90) * 3.141592653589793 / 180
            ax = int(cx + r * 0.55 * (0.983 * -math.sin(rad) ))
            ay = int(cy + r * 0.55 * math.cos(rad)
                     )
            draw.line([cx, cy, ax, ay], fill=accent, width=2)
            draw.ellipse([ax - 2, ay - 2, ax + 2, ay + 2], fill=accent)
    elif kind == "politics":
        import math
        base_y = bottom - int(mini * 0.08)
        left_x = int(left + mini * 0.10)
        columns = [
            (int(cx - mini * 0.22), int(mini * 0.35)),
            (int(cx), int(mini * 0.50)),
            (int(cx + mini * 0.22), int(mini * 0.35)),
        ]
        for i, (px, pw) in enumerate(columns):
            top_y = base_y - int(mini * 0.42)
            heads_y = top_y - int(mini * 0.10)
            draw.rectangle([px - pw // 4, top_y, px + pw // 4, base_y], fill=accent)
            draw.ellipse([px - pw // 2, heads_y, px + pw // 2, heads_y + pw // 2], fill=accent)
            legs_y = base_y + int(mini * 0.08)
            lw = pw // 5
            draw.rectangle([px - lw, base_y - pw // 3, px - lw // 2, legs_y], fill=accent)
            draw.rectangle([px + lw // 2 + 1, base_y - pw // 3, px + lw, legs_y], fill=accent)
    elif kind == "weather":
        cloud_w = int(mini * 0.75)
        cloud_h = int(mini * 0.38)
        top_y = top + int(mini * 0.10)
        cloud_left = cx - cloud_w // 2
        draw.ellipse([cloud_left, top_y, cloud_left + cloud_w // 2, top_y + cloud_h], fill=accent)
        draw.ellipse([cloud_left + cloud_w // 3, top_y - int(cloud_h * 0.35), cloud_left + int(cloud_w * 0.75), top_y + int(cloud_h * 0.65)], fill=accent)
        draw.rectangle([cloud_left, top_y + cloud_h // 3, cloud_left + cloud_w, top_y + cloud_h], fill=accent)
        for (ox, ln) in [(-int(mini * 0.12), int(mini * 0.17)), (0, int(mini * 0.24)), (int(mini * 0.12), int(mini * 0.17))]:
            draw.line([cx + ox, top_y + cloud_h, cx + ox, top_y + cloud_h + ln], fill=accent, width=3)
    elif kind == "markets":
        import math
        bars = [
            (int(cx - mini * 0.30), int(mini * 0.40)),
            (int(cx - mini * 0.12), int(mini * 0.62)),
            (int(cx + mini * 0.06), int(mini * 0.33)),
            (int(cx + mini * 0.24), int(mini * 0.53)),
        ]
        for (bx, bh) in bars:
            draw.rectangle([bx, bottom - bh, bx + int(mini * 0.10), bottom], fill=accent)


def draw_variant1(size=1024):
    s = int(size)
    img = Image.new("RGB", (s, s), _PAPER)
    draw = ImageDraw.Draw(img)

    mast_h = int(s * 0.10)
    date_h = int(s * 0.055)
    lead_h = int(s * 0.235)
    grid_h = int(s * 0.40)
    ticker_h = int(s * 0.075)
    footer_h = int(s * 0.05)
    pad = int(s * 0.03)

    # Masthead
    draw.rectangle([0, 0, s, mast_h], fill=_NAVY)
    title_font = font_bold(int(mast_h * 0.34))
    tag_font = font_regular(int(mast_h * 0.18))
    title = "THE WORLD IN ONE IMAGE"
    tag = "Front page of today -> Tuesday 24 November 2026"
    tw = draw.textlength(title, font=title_font)
    tgw = draw.textlength(tag, font=tag_font)
    draw.text(((s - tw) // 2, int(mast_h * 0.22)), title, font=title_font, fill="white")
    draw.text(((s - tgw) // 2 + int(s * 0.12), mast_h - int(mast_h * 0.22) - int(tag_font.size)), tag, font=tag_font, fill=_GOLD)

    # Date band
    top_date = mast_h
    draw.rectangle([0, top_date, s, top_date + date_h], fill=_PAPER)
    d_font = font_bold(int(date_h * 0.38))
    d_lab_font = font_bold(int(date_h * 0.22))
    date_txt = "TUESDAY, 24 NOVEMBER 2026"
    lab = "FRONT PAGE" 
    dl = draw.textlength(date_txt, font=d_font)
    ll = draw.textlength(lab, font=d_lab_font)
    x1 = int(s * 0.05)
    draw.text((x1, top_date + (date_h - d_font.size) // 2 - 4), lab, font=d_lab_font, fill=_RED)
    draw.text((x1 + int(s * 0.10), top_date + (date_h - d_font.size) // 2 - 4), date_txt, font=d_font, fill=_INK)
    bar_x = s - int(s * 0.05)
    bar_w = int(s * 0.30)
    bar_y = top_date + int(date_h * 0.3)
    draw.rounded_rectangle([bar_x - bar_w, bar_y, bar_x, bar_y + int(date_h * 0.4)], radius=8, fill=_GOLD)
    b_txt = "CHESS - SPACE - SOCCER - POLITICS - WEATHER"
    b_font = font_bold(int(date_h * 0.2))
    btl = draw.textlength(b_txt, font=b_font)
    draw.text((int(bar_x - btl / 2), bar_y + 2), b_txt, font=b_font, fill="white")

    # Lead story
    lead_top = top_date + date_h
    lead_bot = lead_top + lead_h
    head_font = font_bold(int(lead_h * 0.15))
    dek_font = font_regular(int(lead_h * 0.075))
    chip_label = "WORLD CHESS CHAMPIONSHIP"
    chip_color = "#C1272D"
    head = "World Chess Championship Game 1 begins today in Geneva - The 20-year-old Gukesh Dommaraju defends his title against Javokhir Sindarov. The youngest match in history (both players 20) is a 14-game contest with a $2.5M prize fund, and the first move is at 15:00 CET."
    draw_chip(draw, (pad, lead_top + int(lead_h * 0.03)), chip_label, chip_color, font_size=int(lead_h * 0.055))
    max_w = s - pad * 2
    hh = wrap_text(draw, head, head_font, max_w - int(s * 0.07))
    dek = "Sindarov has White in Game 1; first to 7.5 points over 14 games takes the crown."
    lines = wrap_text(draw, dek, dek_font, max_w)
    draw_wrapped(draw, (pad, lead_top + int(lead_h * 0.14)), hh, head_font, _INK, int(lead_h * 0.17))
    draw_wrapped(draw, (pad, lead_top + int(lead_h * 0.62)), lines, dek_font, _LIGHT, int(lead_h * 0.09))
    icon_rect = [s - pad - int(lead_h * 0.32), lead_top + int(lead_h * 0.03), s - pad, lead_top + int(lead_h * 0.62)]
    draw_icon(draw, "chess", icon_rect, "#C1272D")

    # 2x2 grid for stories 2-5
    grid_top = lead_bot + int(s * 0.01)
    grid_bot = grid_top + grid_h
    card_gap = int(s * 0.02)
    card_w = int((s - pad * 2 - card_gap) / 2)
    card_h = int((grid_h - card_gap) / 2)
    stories = [
        {"key": "SPACE", "cat": "SPACE", "accent": _NAVY, "head": "The Beaver Supermoon peaks at 9:53 AM ET".upper(),
         "dek": "0.9 degrees from the Pleiades cluster (the Seven Sisters); closest approach follows on 25 Nov. The first of three straight supermoons into January 2027."},
        {"key": "FOOTBALL", "cat": "Soccer", "accent": _TEAL, "head": "FIFA confirms the Women's World Cup hosts".upper(),
         "dek": "USA, Mexico, Costa Rica and Jamaica stage the first 48-team edition of 2031. England, Scotland, Wales and Northern Ireland host 2035."},
        {"key": "POLITICS", "cat": "Politics", "accent": _NAVY, "head": "Portugal's parliament holds its final vote on the 2027 budget today".upper(),
         "dek": "CGTP unions rally outside after the mass Lisbon march against living costs, low wages and the housing crisis."},
        {"key": "WEATHER", "cat": "Weather", "accent": _TEAL, "head": "Freeze warnings cover Texas overnight into 25 Nov".upper(),
         "dek": "A Thanksgiving storm bears down on the US East Coast with heavy rain, 50 mph gusts, and coastal flooding from the Carolinas to New England."},
    ]
    for idx, item in enumerate(stories):
        row = idx // 2
        col = idx % 2
        cx0 = int(pad + col * (card_w + card_gap))
        cy0 = int(grid_top + row * (card_h + card_gap))
        bgx = (cx0, cy0, cx0 + card_w, cy0 + card_h)
        draw.rounded_rectangle(bgx, radius=int(card_h * 0.03), outline=_NAVY, width=2, fill=_PAPER)
        chip_x = cx0 + int(card_w * 0.02)
        chip_font = 14
        acen = _category_color(item["cat"])
        draw_chip(draw, (chip_x, cy0 + int(card_h * 0.04)), item["cat"].upper(), acen, font_size=chip_font)
        headf = font_bold(int(card_h * 0.125))
        dekf = font_regular(int(card_h * 0.09))
        lead_icon = {
            "SPACE": "space",
            "FOOTBALL": "football",
            "POLITICS": "politics",
            "WEATHER": "weather",
        }[item["key"]]
        icon_rect = [int(cx0 + card_w * 0.03), int(cy0 + card_h * 0.13), int(cx0 + card_w * 0.11), int(cy0 + card_h * 0.25)]
        draw_icon(draw, lead_icon, icon_rect, acen)
        head_lines = wrap_text(draw, item["head"], headf, card_w - int(card_w * 0.06))
        deck_lines = wrap_text(draw, item["dek"], dekf, card_w - int(card_w * 0.06))

        y = cy0 + int(card_h * 0.30)
        for ln in head_lines[:2]:
            draw.text((chip_x, y), ln, font=headf, fill=_INK)
            y += int(headf.size * 1.25)
        y += int(card_h * 0.03)
        for ln in deck_lines[:2]:
            draw.text((chip_x, y), ln, font=dekf, fill=_LIGHT)
            y += int(dekf.size * 1.3)

    # Ticker strip
    tk_top = grid_bot + int(s * 0.015)
    tk_bot = tk_top + ticker_h
    draw.rectangle([0, tk_top, s, tk_bot], fill=_GOLD)
    tk_lab_font = font_bold(int(ticker_h * 0.5))
    tk_body_font = font_regular(int(ticker_h * 0.33))
    tk_lab = "TICKER -"
    tk_body = "Vatican assembly (24-26 Nov); Chennai 5-hr power cut (maintenance); NIJISANJI POPCORN VOL.4: ON SALE TODAY IN JAPAN."
    draw.text((int(s * 0.03), tk_top + int(ticker_h * 0.25)), tk_lab, font=tk_lab_font, fill=_INK)
    x0 = int(s * 0.03) + int(draw.textlength(tk_lab, font=tk_lab_font)) + int(s * 0.01)
    x1 = s - int(s * 0.03)
    # Draw body with a light shade background so it reads on gold
    twb = draw.textlength(tk_body, font=tk_body_font)
    thb = int(tk_body_font.size)
    yb = tk_top + int((ticker_h - thb) / 2)
    draw.text((x0, yb), tk_body, font=tk_body_font, fill=_INK)

    # Footer
    foot_font = font_bold(int(footer_h * 0.55))
    foot_txt = "All stories first reported 24 November 2026."
    ftl = draw.textlength(foot_txt, font=foot_font)
    fy = tk_bot + int(footer_h * 0.2)
    draw.text(((s - ftl) / 2, fy), foot_txt, font=foot_font, fill=_INK)

    return img


def main():
    variant = sys.argv[1] if len(sys.argv) > 1 else "1"
    draw_func = globals().get("draw_variant" + variant)
    if draw_func is None:
        raise SystemExit("unknown variant: " + variant)
    img = draw_func()
    out = "variant_" + str(variant) + ".png"
    img.save(out)
    print("wrote %s 1024x1024 bytes %d" % (out, len(img.tobytes())))


def _icon_for_category(category):
    m = {
        "CHESS": "chess",
        "SPACE": "space",
        "Soccer": "football",
        "Football": "football",
        "Politics": "politics",
        "Weather": "weather",
        "Markets": "markets",
        "Ticker": "markets",
        "Vatican": "politics",
        "Power": "weather",
        "Media": "politics",
    }
    return m.get(category, "politics")


def _icon_for_key(key):
    m = {
        "CHESS": "chess",
        "SPACE": "space",
        "FOOTBALL": "football",
        "POLITICS": "politics",
        "WEATHER": "weather",
        "MARKETS": "markets",
        "TICKER": "markets",
    }
    return m.get(key, "politics")


_STORY_DATA_6 = [
    {"key": "CHESS", "cat": "CHESS", "head": "CHESS: Championship Game 1 in Geneva",
     "dek": "Gukesh (20) defends title vs Sindarov (20) - $2.5M prize, 15:00 CET."},
    {"key": "SPACE", "cat": "SPACE", "head": "Beaver Supermoon peaks 9:53 AM ET",
     "dek": "Within 0.9 degrees of the Pleiades; first of 3 supermoons into Jan 2027."},
    {"key": "FOOTBALL", "cat": "Soccer", "head": "FIFA confirms Women's Cup hosts",
     "dek": "USA, Mexico, Costa Rica, Jamaica 2031; UK nations 2035 (48-team era)."},
    {"key": "POLITICS", "cat": "Politics", "head": "Portugal final vote on 2027 budget",
     "dek": "CGTP unions rally after Lisbon march on costs, wages and housing."},
    {"key": "WEATHER", "cat": "Weather", "head": "Freeze warning: Texas / NE storm",
     "dek": "Tex freeze overnight; 50-mph gusts and coastal flooding, Carolinas-NE."},
    {"key": "MARKETS", "cat": "Markets", "head": "India markets closed for Guru Nanak Jayanti",
     "dek": "Markets shut for Guru Nanak Jayanti, a day after the Sensex slid 1,484 (-1.77%) to 82,436."},
]


def draw_variant2(size=1024):
    s = int(size)
    img = Image.new("RGB", (s, s), _PAPER)
    draw = ImageDraw.Draw(img)

    pad = int(s * 0.03)
    banner_h = int(s * 0.085)
    foot_h = int(s * 0.045)
    grid_top = int(s * 0.10)
    grid_bot = s - foot_h - int(s * 0.015)

    draw.rectangle([0, 0, s, banner_h], fill=_NAVY)
    bf = font_bold(int(banner_h * 0.42))
    draw.text(((s - draw.textlength("TUESDAY 24 NOVEMBER 2026", font=bf)) // 2, int(banner_h * 0.28)),
              "TUESDAY 24 NOVEMBER 2026", font=bf, fill="white")
    subf = font_regular(int(banner_h * 0.2))
    sub = "6 stories - one image - the world in a glance"
    draw.text(((s - draw.textlength(sub, font=subf)) // 2, int(banner_h * 0.72)), sub, font=subf, fill=_GOLD)

    rows = 2
    cols = 3
    gap = int(s * 0.02)
    usable_w = s - pad * 2
    usable_h = grid_bot - grid_top
    cell_w = int((usable_w - gap * (cols - 1)) / cols)
    cell_h = int((usable_h - gap * (rows - 1)) / rows)

    for idx, item in enumerate(_STORY_DATA_6):
        r = idx // cols
        c = idx % cols
        x0 = int(pad + c * (cell_w + gap))
        y0 = int(grid_top + r * (cell_h + gap))
        x1 = x0 + cell_w
        y1 = y0 + cell_h
        draw.rounded_rectangle([x0, y0, x1, y1], radius=int(cell_h * 0.04), fill="white", outline=_NAVY, width=2)
        acen = _category_color(item["cat"])
        ix = x0 + int(cell_w * 0.04)
        iy = y0 + int(cell_h * 0.07)
        iw = int(cell_h * 0.26)
        ih = int(cell_h * 0.26)
        draw_icon(draw, _icon_for_key(item["key"]), (ix, iy, ix + iw, iy + ih), acen)
        draw_chip(draw, (x1 - int(cell_w * 0.04) - 7, y0 + int(cell_h * 0.09)), item["cat"].upper(), acen, font_size=14)
        hx = x0 + int(cell_w * 0.04)
        hd = x1 - int(cell_w * 0.04)
        headf = font_bold(int(cell_h * 0.095))
        text_x = hx + int(cell_w * 0.30)
        text_pad_r = int(cell_w * 0.05)
        hl = wrap_text(draw, item["head"], headf, hd - (hd - text_x) - text_pad_r - 8)
        y = iy + int(cell_h * 0.02)
        for ln in hl[:2]:
            draw.text((text_x, y), ln, font=headf, fill=_INK)
            y += int(headf.size * 1.2)
        dekf = font_regular(int(cell_h * 0.075))
        dy = y1 - int(cell_h * 0.42)
        dl = wrap_text(draw, item["dek"], dekf, hd - (hd - text_x) - text_pad_r)
        for ln in dl[:2]:
            draw.text((text_x, dy), ln, font=dekf, fill=_LIGHT)
            dy += int(dekf.size * 1.2)

    ff = font_bold(int(foot_h * 0.55))
    ft = "All stories first reported 24 November 2026."
    draw.text(((s - draw.textlength(ft, font=ff)) / 2, int(s - foot_h + foot_h * 0.25)), ft, font=ff, fill=_INK)
    return img


def draw_variant3(size=1024):
    s = int(size)
    img = Image.new("RGB", (s, s), _PAPER)
    draw = ImageDraw.Draw(img)

    pad = int(s * 0.04)
    date_h = int(s * 0.06)
    headline_block = int(s * 0.16)
    rule_gap = int(s * 0.012)
    briefs_top = date_h + int(s * 0.015) + headline_block + int(s * 0.015)
    brief_rows = 5
    remaining = s - briefs_top - int(s * 0.07) - int(s * 0.01)
    row_h = int(remaining / brief_rows)

    draw.rectangle([0, 0, s, date_h], fill=_NAVY)
    df = font_bold(int(date_h * 0.5))
    draw.text((pad, int(date_h * 0.15)), "TUESDAY 24 NOVEMBER 2026", font=df, fill="white")
    rf = font_regular(int(date_h * 0.3))
    draw.text((s - pad - draw.textlength("6 STORIES", font=rf), int(date_h * 0.32)), "6 STORIES", font=rf, fill=_GOLD)

    hy0 = date_h + int(s * 0.015)
    hy1 = hy0 + headline_block
    draw.rounded_rectangle([pad, hy0, s - pad, hy1], radius=10, fill="white", outline=_NAVY, width=3)

    acc1 = _category_color("CHESS")
    ciw = int(headline_block * 0.42)
    cix0 = pad + int(headline_block * 0.18)
    ciy0 = hy0 + (headline_block - ciw) // 2
    draw_icon(draw, "chess", (cix0, ciy0, cix0 + ciw, ciy0 + ciw), acc1)
    text_x = cix0 + ciw + int(headline_block * 0.08)
    hf = font_bold(int(headline_block * 0.17))
    hl = wrap_text(draw, _STORY_DATA_6[0]["head"], hf, (s - pad) - text_x - int(headline_block * 0.06))
    dxf = font_regular(int(headline_block * 0.09))
    dl = wrap_text(draw, _STORY_DATA_6[0]["dek"], dxf, (s - pad) - text_x - int(headline_block * 0.06))
    # vertical centering with exact per-section heights (chip removed: headline already says CHESS)
    total_h = min(len(hl), 3) * int(hf.size * 1.15) + int(headline_block * 0.05) + min(len(dl), 3) * int(dxf.size * 1.2)
    y = hy0 + max(0, (headline_block - total_h) // 2)
    for ln in hl[:3]:
        draw.text((text_x, y), ln, font=hf, fill=_INK)
        y += int(hf.size * 1.15)
    y += int(headline_block * 0.05)
    for ln in dl[:3]:
        draw.text((text_x, y), ln, font=dxf, fill=_LIGHT)
        y += int(dxf.size * 1.2)

    rule_y = hy1 + int(s * 0.01)
    draw.line([pad, rule_y, s - pad, rule_y], fill=_RED, width=4)

    for i, item in enumerate(_STORY_DATA_6[1:]):
        ry0 = int(briefs_top + i * row_h)
        ry1 = ry0 + row_h
        draw.rounded_rectangle([pad, ry0, s - pad, ry1], radius=8, fill="white", outline=_LIGHT, width=2)
        ac = _category_color(item["cat"])
        chw = int(row_h * 0.72)
        chx0 = int(pad + row_h * 0.5)
        chy0 = ry0 + int(row_h * 0.08)
        draw_icon(draw, _icon_for_key(item["key"]), (chx0, chy0, chx0 + chw, chy0 + chw), ac)
        draw_chip(draw, (s - pad - int(row_h * 0.9), ry0 + int(row_h * 0.14)), item["cat"].upper(), ac, font_size=14)
        bx0 = chx0 + chw + int(row_h * 0.2)
        bx1 = s - pad - int(row_h * 1.15)
        bhf = font_bold(int(row_h * 0.22))
        bl = wrap_text(draw, item["head"], bhf, bx1 - bx0 - 8)
        bdf = font_regular(int(row_h * 0.18))
        dl = wrap_text(draw, item["dek"], bdf, bx1 - bx0 - 8)
        # vertical centering with exact per-section heights so the block never exceeds the row
        n_head = min(len(bl), 2)
        n_dek = min(len(dl), 2)
        block_h = n_head * int(bhf.size * 1.15) + int(row_h * 0.04) + n_dek * int(bdf.size * 1.2)
        y = ry0 + max(0, (row_h - block_h) // 2)
        for ln in bl[:2]:
            draw.text((bx0, y), ln, font=bhf, fill=_INK)
            y += int(bhf.size * 1.15)
        y += int(row_h * 0.04)
        for ln in dl[:2]:
            draw.text((bx0, y), ln, font=bdf, fill=_LIGHT)
            y += int(bdf.size * 1.2)

    tk_top = s - int(s * 0.07)
    tk_bot = s - int(s * 0.015)
    draw.rectangle([0, tk_top, s, tk_bot], fill=_GOLD)
    tkl = font_bold(int((tk_bot - tk_top) * 0.4))
    tgl = font_regular(int((tk_bot - tk_top) * 0.34))
    lab_x = int(s * 0.02)
    lab_y = int((tk_top + tk_bot) / 2) - int(tkl.size // 2)
    draw.text((lab_x, lab_y), "TICKER", font=tkl, fill=_INK)
    lab_w = int(draw.textlength("TICKER", font=tkl))
    gap = int(s * 0.015)
    x0 = lab_x + lab_w + gap
    x1 = s - int(s * 0.03)
    t1_l = wrap_text(draw, "Vatican dialogue opens in Rome (24-26 Nov);  Chennai 5-hr power cut (maintenance); NIJISANJI POPCORN VOL.4: ON SALE TODAY IN JAPAN.", tgl, x1 - x0 - 8)[:1]
    if t1_l:
        body_y = int((tk_top + tk_bot) / 2) - int(tgl.size // 2)
        draw.text((x0, body_y), t1_l[0], font=tgl, fill=_INK)

    return img

if __name__ == "__main__":
    main()
