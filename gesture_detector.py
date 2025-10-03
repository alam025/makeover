"""
Simple Gesture Detector - Just works, no fancy stuff
"""
import cv2
import numpy as np
import time
import math
import mediapipe as mp

class GestureDetector:
    def __init__(self):
        """Simple initialization - no calibration nonsense"""
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        
        self.finger_pos = None
        self.calibrated = True  # Always calibrated - no setup needed
        
        # Click detection
        self.hold_start_time = 0
        self.hold_threshold = 1.5
        self.last_pos = None
        self.stability_radius = 25
        
        print("Simple gesture detector ready!")

    def detect_finger_click(self, frame):
        """Simple finger detection - just works"""
        if frame is None:
            return None, False
        
        h, w = frame.shape[:2]
        
        # Process with MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        finger_pos = None
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Get finger tip position
                index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
                
                x = int(index_tip.x * w)
                y = int(index_tip.y * h)
                
                # Simple bounds check
                if 0 <= x < w and 0 <= y < h:
                    finger_pos = (x, y)
                break
        
        if finger_pos:
            self.finger_pos = finger_pos
            is_clicking = self.detect_hold_click(finger_pos)
            return finger_pos, is_clicking
        else:
            self.reset_calibration()
            
        return None, False

    def detect_hold_click(self, finger_pos):
        """Simple hold detection"""
        current_time = time.time()
        
        if self.last_pos is None:
            self.last_pos = finger_pos
            self.hold_start_time = current_time
            return False
        
        distance = math.sqrt(
            (finger_pos[0] - self.last_pos[0])**2 + 
            (finger_pos[1] - self.last_pos[1])**2
        )
        
        if distance <= self.stability_radius:
            hold_duration = current_time - self.hold_start_time
            if hold_duration >= self.hold_threshold:
                self.hold_start_time = current_time
                print(f"CLICK at {finger_pos}")
                return True
        else:
            self.last_pos = finger_pos
            self.hold_start_time = current_time
            
        return False

    def draw_finger_tracking_info(self, frame):
        """Simple cursor drawing - ALWAYS ON TOP"""
        cv2.putText(frame, "Point finger - Hold 1.5s to click", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        if self.finger_pos:
            x, y = self.finger_pos
            
            # Simple bright cursor
            cv2.circle(frame, (x, y), 15, (0, 255, 255), 3)
            cv2.circle(frame, (x, y), 5, (255, 255, 255), -1)
            
            # Hold progress
            if self.last_pos and self.hold_start_time:
                current_time = time.time()
                hold_progress = (current_time - self.hold_start_time) / self.hold_threshold
                hold_progress = min(hold_progress, 1.0)
                
                if hold_progress > 0.1:
                    radius = int(25 * hold_progress)
                    cv2.circle(frame, (x, y), radius, (0, 255, 0), 2)
                    percentage = int(hold_progress * 100)
                    cv2.putText(frame, f"{percentage}%", (x + 20, y - 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        return frame

    def setup_mouse_callback(self):
        pass

    def reset_calibration(self):
        self.last_pos = None
        self.hold_start_time = 0

    def get_gesture_confidence(self):
        return 1.0 if self.finger_pos else 0.0

    def calibrate_user_gestures(self, frame, duration=0.3):
        print("Gesture detection ready!")
        time.sleep(duration)