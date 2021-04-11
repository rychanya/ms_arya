import nox


@nox.session(python=False)
def prety(session: nox.Session):
    session.run("black", ".")
    session.run("isort", "--recursive", ".")
    session.run("flake8", ".")


@nox.session(python=False)
def run_tests(session: nox.Session):
    session.run("poetry", "shell")
    session.run("poetry", "install")
    session.run("pytest", "-v")
