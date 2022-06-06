import cv2
import mediapipe as mp
import math


if __name__ == '__main__':
	cap = cv2.VideoCapture(0)
	mpHands = mp.solutions.hands
	hands = mpHands.Hands()
	mpDraw = mp.solutions.drawing_utils

	position_thumb = [0, 0]
	position_forefinger = [100, 100]

	while True:
		success, image = cap.read()
		imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		results = hands.process(imageRGB)
		# checking whether a hand is detected
		if results.multi_hand_landmarks:
			# working with each hand
			for handLms in results.multi_hand_landmarks:
				for id, lm in enumerate(handLms.landmark):
					h, w, c = image.shape
					cx, cy = int(lm.x * w), int(lm.y * h)
					
					#	chek if the current finger is a thumb
					if id == 4:
						print("thumb at", cx, cy)
						position_thumb = [cx, cy]
						#	encircle the finger
						cv2.circle(image, (cx, cy), 25, (255, 0, 255), cv2.FILLED)
					#	chek if the current finger is a forefinger
					elif id == 8:
						print("forefinger at", cx, cy)
						position_forefinger = [cx, cy]
						cv2.circle(image, (cx, cy), 25, (255, 0, 255), cv2.FILLED)

				#	draw hand
				mpDraw.draw_landmarks(image, handLms, mpHands.HAND_CONNECTIONS)

				#	check if the two fingers are near each other
				if math.dist(position_thumb, position_forefinger)<=50:
					print("You've shown OK sign!")
		cv2.imshow("Output", image)

		#	stop if "q" key is pressed
		k = cv2.waitKey(1)
		if k == ord('q'):
			break