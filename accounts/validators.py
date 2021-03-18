import re
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from django.db.models.fields.files import ImageFieldFile
from globals.global_config import ALLOWED_IMAGE_FORMATS

def avatar_validator(avatar):
	if avatar and isinstance(avatar, UploadedFile):
		# size = avatar.size
		file_type, file_format = avatar.content_type.split('/')

		if file_type != 'image' or file_format not in ALLOWED_IMAGE_FORMATS:
			raise ValidationError('File type not supported')
		elif avatar and isinstance(avatar, ImageFieldFile):
			pass