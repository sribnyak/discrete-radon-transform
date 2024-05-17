import tempfile

import nox


nox.options.sessions = "lint", "tests", "safety"
locations = "src", "tests", "./noxfile.py"


def install_with_constraints(session, *args, **kwargs):
    with tempfile.NamedTemporaryFile() as constraints:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=constraints.txt",
            "--without-hashes",
            f"--output={constraints.name}",
            external=True,
        )
        session.install(f"--constraint={constraints.name}", *args, **kwargs)


@nox.session(python="3.9")
def black(session):
    args = session.posargs or locations
    install_with_constraints(session, "black")
    session.run("black", *args)


@nox.session(python="3.9")
def lint(session):
    args = session.posargs or locations
    install_with_constraints(
        session,
        "flake8",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-import-order",
    )
    session.run("flake8", *args)


@nox.session(python="3.9")
def tests(session):
    args = session.posargs or ["--cov", "-m", "not e2e"]
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(session, "coverage[toml]", "pytest", "pytest-cov")
    session.run("pytest", *args)


@nox.session(python="3.9")
def safety(session):
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        install_with_constraints(session, "safety")
        session.run("safety", "check", f"--file={requirements.name}", "--full-report")
