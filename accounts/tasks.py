from celery import shared_task
from .models import FileUpload

@shared_task
def process_file_word_count(file_upload_id):
    try:
        file_upload = FileUpload.objects.get(id=file_upload_id)

        file_upload.word_count = 0
        file_upload.status = 'completed'
        file_upload.save()
    except FileUpload.DoesNotExist:
        pass