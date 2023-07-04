import cv2
import numpy as np
import datetime
from mss import mss
from screeninfo import get_monitors

# Choose the number of monitors to capture
num_monitors = int(input("Enter the number of monitors to capture: "))

# Get information about all available monitors
monitors = get_monitors()
if len(monitors) < num_monitors:
    num_monitors = len(monitors)

# Generate the current date and time string
current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Output file codec and frame rate
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = 20.0  # Adjust the frame rate as needed

# Create separate video writers for each monitor
output_writers = []
for monitor_index in range(num_monitors):
    monitor = monitors[monitor_index]
    screen_size = (monitor.width, monitor.height)
    output_file = f'screen_record_{current_datetime}_{monitor_index}.mp4'
    output = cv2.VideoWriter(output_file, fourcc, fps, screen_size)
    output_writers.append(output)

# Record screen until 'q' key is pressed
with mss() as sct:
    while True:
        try:
            for monitor_index in range(num_monitors):
                monitor = monitors[monitor_index]

                # Capture screen image for the current monitor
                monitor_dict = {
                    "left": monitor.x,
                    "top": monitor.y,
                    "width": monitor.width,
                    "height": monitor.height,
                }
                img = np.array(sct.grab(monitor_dict))

                # Convert the image to a numpy array representation
                frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)  # Convert color space from BGRA to BGR

                # Write the frame to the output file for the current monitor
                output_writers[monitor_index].write(frame)

                # Display the resulting frame
                cv2.imshow('Screen Recording', frame)

            # Stop recording when 'q' is pressed
            if cv2.waitKey(1) == ord('q'):
                break
        except Exception as e:
            print(f"An error occurred: {e}")
            break

# Release the video writers and close the window
for output in output_writers:
    output.release()
cv2.destroyAllWindows()
