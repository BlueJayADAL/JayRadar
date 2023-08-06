import statistics
import cv2
from ultralytics import YOLO
from time import perf_counter

cap = cv2.VideoCapture(0)

model = YOLO('yolov8n.pt')

times = []

warmup_iterations = 10

counted_iterations = 1000

while True:

    start = perf_counter()

    ret, frame = cap.read()

    if ret:
        results = model(frame)

        annotated_frame = results[0].plot()

        cv2.imshow("Yolov8", annotated_frame)

        end = perf_counter()

        it_time = end-start

        if warmup_iterations > 0:
            warmup_iterations -= 1
        elif counted_iterations > 0:
            times.append(it_time)
            counted_iterations -= 1
        else:
            break

        key = cv2.waitKey(1)

        if key == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

mean = round(statistics.mean(times)*1000, 5)

std = round(statistics.stdev(times)*1000, 5)

print(f"Mean: {mean} | STD: {std} | Count: {len(times)}")
