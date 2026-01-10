from invoke import task
import sys

@task
def start(ctx):
    ctx.run(f'"{sys.executable}" src/index.py', env={"PYGAME_HIDE_SUPPORT_PROMPT": "1"})

@task
def test(ctx):
    ctx.run("pytest src")

@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest src")

@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html")

@task
def lint(ctx):
    ctx.run("pylint src")
