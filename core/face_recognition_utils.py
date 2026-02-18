"""
Face Recognition Utilities
Handles face encoding, recognition, and matching for attendance system
"""
import face_recognition
import numpy as np
from PIL import Image
import io
import base64


class FaceRecognitionService:
    """Service class for face recognition operations"""
    
    def __init__(self, tolerance=0.6, model='hog'):
        """
        Initialize face recognition service
        
        Args:
            tolerance: How much distance between faces to consider it a match (lower is more strict)
            model: 'hog' (faster, CPU) or 'cnn' (more accurate, GPU)
        """
        self.tolerance = tolerance
        self.model = model
    
    def encode_face(self, image_path):
        """
        Generate face encoding from an image file
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Face encoding as a list or None if no face found
        """
        try:
            # Load image
            image = face_recognition.load_image_file(image_path)
            
            # Find face locations
            face_locations = face_recognition.face_locations(image, model=self.model)
            
            if not face_locations:
                return None
            
            # Get face encodings
            face_encodings = face_recognition.face_encodings(image, face_locations)
            
            if not face_encodings:
                return None
            
            # Return the first face encoding as a list
            return face_encodings[0].tolist()
            
        except Exception as e:
            print(f"Error encoding face: {str(e)}")
            return None
    
    def encode_face_from_bytes(self, image_bytes):
        """
        Generate face encoding from image bytes
        
        Args:
            image_bytes: Image data as bytes
            
        Returns:
            Face encoding as a list or None if no face found
        """
        try:
            # Convert bytes to image
            image = Image.open(io.BytesIO(image_bytes))
            image_array = np.array(image)
            
            # Find face locations
            face_locations = face_recognition.face_locations(image_array, model=self.model)
            
            if not face_locations:
                return None
            
            # Get face encodings
            face_encodings = face_recognition.face_encodings(image_array, face_locations)
            
            if not face_encodings:
                return None
            
            # Return the first face encoding as a list
            return face_encodings[0].tolist()
            
        except Exception as e:
            print(f"Error encoding face from bytes: {str(e)}")
            return None
    
    def compare_faces(self, known_encoding, unknown_encoding):
        """
        Compare two face encodings
        
        Args:
            known_encoding: Known face encoding (from database)
            unknown_encoding: Unknown face encoding (from uploaded image)
            
        Returns:
            Tuple of (is_match: bool, distance: float)
        """
        try:
            # Convert lists to numpy arrays
            known = np.array(known_encoding)
            unknown = np.array(unknown_encoding)
            
            # Calculate face distance
            distance = face_recognition.face_distance([known], unknown)[0]
            
            # Check if it's a match
            is_match = distance <= self.tolerance
            
            # Calculate confidence (inverse of distance)
            confidence = round((1 - distance) * 100, 2)
            
            return is_match, confidence
            
        except Exception as e:
            print(f"Error comparing faces: {str(e)}")
            return False, 0.0
    
    def find_matching_student(self, uploaded_encoding, student_encodings):
        """
        Find the best matching student from a list of known encodings
        
        Args:
            uploaded_encoding: Face encoding from uploaded image
            student_encodings: Dictionary of {student_id: encoding}
            
        Returns:
            Tuple of (student_id, confidence) or (None, 0) if no match
        """
        try:
            best_match = None
            best_confidence = 0
            
            for student_id, known_encoding in student_encodings.items():
                is_match, confidence = self.compare_faces(known_encoding, uploaded_encoding)
                
                if is_match and confidence > best_confidence:
                    best_match = student_id
                    best_confidence = confidence
            
            return best_match, best_confidence
            
        except Exception as e:
            print(f"Error finding matching student: {str(e)}")
            return None, 0
    
    def detect_faces_in_image(self, image_path):
        """
        Detect number of faces in an image
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Number of faces detected
        """
        try:
            image = face_recognition.load_image_file(image_path)
            face_locations = face_recognition.face_locations(image, model=self.model)
            return len(face_locations)
        except Exception as e:
            print(f"Error detecting faces: {str(e)}")
            return 0
    
    def encoding_to_string(self, encoding):
        """Convert numpy array encoding to string for storage"""
        if encoding is None:
            return ""
        return ",".join(map(str, encoding))
    
    def string_to_encoding(self, encoding_str):
        """Convert stored string encoding back to list"""
        if not encoding_str:
            return None
        try:
            return [float(x) for x in encoding_str.split(",")]
        except:
            return None


def get_face_service():
    """Factory function to get face recognition service instance"""
    from django.conf import settings
    
    tolerance = getattr(settings, 'FACE_RECOGNITION_TOLERANCE', 0.6)
    model = getattr(settings, 'FACE_RECOGNITION_MODEL', 'hog')
    
    return FaceRecognitionService(tolerance=tolerance, model=model)
