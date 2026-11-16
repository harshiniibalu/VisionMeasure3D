
import cv2

# Stores the detected bounding boxes and selected object
selection = {
    "boxes": [],
    "selected_index": None,
    "measurements": []
}


def mouse_callback(event, x, y, flags, param):

    # Check whether the left mouse button was clicked
    if event == cv2.EVENT_LBUTTONDOWN:

        param["selected_index"] = None

        # Check which bounding box contains the click
        for i, (x1, y1, x2, y2) in enumerate(param["boxes"]):

            if x1 <= x <= x2 and y1 <= y <= y2:
                param["selected_index"] = i
                print(f"Object {i + 1} selected")
                break
