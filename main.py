"""
AI Professional Makeover - Modern animations with reliable structure
"""

import cv2
import numpy as np
import os
import time
from camera_handler import CameraHandler
from gesture_detector import GestureDetector
from popup_manager import PopupManager
from background_engine import BackgroundEngine
from clothing_engine import ProfessionalClothingEngine as ClothingEngine
from ui_components import UIComponents

class ProfessionalMakeoverApp:
    def __init__(self):
        print("🚀 Initializing AI Professional Makeover...")
        
        try:
            self.camera = CameraHandler()
            self.gesture_detector = GestureDetector()
            self.popup_manager = PopupManager()
            self.bg_engine = BackgroundEngine()
            self.clothing_engine = ClothingEngine()
            self.ui = UIComponents()
            
            # Application state
            self.current_step = "welcome"
            self.face_detected_time = 0
            self.selected_background = None
            self.selected_clothing_type = None
            self.selected_clothing_item = None
            
            # Load assets
            self.load_assets()
            
            print("✅ Application initialized successfully!")
            
        except Exception as e:
            print(f"❌ Initialization error: {e}")
            print("Check camera connection and asset folders")
    
    def load_assets(self):
        """Load all backgrounds, outfits, and other assets"""
        # Create assets directory if not exists
        os.makedirs("assets/backgrounds", exist_ok=True)
        os.makedirs("assets/clothing/shirts", exist_ok=True)
        os.makedirs("assets/clothing/tshirts", exist_ok=True)
        os.makedirs("assets/clothing/blazers", exist_ok=True)
        os.makedirs("assets/clothing/ties", exist_ok=True)
        
        # Background options (professional settings)
        self.backgrounds = [
            "assets/backgrounds/office_modern.jpg",
            "assets/backgrounds/conference_room.jpg", 
            "assets/backgrounds/home_office.jpg",
            "assets/backgrounds/library.jpg",
            "assets/backgrounds/city_view.jpg",
            "assets/backgrounds/minimalist_white.jpg",
            "assets/backgrounds/tech_office.jpg",
            "assets/backgrounds/boardroom.jpg"
        ]
        
        # Create placeholder assets if they don't exist
        self.create_placeholder_assets()
        
        print(f"📁 Loaded {len(self.backgrounds)} background images")
    
    def create_placeholder_assets(self):
        """Create placeholder backgrounds for testing"""
        for i, bg_path in enumerate(self.backgrounds):
            if not os.path.exists(bg_path):
                # Create gradient backgrounds as placeholders
                img = self.ui.create_gradient_background(640, 480, i)
                cv2.imwrite(bg_path, img)
    
    def run(self):
        """Main application loop with modern animations"""
        print("🎥 Starting camera...")
        
        # Create fullscreen window
        cv2.namedWindow('AI Professional Makeover', cv2.WINDOW_NORMAL)
        cv2.setWindowProperty('AI Professional Makeover', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        
        while True:
            try:
                # Get camera frame
                frame = self.camera.get_frame()
                if frame is None:
                    print("❌ Error: Could not read from camera")
                    break
                
                # Resize frame for consistent processing
                frame = cv2.resize(frame, (1280, 720))
                
                # Get finger position FIRST (before any drawing)
                finger_pos, is_clicking = self.gesture_detector.detect_finger_click(frame)
                
                # Process current step with modern animations
                if self.current_step == "welcome":
                    frame = self.handle_welcome_screen_modern(frame)
                elif self.current_step == "face_detection":
                    frame = self.handle_face_detection_modern(frame)
                elif self.current_step == "background_selection":
                    frame = self.handle_background_selection_modern(frame, finger_pos, is_clicking)
                elif self.current_step == "clothing_selection":
                    frame = self.handle_clothing_selection_modern(frame, finger_pos, is_clicking)
                elif self.current_step == "complete":
                    frame = self.handle_complete_screen_modern(frame, finger_pos, is_clicking)
                
                # Draw modern finger cursor LAST (always on top)
                if finger_pos and self.gesture_detector.calibrated:
                    frame = self.ui.draw_finger_cursor(frame, finger_pos)
                
                # Display frame
                cv2.imshow('AI Professional Makeover', frame)
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q') or key == 27:  # Q or ESC to quit
                    break
                elif key == ord('s'):  # S to start from welcome
                    self.current_step = "welcome"
                elif key == ord('r'):  # R to restart
                    self.restart_application()
                elif key == ord('f'):  # F to toggle fullscreen
                    cv2.setWindowProperty('AI Professional Makeover', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
                
            except Exception as e:
                print(f"❌ Main loop error: {e}")
                break
        
        # Cleanup
        self.cleanup()
    
    def handle_welcome_screen_modern(self, frame):
        """Display enhanced welcome screen with modern animations"""
        frame = self.ui.draw_welcome_screen(frame)
        
        # Auto-proceed to face detection after 3 seconds
        if not hasattr(self, 'welcome_start_time'):
            self.welcome_start_time = time.time()
        
        elapsed = time.time() - self.welcome_start_time
        if elapsed > 3.0:
            self.current_step = "face_detection"
            print("🎯 Starting face detection...")
        
        return frame
    
    def handle_face_detection_modern(self, frame):
        """Handle face detection with modern UI animations"""
        # Use simple camera detection (returns boolean only)
        face_detected = self.camera.detect_face(frame)
        
        if face_detected:
            # Get face coordinates from camera handler
            face_coords = getattr(self.camera, 'face_coords', None)
            
            if face_coords:
                # Draw modern face outline with professional styling
                frame = self.ui.draw_face_outline(frame, face_coords)
            
            # Track detection time
            if self.face_detected_time == 0:
                self.face_detected_time = time.time()
            
            # Show modern progress with enhanced styling
            elapsed = time.time() - self.face_detected_time
            progress = min(elapsed / 2.0, 1.0)  # 2 seconds to complete
            frame = self.ui.draw_detection_progress(frame, progress)
            
            # Auto-proceed when stable
            if elapsed > 2.0:
                self.current_step = "background_selection"
                print("✅ Face detected! Moving to background selection...")
        else:
            self.face_detected_time = 0
            # Use modern face detection guide with enhanced styling
            frame = self.ui.draw_face_detection_guide(frame)
        
        return frame
    
    def handle_background_selection_modern(self, frame, finger_pos, is_clicking):
        """Handle background selection with hover progress animation"""
        # Apply current background if selected - PERSON ALWAYS STAYS VISIBLE
        if self.selected_background is not None:
            frame = self.bg_engine.apply_background(frame, self.selected_background)
        
        # Draw modern background popups FIRST
        frame = self.popup_manager.draw_background_popups(frame, self.backgrounds)
        
        # Add modern hover highlight with PROGRESS ANIMATION
        if finger_pos:
            frame = self.popup_manager.highlight_popup_on_hover(frame, finger_pos)
            
            # Show hover progress (0-100% counting animation)
            if hasattr(self.gesture_detector, 'last_pos') and self.gesture_detector.last_pos:
                if hasattr(self.gesture_detector, 'hold_start_time') and self.gesture_detector.hold_start_time:
                    current_time = time.time()
                    hold_progress = ((current_time - self.gesture_detector.hold_start_time) / 
                                   self.gesture_detector.hold_threshold)
                    hold_progress = min(hold_progress, 1.0)
                    
                    if hold_progress > 0:
                        # Draw progress animation (0-100%)
                        percentage = int(hold_progress * 100)
                        x, y = finger_pos
                        
                        # Progress ring around cursor
                        progress_radius = int(40 + 20 * hold_progress)
                        color = (0, 255, 255) if hold_progress < 0.8 else (0, 255, 0)
                        cv2.circle(frame, (x, y), progress_radius, color, 4)
                        
                        # Progress text with counting animation
                        cv2.putText(frame, f"{percentage}%", (x + 50, y - 30),
                                   cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 3)
                        
                        # "SELECTING..." text
                        if hold_progress > 0.1:
                            cv2.putText(frame, "SELECTING...", (x + 50, y + 10),
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        # Modern instruction text with enhanced styling
        frame = self.ui.draw_instruction_text(frame, "Point and hold to select background", (640, 50))
        
        # Check for click when progress reaches 100%
        if is_clicking:
            selected_idx = self.popup_manager.check_popup_click(finger_pos)
            if selected_idx is not None and selected_idx < len(self.backgrounds):
                self.selected_background = self.backgrounds[selected_idx]
                # INSTANT background change - no delay
                self.bg_engine.change_background(self.selected_background)
                print(f"Background selected: {os.path.basename(self.selected_background)}")
                # Move to next step immediately
                self.current_step = "clothing_selection"
        
        return frame
    
    def handle_clothing_selection_modern(self, frame, finger_pos, is_clicking):
        """Handle multi-step clothing selection with proper flow and counting animation"""
        # Apply background first
        if self.selected_background:
            frame = self.bg_engine.apply_background(frame, self.selected_background)
        
        # Apply current clothing if selected
        if self.selected_clothing_type and self.selected_clothing_item is not None:
            frame = self.clothing_engine.apply_clothing_item(frame, self.selected_clothing_type, self.selected_clothing_item)
        
        # STEP 1: Initial choice between T-shirt and Shirt
        if not hasattr(self, 'clothing_step') or self.clothing_step == "initial":
            self.clothing_step = "initial"
            
            # Show T-shirt (LEFT) and Shirt (RIGHT) options - FIXED ORDER
            initial_options = ["tshirts", "shirts"]  # This will put tshirts on LEFT, shirts on RIGHT
            frame = self.popup_manager.draw_initial_clothing_choice(frame, initial_options)
            
            # Add hover highlight with PROGRESS ANIMATION
            if finger_pos:
                frame = self.popup_manager.highlight_popup_on_hover(frame, finger_pos)
                
                # Show hover progress (0-100% counting animation)
                if hasattr(self.gesture_detector, 'last_pos') and self.gesture_detector.last_pos:
                    if hasattr(self.gesture_detector, 'hold_start_time') and self.gesture_detector.hold_start_time:
                        current_time = time.time()
                        hold_progress = ((current_time - self.gesture_detector.hold_start_time) / 
                                       self.gesture_detector.hold_threshold)
                        hold_progress = min(hold_progress, 1.0)
                        
                        if hold_progress > 0:
                            # Draw progress animation (0-100%)
                            percentage = int(hold_progress * 100)
                            x, y = finger_pos
                            
                            # Progress ring around cursor
                            progress_radius = int(40 + 20 * hold_progress)
                            color = (0, 255, 255) if hold_progress < 0.8 else (0, 255, 0)
                            cv2.circle(frame, (x, y), progress_radius, color, 4)
                            
                            # Progress text with counting animation
                            cv2.putText(frame, f"{percentage}%", (x + 50, y - 30),
                                       cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 3)
                            
                            # "SELECTING..." text
                            if hold_progress > 0.1:
                                cv2.putText(frame, "SELECTING...", (x + 50, y + 10),
                                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            
            # Instructions
            frame = self.ui.draw_instruction_text(frame, "Point and hold: T-shirt (LEFT) or Shirt (RIGHT)", (640, 50))
            
            # Check for click
            if is_clicking:
                selected_idx = self.popup_manager.check_popup_click(finger_pos)
                if selected_idx is not None and selected_idx < len(initial_options):
                    self.selected_clothing_category = initial_options[selected_idx]
                    
                    if self.selected_clothing_category == "tshirts":
                        self.clothing_step = "tshirt_selection"
                        print("T-shirt category selected")
                    elif self.selected_clothing_category == "shirts":
                        self.clothing_step = "shirt_selection"
                        print("Shirt category selected")
        
        # STEP 2A: T-shirt selection (final step for T-shirts)
        elif self.clothing_step == "tshirt_selection":
            # Get available T-shirts
            available_tshirts = self.clothing_engine.get_available_clothing("tshirts")
            
            if available_tshirts:
                frame = self.popup_manager.draw_clothing_item_popups(frame, available_tshirts, "tshirts")
                
                if finger_pos:
                    frame = self.popup_manager.highlight_popup_on_hover(frame, finger_pos)
                    
                    # Show hover progress (0-100% counting animation)
                    if hasattr(self.gesture_detector, 'last_pos') and self.gesture_detector.last_pos:
                        if hasattr(self.gesture_detector, 'hold_start_time') and self.gesture_detector.hold_start_time:
                            current_time = time.time()
                            hold_progress = ((current_time - self.gesture_detector.hold_start_time) / 
                                           self.gesture_detector.hold_threshold)
                            hold_progress = min(hold_progress, 1.0)
                            
                            if hold_progress > 0:
                                # Draw progress animation (0-100%)
                                percentage = int(hold_progress * 100)
                                x, y = finger_pos
                                
                                # Progress ring around cursor
                                progress_radius = int(40 + 20 * hold_progress)
                                color = (255, 0, 255) if hold_progress < 0.8 else (0, 255, 0)  # Purple for T-shirts
                                cv2.circle(frame, (x, y), progress_radius, color, 4)
                                
                                # Progress text with counting animation
                                cv2.putText(frame, f"{percentage}%", (x + 50, y - 30),
                                           cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 3)
                                
                                # "SELECTING..." text
                                if hold_progress > 0.1:
                                    cv2.putText(frame, "SELECTING T-SHIRT...", (x + 50, y + 10),
                                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                
                frame = self.ui.draw_instruction_text(frame, "Point and hold to select your T-shirt style", (640, 50))
                
                if is_clicking:
                    selected_idx = self.popup_manager.check_popup_click(finger_pos)
                    if selected_idx is not None and selected_idx < len(available_tshirts):
                        self.selected_clothing_type = "tshirts"
                        self.selected_clothing_item = selected_idx
                        self.current_step = "complete"
                        print(f"T-shirt {selected_idx + 1} selected - Going to complete")
            else:
                frame = self.ui.draw_instruction_text(frame, "No T-shirts available", (640, 50))
        
        # STEP 2B: Shirt selection
        elif self.clothing_step == "shirt_selection":
            # Get available shirts
            available_shirts = self.clothing_engine.get_available_clothing("shirts")
            
            if available_shirts:
                frame = self.popup_manager.draw_clothing_item_popups(frame, available_shirts, "shirts")
                
                if finger_pos:
                    frame = self.popup_manager.highlight_popup_on_hover(frame, finger_pos)
                    
                    # Show hover progress (0-100% counting animation)
                    if hasattr(self.gesture_detector, 'last_pos') and self.gesture_detector.last_pos:
                        if hasattr(self.gesture_detector, 'hold_start_time') and self.gesture_detector.hold_start_time:
                            current_time = time.time()
                            hold_progress = ((current_time - self.gesture_detector.hold_start_time) / 
                                           self.gesture_detector.hold_threshold)
                            hold_progress = min(hold_progress, 1.0)
                            
                            if hold_progress > 0:
                                # Draw progress animation (0-100%)
                                percentage = int(hold_progress * 100)
                                x, y = finger_pos
                                
                                # Progress ring around cursor
                                progress_radius = int(40 + 20 * hold_progress)
                                color = (255, 255, 0) if hold_progress < 0.8 else (0, 255, 0)  # Cyan for shirts
                                cv2.circle(frame, (x, y), progress_radius, color, 4)
                                
                                # Progress text with counting animation
                                cv2.putText(frame, f"{percentage}%", (x + 50, y - 30),
                                           cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 3)
                                
                                # "SELECTING..." text
                                if hold_progress > 0.1:
                                    cv2.putText(frame, "SELECTING SHIRT...", (x + 50, y + 10),
                                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                
                frame = self.ui.draw_instruction_text(frame, "Point and hold to select your shirt style", (640, 50))
                
                if is_clicking:
                    selected_idx = self.popup_manager.check_popup_click(finger_pos)
                    if selected_idx is not None and selected_idx < len(available_shirts):
                        self.selected_clothing_type = "shirts"
                        self.selected_clothing_item = selected_idx
                        self.clothing_step = "accessories_selection"
                        print(f"Shirt {selected_idx + 1} selected - Moving to accessories")
            else:
                frame = self.ui.draw_instruction_text(frame, "No shirts available", (640, 50))
        
        # STEP 3: Accessories selection (only after shirt)
        elif self.clothing_step == "accessories_selection":
            # Show Blazer, Tie, and "No Blazer/Tie" options
            accessory_options = ["blazers", "ties", "no_accessories"]
            frame = self.popup_manager.draw_accessory_popups(frame, accessory_options)
            
            if finger_pos:
                frame = self.popup_manager.highlight_popup_on_hover(frame, finger_pos)
                
                # Show hover progress (0-100% counting animation)
                if hasattr(self.gesture_detector, 'last_pos') and self.gesture_detector.last_pos:
                    if hasattr(self.gesture_detector, 'hold_start_time') and self.gesture_detector.hold_start_time:
                        current_time = time.time()
                        hold_progress = ((current_time - self.gesture_detector.hold_start_time) / 
                                       self.gesture_detector.hold_threshold)
                        hold_progress = min(hold_progress, 1.0)
                        
                        if hold_progress > 0:
                            # Draw progress animation (0-100%)
                            percentage = int(hold_progress * 100)
                            x, y = finger_pos
                            
                            # Progress ring around cursor
                            progress_radius = int(40 + 20 * hold_progress)
                            color = (0, 165, 255) if hold_progress < 0.8 else (0, 255, 0)  # Orange for accessories
                            cv2.circle(frame, (x, y), progress_radius, color, 4)
                            
                            # Progress text with counting animation
                            cv2.putText(frame, f"{percentage}%", (x + 50, y - 30),
                                       cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 3)
                            
                            # "SELECTING..." text
                            if hold_progress > 0.1:
                                cv2.putText(frame, "SELECTING ACCESSORY...", (x + 50, y + 10),
                                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            
            frame = self.ui.draw_instruction_text(frame, "Point and hold: Add Blazer, Tie, or keep shirt only?", (640, 50))
            
            if is_clicking:
                selected_idx = self.popup_manager.check_popup_click(finger_pos)
                if selected_idx is not None and selected_idx < len(accessory_options):
                    selected_accessory = accessory_options[selected_idx]
                    
                    if selected_accessory == "no_accessories":
                        # User wants only shirt - go to complete
                        self.current_step = "complete"
                        print("Shirt only selected - Going to complete")
                    elif selected_accessory == "blazers":
                        self.clothing_step = "blazer_selection"
                        print("Blazer category selected")
                    elif selected_accessory == "ties":
                        self.clothing_step = "tie_selection"
                        print("Tie category selected")
        
        # STEP 4A: Blazer selection
        elif self.clothing_step == "blazer_selection":
            available_blazers = self.clothing_engine.get_available_clothing("blazers")
            
            if available_blazers:
                frame = self.popup_manager.draw_clothing_item_popups(frame, available_blazers, "blazers")
                
                if finger_pos:
                    frame = self.popup_manager.highlight_popup_on_hover(frame, finger_pos)
                    
                    # Show hover progress (0-100% counting animation)
                    if hasattr(self.gesture_detector, 'last_pos') and self.gesture_detector.last_pos:
                        if hasattr(self.gesture_detector, 'hold_start_time') and self.gesture_detector.hold_start_time:
                            current_time = time.time()
                            hold_progress = ((current_time - self.gesture_detector.hold_start_time) / 
                                           self.gesture_detector.hold_threshold)
                            hold_progress = min(hold_progress, 1.0)
                            
                            if hold_progress > 0:
                                # Draw progress animation (0-100%)
                                percentage = int(hold_progress * 100)
                                x, y = finger_pos
                                
                                # Progress ring around cursor
                                progress_radius = int(40 + 20 * hold_progress)
                                color = (128, 0, 128) if hold_progress < 0.8 else (0, 255, 0)  # Purple for blazers
                                cv2.circle(frame, (x, y), progress_radius, color, 4)
                                
                                # Progress text with counting animation
                                cv2.putText(frame, f"{percentage}%", (x + 50, y - 30),
                                           cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 3)
                                
                                # "SELECTING..." text
                                if hold_progress > 0.1:
                                    cv2.putText(frame, "SELECTING BLAZER...", (x + 50, y + 10),
                                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                
                frame = self.ui.draw_instruction_text(frame, "Point and hold to select your blazer style", (640, 50))
                
                if is_clicking:
                    selected_idx = self.popup_manager.check_popup_click(finger_pos)
                    if selected_idx is not None and selected_idx < len(available_blazers):
                        # Apply blazer
                        self.apply_accessory("blazers", selected_idx)
                        self.current_step = "complete"
                        print(f"Blazer {selected_idx + 1} selected - Going to complete")
            else:
                frame = self.ui.draw_instruction_text(frame, "No blazers available", (640, 50))
        
        # STEP 4B: Tie selection  
        elif self.clothing_step == "tie_selection":
            available_ties = self.clothing_engine.get_available_clothing("ties")
            
            if available_ties:
                frame = self.popup_manager.draw_clothing_item_popups(frame, available_ties, "ties")
                
                if finger_pos:
                    frame = self.popup_manager.highlight_popup_on_hover(frame, finger_pos)
                    
                    # Show hover progress (0-100% counting animation)
                    if hasattr(self.gesture_detector, 'last_pos') and self.gesture_detector.last_pos:
                        if hasattr(self.gesture_detector, 'hold_start_time') and self.gesture_detector.hold_start_time:
                            current_time = time.time()
                            hold_progress = ((current_time - self.gesture_detector.hold_start_time) / 
                                           self.gesture_detector.hold_threshold)
                            hold_progress = min(hold_progress, 1.0)
                            
                            if hold_progress > 0:
                                # Draw progress animation (0-100%)
                                percentage = int(hold_progress * 100)
                                x, y = finger_pos
                                
                                # Progress ring around cursor
                                progress_radius = int(40 + 20 * hold_progress)
                                color = (255, 0, 0) if hold_progress < 0.8 else (0, 255, 0)  # Blue for ties
                                cv2.circle(frame, (x, y), progress_radius, color, 4)
                                
                                # Progress text with counting animation
                                cv2.putText(frame, f"{percentage}%", (x + 50, y - 30),
                                           cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 3)
                                
                                # "SELECTING..." text
                                if hold_progress > 0.1:
                                    cv2.putText(frame, "SELECTING TIE...", (x + 50, y + 10),
                                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                
                frame = self.ui.draw_instruction_text(frame, "Point and hold to select your tie style", (640, 50))
                
                if is_clicking:
                    selected_idx = self.popup_manager.check_popup_click(finger_pos)
                    if selected_idx is not None and selected_idx < len(available_ties):
                        # Apply tie
                        self.apply_accessory("ties", selected_idx)
                        self.current_step = "complete"
                        print(f"Tie {selected_idx + 1} selected - Going to complete")
            else:
                frame = self.ui.draw_instruction_text(frame, "No ties available", (640, 50))
        
        return frame
    
    def apply_accessory(self, accessory_type, item_index):
        """Apply accessory (blazer or tie) on top of shirt"""
        # Store accessory information
        if not hasattr(self, 'selected_accessories'):
            self.selected_accessories = {}
        
        self.selected_accessories[accessory_type] = item_index
        print(f"Applied {accessory_type}: {item_index}")
    
    def handle_complete_screen_modern(self, frame, finger_pos, is_clicking):
        """Show final result with all applied clothing"""
        # Apply background
        if self.selected_background:
            frame = self.bg_engine.apply_background(frame, self.selected_background)
        
        # Apply main clothing (shirt or t-shirt)
        if self.selected_clothing_type and self.selected_clothing_item is not None:
            frame = self.clothing_engine.apply_clothing_item(frame, self.selected_clothing_type, self.selected_clothing_item)
        
        # Apply accessories if any (blazer, tie)
        if hasattr(self, 'selected_accessories'):
            for accessory_type, item_index in self.selected_accessories.items():
                frame = self.clothing_engine.apply_clothing_item(frame, accessory_type, item_index)
        
        # Draw modern completion overlay
        frame = self.ui.draw_completion_screen(frame)
        
        # Add professional watermark
        frame = self.ui.add_professional_watermark(frame)
        
        # Save screenshot option with modern feedback
        if is_clicking and finger_pos:
            self.save_result(frame)
            # Show save notification
            frame = self.ui.draw_notification(frame, "Screenshot saved successfully!", "success")
        
        return frame
    
    def save_result(self, frame):
        """Save the final result with timestamp"""
        timestamp = int(time.time())
        filename = f"professional_makeover_{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        print(f"📸 Result saved as {filename}")
    
    def restart_application(self):
        """Restart the application with modern feedback"""
        self.current_step = "welcome"
        self.face_detected_time = 0
        self.selected_background = None
        self.selected_clothing_type = None
        self.selected_clothing_item = None
        
        # Reset clothing selection states
        if hasattr(self, 'clothing_step'):
            delattr(self, 'clothing_step')
        if hasattr(self, 'selected_clothing_category'):
            delattr(self, 'selected_clothing_category')
        if hasattr(self, 'selected_accessories'):
            delattr(self, 'selected_accessories')
        
        # Reset background learning
        if hasattr(self.bg_engine, 'reset_background_learning'):
            self.bg_engine.reset_background_learning()
        
        # Clear timing attributes
        if hasattr(self, 'welcome_start_time'):
            delattr(self, 'welcome_start_time')
        
        print("Application restarted with modern interface!")
    
    def cleanup(self):
        """Clean up resources"""
        self.camera.release()
        cv2.destroyAllWindows()
        print("Modern AI Professional Makeover closed successfully!")

if __name__ == "__main__":
    try:
        app = ProfessionalMakeoverApp()
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        print("Please check your camera connection and try again.")