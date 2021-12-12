def solve(polygon, pt):
    ans = False
    for i in range(len(polygon)):
        x0, y0 = polygon[i]
        x1, y1 = polygon[(i + 1) % len(polygon)]
        if not min(y0, y1) < pt[1] <= max(y0, y1):
            continue
        if pt[0] < min(x0, x1):
            continue
        cur_x = x0 if x0 == x1 else x0 + (pt[1] - y0) * (x1 - x0) / (y1 - y0)
        ans ^= pt[0] > cur_x # ^ xor operator, one and only one is True
    return ans

points = [(0, 0), (1, 3), (4, 4), (6, 2), (4, 0)]
Pt = (3, 1)
print(solve(points, Pt))