import socket
import threading
import cv2
import mediapipe as mp


INPUT_PORT = 6000
OUTPUT_PORT = 6001
HOST = socket.gethostname()


def get_range():
    '''Continuously gets changes to instrument's range from Pure Data'''
    global range_in_semitones
    while True:
        message, _ = input_socket.recvfrom(2)
        range_in_semitones = int(message.decode().rstrip(';'))
        

# Socket to receive instrument's range from Pure Data
input_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
input_socket.bind((HOST, INPUT_PORT))

# Set up and start thread that uses the get_range function
get_range_thread = threading.Thread(target=get_range)
get_range_thread.daemon = True
range_in_semitones = None
get_range_thread.start()

# Socket to output hand landmarks to Pure Data
output_socket = socket.socket()
output_socket.connect((HOST, OUTPUT_PORT))

# 0 is built-in webcam
capture = cv2.VideoCapture(0)

CAPTURE_WIDTH = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
CAPTURE_HEIGHT = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Setting up mediapipe tools for getting and drawing hand landmarks
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1,
                       min_detection_confidence=0.5,
                       min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

while True:
    # Get image from webcam and mirror it
    _, image = capture.read()
    image = cv2.flip(image, 1)

    # Get results of hand landmark detection using RGB-converted image
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_rgb.flags.writeable = False
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        detected_hand = results.multi_hand_landmarks[0]
        # 8 is the index for index fingertip landmark. For more, see
        # https://google.github.io/mediapipe/solutions/hands.html
        index_tip_landmark = detected_hand.landmark[8]

        # Send x and inverted y positions to Pure Data
        message = f'{index_tip_landmark.x} {1 - index_tip_landmark.y};'
        output_socket.send(message.encode('utf-8'))

        # Draw landmark positions and wireframe connections
        mp_draw.draw_landmarks(image,
                               detected_hand,
                               mp_hands.HAND_CONNECTIONS)

    if range_in_semitones:
        # Draw vertical marker on image for each semitone position,
        # excluding those at the edge of the image
        division_width = CAPTURE_WIDTH / range_in_semitones
        for i in range(1, range_in_semitones):
            # Every fourth line will be a different colour
            line_colour = (0, 255, 0) if i % 4 == 0 else (255, 0, 255)
            x = round(division_width * i)
            cv2.line(img=image,
                     pt1=(x, 0),
                     pt2=(x, CAPTURE_HEIGHT),
                     color=line_colour,
                     thickness=1)

    cv2.imshow('Webcam Synth', image)
    cv2.waitKey(1)
