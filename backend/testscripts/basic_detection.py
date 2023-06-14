import cv2
import public

cap = cv2.VideoCapture(0)
while cap.isOpened():
        success, frame = cap.read()

        if success:
            results = public.model.predict(frame)
            result = results[0]
            annotated_frame = result.plot()

            cv2.imshow('YOLOv8 Inference', annotated_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break