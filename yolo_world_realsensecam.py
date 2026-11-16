from ultralytics import YOLOE
import cv2
import pyrealsense2 as rs
import numpy as np
import csv
from object_selection import selection, mouse_callback

model = YOLOE("yoloe-26s-seg.pt")
print("YOLOE segmentation model loaded successfully")

names = ["black rectangular product box",
    "electronics packaging box",
    "black cardboard box",
    "rectangular box", 
    #"bottle"
    #"ring"
]

model.set_classes(names)
selection["boxes"] = []
selection["selected_index"] = None
window_name = "YOLO-World RealSense D455 Detection"
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
profile = pipeline.start(config)
align = rs.align(rs.stream.color)

print("Intel RealSense D455 started successfully")

color_profile = profile.get_stream(rs.stream.color)
color_intrinsics = color_profile.as_video_stream_profile().get_intrinsics()

fx = color_intrinsics.fx
fy = color_intrinsics.fy

print("Focal length X:", fx)
print("Focal length Y:", fy)
csv_file = open("experiment_data.csv", "w", newline="")

csv_writer = csv.writer(csv_file)
csv_writer.writerow([
    "Reading",
    "Actual Distance (m)",
    "Measured Distance (m)",
    "Estimated Width (cm)",
    "Estimated Height (cm)"
])
print("Experiment CSV file created successfully")
reading_number = 0

cv2.namedWindow(window_name)
cv2.setMouseCallback(window_name, mouse_callback, selection)

try:
    while True:
        frames = pipeline.wait_for_frames()

        aligned_frames = align.process(frames)

        color_frame = aligned_frames.get_color_frame()
        depth_frame = aligned_frames.get_depth_frame()
        if not color_frame:
            print("Could not capture frame")
            continue
        frame = np.asanyarray(color_frame.get_data())
        depth_image = np.asanyarray(depth_frame.get_data())
        depth_colormap = cv2.applyColorMap(
            cv2.convertScaleAbs(depth_image, alpha=0.03),
            cv2.COLORMAP_JET)
        results = model.predict(
                        frame,
                        conf=0.15,
                        imgsz=640,
                        retina_masks=True,
                        verbose=False
                    )
        
        annotated_frame = frame.copy()

        selection["boxes"] = []
        selection["measurements"] = []

        detection_count = len(results[0].boxes)

        cv2.putText(
            annotated_frame,
            f"Detections: {detection_count}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2
        )
        if results[0].masks is not None:

            for i, box in enumerate(results[0].boxes):

                # Get segmentation mask
                mask = results[0].masks.data[i].cpu().numpy()

                # Find object pixels
                ys, xs = np.where(mask > 0)

                if len(xs) == 0 or len(ys) == 0:
                    continue

                # Get tight bounding box
                x1 = int(xs.min())
                x2 = int(xs.max())
                y1 = int(ys.min())
                y2 = int(ys.max())

                object_index = len(selection["boxes"])
                selection["boxes"].append((x1, y1, x2, y2))

                # Draw bounding box
                if selection["selected_index"] == object_index:
                    color = (0, 0, 255)  # Red for selected object
                    thickness = 3
                else:
                    color = (0, 255, 0)  # Green for other objects
                    thickness = 1

                cv2.rectangle(
                    annotated_frame,
                    (x1, y1),
                    (x2, y2),
                    color,
                    thickness
                )

                # Calculate pixel dimensions
                box_width = x2 - x1
                box_height = y2 - y1

                # Find centre
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2

                # Get depth
                distance = depth_frame.get_distance(cx, cy)

                if distance > 0:

                    real_width = (box_width * distance) / fx
                    real_height = (box_height * distance) / fy

                    width_cm = real_width * 100
                    height_cm = real_height * 100

                    label = f"W: {width_cm:.1f} cm H: {height_cm:.1f} cm"

                    object_measurement = {
                        "distance": distance,
                        "width": width_cm,
                        "height": height_cm
                    }

                else:
                    label = "Depth unavailable"

                    object_measurement = None

                selection["measurements"].append(object_measurement)

                # Display measurements
                cv2.putText(
                    annotated_frame,
                    label,
                    (x1, max(y1 - 10, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

        cv2.imshow(window_name, annotated_frame)
        #cv2.imshow("RealSense Depth Map", depth_colormap)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):

            selected = selection["selected_index"]

            if selected is None:
                print("Please click on an object first!")

            elif selected >= len(selection["measurements"]):
                print("Selected object is unavailable. Please select again.")

            elif selection["measurements"][selected] is None:
                print("Depth unavailable for the selected object!")

            else:
                actual_distance = float(
                    input("Enter actual distance in metres: ")
                )

                measurement = selection["measurements"][selected]

                reading_number += 1

                csv_writer.writerow([
                    reading_number,
                    actual_distance,
                    measurement["distance"],
                    measurement["width"],
                    measurement["height"]
                ])

                csv_file.flush()

                print(f"Selected object reading {reading_number} saved!")

        if key == ord('q'):
            break

finally:
    pipeline.stop()
    csv_file.close()
    cv2.destroyAllWindows()
