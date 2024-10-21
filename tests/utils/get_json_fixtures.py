import os

import commentjson  # type: ignore

TEST_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIXTURE_DIR = os.path.join(TEST_BASE_DIR, "fixture")


def get_json_fixture(path: str) -> dict:
    path = os.path.join(FIXTURE_DIR, path)
    with open(path, "r", encoding="utf8") as file:
        return commentjson.loads(file.read())


def get_json_fixtures(*paths) -> list[dict]:
    return [get_json_fixture(path) for path in paths]
