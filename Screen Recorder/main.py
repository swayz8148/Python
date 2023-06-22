import cv2
import pyautogui
import numpy as np

# Screen resolution
screen_size = pyautogui.size()

# Output file name and codec
output_file = 'screen_record.mp4'
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = 20.0  # Adjust the frame rate as needed
output = cv2.VideoWriter(output_file, fourcc, fps, screen_size)

# Record screen until 'q' key is pressed
while True:
    try:
        # Capture screen image
        img = pyautogui.screenshot()

        # Convert the image to a numpy array representation
        frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        # Apply slight image smoothing
        frame = cv2.bilateralFilter(frame, 5, 50, 50)

        # Write the frame to the output file
        output.write(frame)

        # Display the resulting frame
        cv2.imshow('Screen Recording', frame)

        # Stop recording when 'q' is pressed
        if cv2.waitKey(1) == ord('q'):
            break
    except Exception as e:
        print(f"An error occurred: {e}")
        break

# Release the video writer and close the window
output.release()
cv2.destroyAllWindows()
