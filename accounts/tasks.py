from celery import shared_task
from .models import FileUpload, ActivityLog
import os
from django.conf import settings
import docx

@shared_task
def add(x, y):
    print('Starting addition')
    return x + y

@shared_task
def process_file_word_count(file_upload_id):
    print('Entered file processing')
    try:
        print('In try block')
        file_upload = FileUpload.objects.get(id=file_upload_id)
        file_upload.status = 'processing'
        file_upload.save()

        filepath = file_upload.file.path
        word_count=0

        if filepath.endswith('.txt'):
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
                word_count = len(text.split())
        elif filepath.endswith('.docx'):
            doc = docx.Document(filepath)
            full_text = []
            for para in doc.paragraphs:
                full_text.append(para.text)
            text = '\n'.join(full_text)
            word_count = len(text.split())
        else:
            file_upload.status = 'failed'
            file_upload.save()
            return

        file_upload.word_count = word_count
        file_upload.status = 'completed'
        file_upload.save()

        # Log the activity
        ActivityLog.objects.create(
            user=file_upload.user,
            action='Processed file word count',
            metadata={'file_upload_id': file_upload_id, 'word_count': word_count},
        )

    except FileUpload.DoesNotExist:
        pass

    