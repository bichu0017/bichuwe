from django.core.exceptions import ValidationError


def validate_image_size(upload):
    if upload.size > 5 * 1024 * 1024:
        raise ValidationError("Images must be 5 MB or smaller.")


def validate_resume_file(upload):
    if upload.size > 10 * 1024 * 1024:
        raise ValidationError("Resume files must be 10 MB or smaller.")

    if upload.name.lower().endswith(".pdf"):
        header = upload.read(5)
        upload.seek(0)
        if header != b"%PDF-":
            raise ValidationError("Upload a valid PDF document.")


def validate_certificate_file(upload):
    if upload.size > 10 * 1024 * 1024:
        raise ValidationError("Certificate files must be 10 MB or smaller.")

    if upload.name.lower().endswith(".pdf"):
        header = upload.read(5)
        upload.seek(0)
        if header != b"%PDF-":
            raise ValidationError("Upload a valid PDF certificate.")


def validate_document_file(upload):
    if upload.size > 20 * 1024 * 1024:
        raise ValidationError("Documents must be 20 MB or smaller.")

    extension = upload.name.rsplit(".", 1)[-1].lower() if "." in upload.name else ""
    allowed_extensions = {
        "pdf", "doc", "docx", "odt", "rtf", "txt",
        "xls", "xlsx", "csv", "ppt", "pptx", "zip",
    }
    if extension not in allowed_extensions:
        raise ValidationError("Upload a PDF, Office document, text file, or ZIP archive.")

    if extension == "pdf":
        header = upload.read(5)
        upload.seek(0)
        if header != b"%PDF-":
            raise ValidationError("Upload a valid PDF document.")
