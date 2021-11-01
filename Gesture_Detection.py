from pynput.keyboard import Key, Controller
import cv2
from Hand_Tracking import Hand_Detector
import math



def main():
    capture = cv2.VideoCapture(0)
    kb = Controller()

    cam_width = 640
    cam_height = 480
    capture.set(3, cam_width)
    capture.set(4, cam_height)

    detector = Hand_Detector()

    keyup_clicked = False
    keydown_clicked = False


    while True:

        _, frame = capture.read()
        frame = detector.find_hands(frame, draw=False)
        lm_list = detector.find_position(frame)
        if len(lm_list) != 0:

            x1, y1 = lm_list[4][1], lm_list[4][2]
            x2, y2 = lm_list[8][1], lm_list[8][2]
            #line_center_x, line_center_y = (x1 + x2)//2, (y1 + y2)//2

            # Draw a line
            cv2.line(frame, (x1,y1), (x2,y2), (255,0,255), 3)

            # Calculate the length
            length = math.hypot(x2-x1, y2-y1)

            # Key Down
            if length < 10 and not keydown_clicked:
                keydown_clicked = True
                kb.press(Key.down)

            # Key Up
            elif length > 110 and not keyup_clicked:
                keyup_clicked = True
                kb.press(Key.up)

            # No Key
            elif 20 < length < 100:
                kb.release(Key.up)
                kb.release(Key.down)
                keydown_clicked = False
                keyup_clicked = False

        cv2.imshow("Frame", frame)
        
        # Break the loop when 'q' button is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # After the loop release the object
    capture.release()

    # Destroy all the windows
    cv2.destroyAllWindows()



# Main ------------------------
if __name__ == "__main__":
    main()