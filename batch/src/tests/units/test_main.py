from main import app


def test_app_includes_input_batch():

    assert "input" in [typer.name for typer in app.registered_groups]


def test_app_includes_output_batch():

    assert "output" in [typer.name for typer in app.registered_groups]


def test_app_includes_similarity_batch():

    assert "sim" in [typer.name for typer in app.registered_groups]
