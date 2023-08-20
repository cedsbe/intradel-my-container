import os
from datetime import datetime

import pytest

from intradel_my_container import Informations, IntradelMyContainer, Organic, Residual


def mocked_page_content() -> bytes:
    current_path = os.path.dirname(__file__)
    page_content_file_path = os.path.join(current_path, "page.content.html")
    with open(page_content_file_path, "rb") as my_file:
        return my_file.read()


@pytest.fixture(autouse=True)
def disable_intradel_call(monkeypatch):
    def stunted_get():
        return mocked_page_content()

    monkeypatch.setattr(
        IntradelMyContainer, "_get_page_content", lambda *args, **kwargs: stunted_get()
    )


def test_full_with_mock():
    data: IntradelMyContainer = IntradelMyContainer(
        login="not_required__mocked",
        password="not_required__mocked",
        municipality="not_required__mocked",
        start_date=datetime.today().replace(year=2014, month=1, day=1),
    )
    assert data.my_informations.__class__ == Informations
