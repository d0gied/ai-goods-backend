import datetime
import json
from typing import Any

from fastapi.responses import JSONResponse as BaseJSONResponse


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, set):
            return list(o)
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        return super().default(o)


class JSONResponse(BaseJSONResponse):
    def render(self, content: Any) -> bytes:
        """Render the given content as JSON. Process datetime objects and sets"""
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
            cls=JSONEncoder,
        ).encode("utf-8")
