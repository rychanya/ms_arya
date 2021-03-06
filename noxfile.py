import shutil

import nox

nox.options.sessions = ["prety", "tests"]


@nox.session(python=False)
def prety(session: nox.Session):
    session.run("poetry", "shell")
    session.run("black", ".")
    session.run("isort", "--recursive", ".")
    session.run("flake8", ".")


@nox.session(python=False)
def tests(session: nox.Session):
    session.run("poetry", "shell")
    session.run("poetry", "install")
    session.run("pytest", "-v")


@nox.session(python=False)
def coverage(session: nox.Session):
    session.run("poetry", "shell")
    session.run("poetry", "install")
    session.run("coverage", "run", "--source=ms_arya", "-m", "pytest")
    session.run("coverage", "report")
    session.run("coverage", "html")


@nox.session(python=False)
def docs(session: nox.Session):
    session.run("poetry", "shell")
    session.chdir("docs")
    shutil.rmtree("_build", ignore_errors=True)
    session.run("sphinx-build", "-b", "html", "-W", ".", "_build/html")


@nox.session(python=False)
def req(session: nox.Session):
    session.run(
        "poetry", "export", "-f", "requirements.txt", "--output", "requirements.txt", "--without-hashes"
    )
