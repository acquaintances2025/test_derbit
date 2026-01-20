import httpx

from config.settings import Config

timeout = httpx.Timeout(60.0)


class DeribitClient(httpx.AsyncClient):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            base_url=Config.DERIBIT_API,
            verify=True,
            timeout=timeout,
            **kwargs,
        )