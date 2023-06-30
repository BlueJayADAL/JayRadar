import math

def filter_center_crosshair(result, tx, ty):
    if not result.boxes:
        return None, False

    closest_box = None
    min_distance = math.inf

    for box in result.boxes:
        cx, cy, w, h = [round(x) for x in box.xywh[0].tolist()]
        distance = math.sqrt((cx - tx)**2 + (cy - ty)**2)

        if distance < min_distance:
            min_distance = distance
            closest_box = box

    return closest_box, True

def filter_max_area(result):
    if not result.boxes:
        return None, False

    max_area = -1
    max_area_box = None

    for box in result.boxes:
        area = box.xywh[0][2] * box.xywh[0][3]

        if area > max_area:
            max_area = area
            max_area_box = box

    return max_area_box, True

def filter_edge_crosshair(result, tx, ty):
    if not result.boxes:
        return None, False

    closest_box = None
    min_distance = math.inf

    for box in result.boxes:
        cx, cy, w, h = [round(x) for x in box.xywh[0].tolist()]

        # Find the closest point on the outside of the box
        closest_x = max(cx - w / 2, min(tx, cx + w / 2))
        closest_y = max(cy - h / 2, min(ty, cy + h / 2))

        distance = math.sqrt((closest_x - tx)**2 + (closest_y - ty)**2)

        if distance < min_distance:
            min_distance = distance
            closest_box = box

    return closest_box, True

