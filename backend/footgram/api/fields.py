"""Custom field module for api serializers module."""
import base64
import uuid

from rest_framework import serializers
from django.core.files.base import ContentFile


class Base64ImageField(serializers.ImageField):
    """Custom serializer field for encode base64 image."""
    def to_internal_value(self, data):
        decoded_file = base64.b64decode(data)
        file_name = str(uuid.uuid4())[:12]
        file_extension = self.get_file_extension(file_name, decoded_file)
        complete_file_name = "%s.%s" % (file_name, file_extension,)
        data = ContentFile(decoded_file, name=complete_file_name)
        return super(Base64ImageField, self).to_internal_value(data)
