
import face_recognition
import numpy as np
from PIL import Image
import io
import base64


class FaceRecognitionService:
    
    def __init__(self, tolerance=0.6, model='hog'):
        self.tolerance = tolerance
        self.model = model
    
    def encode_face(self, image_path):
        try:
            image = face_recognition.load_image_file(image_path)
        
            face_locations = face_recognition.face_locations(image, model=self.model)
            
            if not face_locations:
                return None
            face_encodings = face_recognition.face_encodings(image, face_locations)
            
            if not face_encodings:
                return None
            return face_encodings[0].tolist()
            
        except Exception as e:
            print(f"Error encoding face: {str(e)}")
            return None
    
    def encode_face_from_bytes(self, image_bytes):
        try:
            image = Image.open(io.BytesIO(image_bytes))
            image_array = np.array(image)
            face_locations = face_recognition.face_locations(image_array, model=self.model)
            
            if not face_locations:
                return None
            face_encodings = face_recognition.face_encodings(image_array, face_locations)
            
            if not face_encodings:
                return None
            return face_encodings[0].tolist()
            
        except Exception as e:
            print(f"Error encoding face from bytes: {str(e)}")
            return None
    
    def compare_faces(self, known_encoding, unknown_encoding):
    
        try:
            known = np.array(known_encoding)
            unknown = np.array(unknown_encoding)
            distance = face_recognition.face_distance([known], unknown)[0]
            
            is_match = distance <= self.tolerance
            
            confidence = round((1 - distance) * 100, 2)
            
            return is_match, confidence
            
        except Exception as e:
            print(f"Error comparing faces: {str(e)}")
            return False, 0.0
    
    def find_matching_student(self, uploaded_encoding, student_encodings):
       
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

        try:
            image = face_recognition.load_image_file(image_path)
            face_locations = face_recognition.face_locations(image, model=self.model)
            return len(face_locations)
        except Exception as e:
            print(f"Error detecting faces: {str(e)}")
            return 0
    
    def encoding_to_string(self, encoding):
        if encoding is None:
            return ""
        return ",".join(map(str, encoding))
    
    def string_to_encoding(self, encoding_str):
        if not encoding_str:
            return None
        try:
            return [float(x) for x in encoding_str.split(",")]
        except:
            return None


def get_face_service():
    from django.conf import settings
    
    tolerance = getattr(settings, 'FACE_RECOGNITION_TOLERANCE', 0.6)
    model = getattr(settings, 'FACE_RECOGNITION_MODEL', 'hog')
    
    return FaceRecognitionService(tolerance=tolerance, model=model)
