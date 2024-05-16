import nox

nox.options.sessions = "lint", "tests"
locations = "src", "tests", "noxfile.py"


@nox.session(python=["3.9"])
def lint(session):
    args = session.posargs or locations
    session.install("flake8", "flake8-import-order")
    session.run("flake8", *args)


@nox.session(python=["3.9"])
def tests(session):
    args = session.posargs or ["--cov"]
    session.run("poetry", "install", external=True)
    session.run("pytest", *args)
