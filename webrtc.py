Certainly! Let's modify your code to use **Streamlit-WebRTC** for webcam object detection. I'll provide the updated code below:

```python
import cv2
import pandas as pd
import streamlit as st
from ultralytics import YOLO
import numpy as np
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration

# Load the pre-trained YOLO model
model = YOLO("best.pt")

# Read the COCO class list from a file
with open("roadsylabels.txt", "r") as my_file:
    class_list = my_file.read().split("\n")

# Streamlit interface
st.title('ROADSY: Automated Traffic Sign Detection and Classification')
st.write('Choose detection method:')

# Choose detection method
option = st.selectbox('Select detection method', ('Image Upload', 'Webcam', 'Video Upload'))

if option == 'Image Upload':
    # Upload image through Streamlit
    uploaded_file = st.file_uploader("Choose an image...", type="jpg")

    if uploaded_file is not None:
        # Read the image
        frame = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)
        # Perform object detection on the frame
        results = model.predict(frame)
        detections = results[0].boxes.data
        px = pd.DataFrame(detections).astype("float")

        # Display the detected objects and their class labels
        for index, row in px.iterrows():
            x1, y1, x2, y2, _, d = map(int, row)
            c = class_list[d]

            # Draw bounding boxes and class labels on the frame
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(frame, str(c), (x1, y1),
                        cv2.FONT_HERSHEY_COMPLEX, 0.75, (255, 0, 0), 1)

        # Display the frame with objects detected
        st.image(frame, channels="BGR", caption="Detected Objects", use_column_width=True)

elif option == 'Webcam':
    # Define the video processor class
    class VideoProcessor:
        def recv(self, frame):
            img = frame.to_ndarray(format="bgr24")
            # Perform object detection on the frame
            results = model.predict(img)
            detections = results[0].boxes.data
            px = pd.DataFrame(detections).astype("float")

            # Display the detected objects and their class labels
            for index, row in px.iterrows():
                x1, y1, x2, y2, _, d = map(int, row)
                c = class_list[d]
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(img, str(c), (x1, y1),
                            cv2.FONT_HERSHEY_COMPLEX, 0.75, (255, 0, 0), 1)

            return av.VideoFrame.from_ndarray(img, format="bgr24")

    # Set up WebRTC streamer
    RTC_CONFIGURATION = RTCConfiguration(
        {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
    )
    webrtc_ctx = webrtc_streamer(
        key="WYH",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=RTC_CONFIGURATION,
        media_stream_constraints={"video": True, "audio": False},
        video_processor_factory=VideoProcessor(),
        async_processing=True,
    )

# Add any additional code or UI elements as needed
```

This modified code integrates Streamlit-WebRTC for webcam object detection. When you select the "Webcam" option, it will start capturing frames from your webcam and display the detected objects with bounding boxes and class labels. Remember to adjust any other parts of your application as necessary. 📹🚦

Source: Conversation with Bing, 25/3/2024
(1) Live Webcam with Streamlit - Medium. https://z-uo.medium.com/live-webcam-with-streamlit-f32bf68945a4.
(2) Real-time Object Detection and Tracking with YOLOv8 and Streamlit - GitHub. https://github.com/CodingMantras/yolov8-streamlit-detection-tracking.
(3) New Component: streamlit-webrtc, a new way to deal with real-time media .... https://discuss.streamlit.io/t/new-component-streamlit-webrtc-a-new-way-to-deal-with-real-time-media-streams/8669/31.
(4) Streamlit Object Detection with WEBRTC and YOLOv5 - GitHub. https://github.com/VioletVivirand/streamlit-webrtc-yolov5.
