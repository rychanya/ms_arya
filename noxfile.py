import nox


@nox.session(python=False)
def prety(session: nox.Session):
    session.run("black", ".")
    session.run("isort", "--recursive", ".")


@nox.session(python=False)
def run_tests(session: nox.Session):
    session.run("poetry", "shell")
    session.run("poetry", "install")
    session.run("pytest", "-v")
