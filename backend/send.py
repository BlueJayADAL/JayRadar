import math
from collections import deque
from detection import result_queue, times_queue, results_event
from constants import MAX_FRAMES, MAX_TIMES, NT_SERVER_IP, TABLE_NAME
from networktables import NetworkTables

filtered_queue = deque(maxlen=MAX_FRAMES)

NetworkTables.initialize(server=NT_SERVER_IP)

# Retrieve the JayRadar table for us to use
nt = NetworkTables.getTable(TABLE_NAME)

def filter_center_crosshair(result, tx, ty):
    if not result:
        return None, False

    closest_box = None
    min_distance = math.inf

    for box in result:
        cx, cy, w, h, _, _ = box
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
        _, _, w, h, _, _ = box
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
        cx, cy, w, h, _, _ = box

        # Find the closest point on the outside of the box
        closest_x = max(cx - w / 2, min(tx, cx + w / 2))
        closest_y = max(cy - h / 2, min(ty, cy + h / 2))

        distance = math.sqrt((closest_x - tx)**2 + (closest_y - ty)**2)

        if distance < min_distance:
            min_distance = distance
            closest_box = box

    return closest_box, True


def average_last_iterations(times, iterations):
    return sum(times[-iterations:]) / iterations

def send_filtered_results():
    
    iterations = 0
    times = []
    max_iterations = MAX_TIMES

    while True:
        results_event.wait()
        results_event.clear()
        if result_queue and times_queue:
            results = result_queue[-1]
            
            result, success = filter_edge_crosshair(results, 320, 240)

            if success:
                nt.putBoolean('te', True)
                nt.putNumber('tx', result[0])
                nt.putNumber('ty', result[1])
                nt.putNumber('tw', result[2])
                nt.putNumber('th', result[3])
                nt.putNumber('id', result[4])
                nt.putNumber('tc', result[5])
                nt.putNumber('ta', result[2]*result[3])
                filtered_queue.append(result)
                
            else:
                nt.putBoolean('te', False)
            
            iteration_time = times_queue[-1]
            
            times.append(iteration_time)

            if iterations < max_iterations:
                iterations +=1

            if len(times) > max_iterations:
                times = times[-max_iterations:]

            avg_last_x_iterations = average_last_iterations(times, iterations)

            nt.putNumber('delay', iteration_time)
            nt.putNumber('avgdelay', avg_last_x_iterations)

            print(f"Time: {iteration_time:.4f}s | "
                f"Avg Last {iterations} Iterations: {avg_last_x_iterations:.4f}s | "
                f"{(1/avg_last_x_iterations):.4f} FPS")