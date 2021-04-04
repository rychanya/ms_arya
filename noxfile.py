import nox


@nox.session(python=False)
def black(session):
    session.run("black", ".")
