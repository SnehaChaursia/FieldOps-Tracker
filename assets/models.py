from django.db import models
from django.contrib.auth import get_user_model
from io import BytesIO
from django.core.files.base import ContentFile
import qrcode

User = get_user_model()


class Asset(models.Model):
    STATUS_CHOICES = [
        ("available", "Available"),
        ("unavailable", "Unavailable"),
        ("checked_out", "Checked Out"),
    ]

    name = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=255, unique=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    image = models.ImageField(upload_to="assets/", blank=True, null=True)
    qr_code = models.ImageField(upload_to="qr_codes/", blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="available"
    )

    def generate_qr(self):
        # Include basic asset info in the QR payload
        image_part = self.image.url if self.image else ""
        qr_data = (
            f"ASSET_ID:{self.id}|"
            f"NAME:{self.name}|"
            f"SERIAL:{self.serial_number}|"
            f"IMAGE:{image_part}"
        )
        qr_img = qrcode.make(qr_data)
        buffer = BytesIO()
        qr_img.save(buffer, format="PNG")
        filename = f"asset_{self.id}_qr.png"
        return filename, buffer.getvalue()

    def save(self, *args, **kwargs):
        # First save so we have an ID, then (re)generate QR for current data
        super().save(*args, **kwargs)  # save to get PK

        filename, content = self.generate_qr()
        self.qr_code.save(filename, ContentFile(content), save=False)
        # update only qr_code field to avoid recursion
        super().save(update_fields=["qr_code"])

    def __str__(self):
        return self.name

class Reservation(models.Model):
    # simple text field for the person using the asset
    user_name = models.CharField(max_length=255)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    days = models.PositiveIntegerField()
    status = models.CharField(max_length=20, default="booked")

    def __str__(self):
        return f"{self.user_name} -> {self.asset.name} ({self.status})"

