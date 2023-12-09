from io import BytesIO

from requests import get

from ..types import URL


def download_image(url: URL) -> BytesIO:
    """Download image from URL."""

    image = get(url).content
    image = BytesIO(image)

    return image
