from django.core.exceptions import ValidationError


MAX_IMAGE_SIZE = 3 * 1024 * 1024


def validate_image_size(image):
    if image.size > MAX_IMAGE_SIZE:
        raise ValidationError("Размер изображения не должен превышать 3 МБ.")
