import pytest


@pytest.fixture(scope="session")
def base(request):
    top_level_dirs = [
        "source",
        "dest",
    ]

    for dir in top_level_dirs:
        create_directory(dir)

    def finalizer():
        for dir in top_level_dirs:
            remote_tree(dir)

    request.addfinalizer(finalizer)
