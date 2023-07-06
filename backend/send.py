import math
import threading
import cv2
from collections import deque
from detection import result_queue
from capture import frame_queue, process_event
from constants import MAX_FRAMES

filtered_queue = deque(maxlen=MAX_FRAMES)

filtered_event = threading.Event()

def filter_center_crosshair(result, tx, ty):
    if not result:
        return None, False

    closest_box = None
    min_distance = math.inf

    for box in result:
        cx, cy, w, h, _ = box
        distance = math.sqrt((cx - tx)**2 + (cy - ty)**2)

        if distance < min_distance:
            min_distance = distance
            closest_box = box

    return closest_box, True

def filter_max_area(result):
    if not result:
        return None, False

    max_area = -1
    max_area_box = None

    for box in result:
        _, _, w, h, _ = box
        area = w * h

        if area > max_area:
            max_area = area
            max_area_box = box

    return max_area_box, True

def filter_edge_crosshair(result, tx, ty):
    if not result:
        return None, False

    closest_box = None
    min_distance = math.inf

    for box in result:
        cx, cy, w, h, _ = box

        # Find the closest point on the outside of the box
        closest_x = max(cx - w / 2, min(tx, cx + w / 2))
        closest_y = max(cy - h / 2, min(ty, cy + h / 2))

        distance = math.sqrt((closest_x - tx)**2 + (closest_y - ty)**2)

        if distance < min_distance:
            min_distance = distance
            closest_box = box

    return closest_box, True
def draw_bounding_box(frame, x, y, w, h):
    x1, y1 = int(x - w/2), int(y - h/2)  # Calculate top-left corner coordinates
    x2, y2 = int(x + w/2), int(y + h/2)  # Calculate bottom-right corner coordinates

    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw the bounding box

    return frame

def draw_crosshair(frame, x, y):
    cv2.drawMarker(frame, (x, y), (0, 0, 255), cv2.MARKER_CROSS, 5, 2)
    return frame

def send_filtered_results():
    while True:
        process_event.wait()
        process_event.clear()
        if frame_queue and result_queue:

            frame = frame_queue[-1].copy()
            results = result_queue[-1]
            result, success = filter_edge_crosshair(results, 320, 240)
            crosshair_frame = draw_crosshair(frame, 320, 240)
            if success:
                final_frame = draw_bounding_box(crosshair_frame, result[0], result[1], result[2], result[3])
            else:
                final_frame = crosshair_frame
            
            filtered_queue.append(final_frame)

            filtered_event.set()