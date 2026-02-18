from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Student
from .face_recognition_utils import get_face_service


@receiver(post_save, sender=Student)
def generate_face_encoding(sender, instance, created, **kwargs):
    """
    Automatically generate face encoding when a student photo is uploaded
    """
    # Only process if photo exists and no encoding yet
    if instance.photo and not instance.face_encoding:
        try:
            face_service = get_face_service()
            encoding = face_service.encode_face(instance.photo.path)
            
            if encoding:
                # Update the instance with encoding
                Student.objects.filter(pk=instance.pk).update(
                    face_encoding=face_service.encoding_to_string(encoding)
                )
                print(f"Face encoding generated for {instance.name}")
            else:
                print(f"No face detected for {instance.name}")
        except Exception as e:
            print(f"Error generating face encoding: {str(e)}")
