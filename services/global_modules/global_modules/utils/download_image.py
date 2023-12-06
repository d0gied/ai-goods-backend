from ..types import URL
from requests import get
from io import BytesIO

def download_image(url: URL) -> BytesIO:
    """Download image from URL.""" 
    
    image = get(url).content
    image = BytesIO(image)
    
    return image
