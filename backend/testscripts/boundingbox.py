import cv2

def draw_box_on_frame(frame, box):
    center_x, center_y, width, height, probability = box

    # Calculate the top-left and bottom-right coordinates of the box
    half_width = width // 2
    half_height = height // 2
    top_left = (int(center_x - half_width), int(center_y - half_height))
    bottom_right = (int(center_x + half_width), int(center_y + half_height))

    # Draw the box on the frame
    cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), thickness=2)

    # Display the probability as text on the top of the bounding box
    text = f"Probability: {probability:.2f}"
    cv2.putText(frame, text, (top_left[0], top_left[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), thickness=2)

    return frame
