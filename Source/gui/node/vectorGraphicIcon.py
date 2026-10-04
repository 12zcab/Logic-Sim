pad = min(w, h) * 0.1
x0, y0 = x + pad, y + pad
x1, y1 = x + w - pad, y + h - pad
mid_x, mid_y = x + w / 2, y + h / 2

pts = [
    (x0, y0),
    (x0 + (w - 2 * pad) * 0.5, y0),
    (x1, mid_y),
    (x0 + (w - 2 * pad) * 0.5, y1),
    (x0, y1)
]

if angle != 0:
    pts = [rotatePoint(px, py, cx, cy, angle) for px, py in pts]

flat_pts = [coord for pt in pts for coord in pt]

canvas.create_polygon(flat_pts, fill="#BB86FC", outline="#FFFFFF", width=2, tags=tags)

center_pt = (mid_x, mid_y)
if angle != 0:
    center_pt = rotatePoint(mid_x, mid_y, cx, cy, angle)

r = min(w, h) * 0.1
canvas.create_oval(
    center_pt[0] - r, center_pt[1] - r, center_pt[0] + r, center_pt[1] + r,
    fill="#00ADB5", outline="#FFFFFF", width=1, tags=tags
)