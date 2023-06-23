from typing import Callable, List, Mapping, Optional
from requests import Session, Request

class SessionHandler:

    def __init__(self) -> None:
        self.session = Session()
        self.cookies = dict()
        self.proxies = dict()
        self.hooks: List[Callable] = list()

    def reset(self, retain_cookies: bool = False):
        if retain_cookies: self.save_cookies()
        self.session.close()
        self.session = Session()

    def extract_cookie(self, name: str) -> Optional[str]:
        return self.session.cookies.get(name)

    def get_cookie(self, name: str) -> Optional[str]:
        return self.cookies.get(name)

    def update_proxies(self, proxies: Mapping):
        self.session.proxies.update(**proxies)
        self.proxies.update(**proxies)

    def update_cookies(self, cookies: Mapping):
        self.session.cookies.update(**cookies)
        self.cookies.update(**cookies)

    def save_cookies(self):
        self.cookies.update(**self.session.cookies.get_dict())

    def run_request(self, request: Request):
        preped = self.session.prepare_request(request)
        return self.session.send(preped)
