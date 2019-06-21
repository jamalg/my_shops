from typing import Callable, List, Dict
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

from back.config import config


class PhotoApiMixin:
    @staticmethod
    def filename_from_headers(headers: requests.structures.CaseInsensitiveDict) -> str:
        content_disposition = headers.get("content-disposition", None)
        if content_disposition:
            # Need to bulletproof the regexp before "real" go live
            # Don't know exactly why the r is necessary to turn down flake8 error
            match = re.search(r'filename="([\w._\-/]+)"', content_disposition)
            if match:
                return match.group(1)
        image_type = headers["content-type"].split("/")[-1]
        return "image.{}".format(image_type)

    @staticmethod
    def headers_to_photo_metadata(headers: requests.structures.CaseInsensitiveDict) -> Dict:
        mimetype = headers["content-type"]
        filename = PhotoApiMixin.filename_from_headers(headers)
        return dict(
            mimetype=mimetype,
            filename=filename
        )


class ExcecutorMixin:
    @staticmethod
    def sequential(callback: Callable, kwargs_list: List[Dict]):
        results = []
        for kwargs in kwargs_list:
            try:
                results.append(callback(**kwargs))
            except Exception:
                continue
        return results

    @staticmethod
    def threaded(callback: Callable, kwargs_list: List[Dict]):
        results = []
        with ThreadPoolExecutor(max_workers=config.MAX_THREAD_POOL_SIZE) as executor:
            futures = [executor.submit(callback, **kwargs) for kwargs in kwargs_list]
            for completed in as_completed(futures):
                try:
                    results.append(completed.result())
                except Exception:
                    continue
        return results
