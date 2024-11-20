import cv2
import requests
import numpy as np

# Replace with the IP of your ESP32-CAM
stream_url = 'http://192.168.78.159:81/stream'  # Update the port if necessary

# Attempt to connect to the stream
try:
    print("Connecting to video stream...")
    stream = requests.get(stream_url, stream=True)
    print("Connected to video stream.")
except Exception as e:
    print(f"Error connecting to video stream: {e}")
    exit()

# Byte buffer for assembling frame data
byte_buffer = b''

# Process the video stream
for chunk in stream.iter_content(chunk_size=1024):
    byte_buffer += chunk

    # Find the JPEG start and end markers
    start_marker = byte_buffer.find(b'\xff\xd8')  # JPEG start
    end_marker = byte_buffer.find(b'\xff\xd9')    # JPEG end

    if start_marker != -1 and end_marker != -1:
        # Extract the JPEG frame
        jpg_data = byte_buffer[start_marker:end_marker + 2]
        byte_buffer = byte_buffer[end_marker + 2:]  # Remove processed data
        try:
            # Decode the JPEG image into a frame
            frame = cv2.imdecode(np.frombuffer(jpg_data, dtype=np.uint8), cv2.IMREAD_COLOR)

            if frame is not None:
                # Display the frame
                cv2.imshow("ESP32-CAM Stream", frame)

                # Exit when 'q' key is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("Exiting...")
                    break
            else:
                print("Failed to decode frame.")
        except:
            continue

# Release resources
cv2.destroyAllWindows()
