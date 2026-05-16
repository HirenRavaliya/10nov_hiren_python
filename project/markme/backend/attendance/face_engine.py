"""
AI Face Recognition Engine
Uses the `face_recognition` library (dlib-based) to:
1. Load all enrolled student face encodings from the DB
2. Compare a new face image against the stored encodings
3. Return the matched student + confidence score
"""
import pickle
import numpy as np
import face_recognition
from PIL import Image
import io
import logging

logger = logging.getLogger(__name__)


def get_all_face_encodings():
    """
    Fetches all students with face_registered=True and returns
    a list of (student, encoding_array) tuples.
    """
    from accounts.models import Student
    students = Student.objects.filter(face_registered=True).select_related('user')
    result = []
    for student in students:
        if student.face_encoding:
            try:
                encoding = pickle.loads(bytes(student.face_encoding))
                result.append((student, encoding))
            except Exception as e:
                logger.warning(f'Could not load encoding for student {student.id}: {e}')
    return result


def identify_face_from_image(image_file, tolerance: float = 0.5):
    """
    Given an image file-like object, extract face encodings and attempt
    to match against all enrolled students.

    Returns:
        dict with keys:
            'matched'    (bool)
            'student'    (Student instance or None)
            'confidence' (float 0-1, higher is better; None if no match)
            'message'    (str)
            'face_found' (bool)
    """
    try:
        img = Image.open(image_file).convert('RGB')
        img_array = np.array(img)
    except Exception as e:
        return {'matched': False, 'student': None, 'confidence': None,
                'face_found': False, 'message': f'Invalid image: {e}'}

    # Detect faces
    face_locations = face_recognition.face_locations(img_array, model='hog')
    if not face_locations:
        return {'matched': False, 'student': None, 'confidence': None,
                'face_found': False, 'message': 'No face detected in the image.'}

    # Get encoding for the first (largest) face
    encodings = face_recognition.face_encodings(img_array, known_face_locations=[face_locations[0]])
    if not encodings:
        return {'matched': False, 'student': None, 'confidence': None,
                'face_found': True, 'message': 'Could not compute face encoding.'}

    unknown_encoding = encodings[0]

    # Load known encodings
    known = get_all_face_encodings()
    if not known:
        return {'matched': False, 'student': None, 'confidence': None,
                'face_found': True, 'message': 'No enrolled faces in the database yet.'}

    known_encodings = [enc for (_, enc) in known]
    known_students = [s for (s, _) in known]

    # Compute distances
    distances = face_recognition.face_distance(known_encodings, unknown_encoding)
    best_idx = int(np.argmin(distances))
    best_distance = float(distances[best_idx])
    confidence = round(1.0 - best_distance, 4)

    if best_distance <= tolerance:
        matched_student = known_students[best_idx]
        return {
            'matched': True,
            'student': matched_student,
            'confidence': confidence,
            'face_found': True,
            'message': f'Matched: {matched_student.user.full_name} (confidence: {confidence:.1%})',
        }
    else:
        return {
            'matched': False,
            'student': None,
            'confidence': confidence,
            'face_found': True,
            'message': 'No match found within tolerance.',
        }


def identify_face_from_base64(base64_str: str, tolerance: float = 0.5):
    """
    Same as identify_face_from_image but accepts a base64-encoded image string
    (useful for webcam snapshots from the browser/mobile).
    """
    import base64
    # Strip data URI prefix if present
    if ',' in base64_str:
        base64_str = base64_str.split(',', 1)[1]
    image_bytes = base64.b64decode(base64_str)
    image_file = io.BytesIO(image_bytes)
    return identify_face_from_image(image_file, tolerance)
