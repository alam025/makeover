"""
Background Engine - True Body Segmentation using MediaPipe
Detects precise body outline like PNG background removal
"""

import cv2
import numpy as np
import os
import mediapipe as mp

class BackgroundEngine:
    def __init__(self):
        """Initialize background replacement with MediaPipe body segmentation"""
        self.current_background = None
        
        # Initialize MediaPipe Selfie Segmentation
        self.mp_selfie_segmentation = mp.solutions.selfie_segmentation
        self.selfie_segmentation = self.mp_selfie_segmentation.SelfieSegmentation(
            model_selection=1  # 1 for general model (better for full body)
        )
        
        print("MediaPipe Body Segmentation background engine initialized!")

    def change_background(self, background_path):
        """Change background instantly"""
        try:
            if os.path.exists(background_path):
                self.current_background = cv2.imread(background_path)
                print(f"Background loaded: {background_path}")
                return True
            else:
                print(f"Background not found: {background_path}")
                return False
        except Exception as e:
            print(f"Background load error: {e}")
            return False

    def apply_background(self, frame, background_path=None):
        """Apply background with precise body segmentation"""
        if background_path and background_path != getattr(self, 'last_bg_path', None):
            self.change_background(background_path)
            self.last_bg_path = background_path
        
        if self.current_background is None:
            return frame
        
        try:
            # Use MediaPipe for precise body segmentation
            person_mask = self.get_mediapipe_body_mask(frame)
            
            if person_mask is None:
                return frame
            
            # Resize background
            h, w = frame.shape[:2]
            background = cv2.resize(self.current_background, (w, h))
            
            # Apply precise background replacement
            result = self.apply_precise_background_replacement(frame, background, person_mask)
            
            return result
            
        except Exception as e:
            print(f"Background application error: {e}")
            return frame

    def get_mediapipe_body_mask(self, frame):
        """Get precise body mask using MediaPipe Selfie Segmentation"""
        # Convert BGR to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process frame with MediaPipe
        results = self.selfie_segmentation.process(rgb_frame)
        
        if results.segmentation_mask is not None:
            # Convert segmentation mask to binary mask
            # MediaPipe gives float values 0-1, convert to 0-255
            segmentation_mask = results.segmentation_mask
            
            # Convert to binary mask (0 or 255)
            binary_mask = (segmentation_mask > 0.5).astype(np.uint8) * 255
            
            # Apply some smoothing to soften edges
            binary_mask = cv2.medianBlur(binary_mask, 5)
            binary_mask = cv2.GaussianBlur(binary_mask, (3, 3), 0)
            
            return binary_mask
        
        return None

    def apply_precise_background_replacement(self, frame, background, person_mask):
        """Apply precise background replacement using MediaPipe mask"""
        # Normalize mask to 0-1 range
        mask_normalized = person_mask.astype(np.float32) / 255.0
        
        # Create 3-channel mask
        mask_3d = np.stack([mask_normalized] * 3, axis=2)
        
        # Apply background replacement with precise body outline
        # Person areas = original frame
        # Background areas = new background
        person_part = frame.astype(np.float32) * mask_3d
        background_part = background.astype(np.float32) * (1.0 - mask_3d)
        
        result = person_part + background_part
        result = np.clip(result, 0, 255).astype(np.uint8)
        
        return result

    def reset_background_learning(self):
        """Reset (not needed for MediaPipe approach)"""
        print("MediaPipe background engine ready - no learning needed")
    
    def get_learning_progress(self):
        """Always ready with MediaPipe"""
        return 100