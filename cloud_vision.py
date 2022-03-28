from io import BytesIO
from google.cloud import vision
from google.cloud.vision_v1.types import TextAnnotation
from PIL.Image import Image


class CloudVision:
    """Helper class for recognizing images
    with Google Cloud Vision.

    Note that you will have to do some setup before using
    this class, as described in the docs
    [here](https://pypi.org/project/google-cloud-vision/).
    """

    def __init__(self):
        self.client = vision.ImageAnnotatorClient(
            client_options={"api_endpoint": "eu-vision.googleapis.com"}
        )

    def extract(self, image: Image) -> TextAnnotation:
        """Given an input `image`, try to extract its text
        with Google Cloud Vision OCR.

        The returned `TextAnnotation` also contains language information.
        """
        image_buffer = BytesIO()
        image.save(image_buffer, format="PNG")  # Lossless format
        image_content = image_buffer.getvalue()
        vision_image = vision.Image(content=image_content)
        response = self.client.text_detection(image=vision_image)
        annotation = response.full_text_annotation

        return annotation
