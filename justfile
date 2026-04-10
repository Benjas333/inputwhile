set shell := ["powershell.exe", "-c"]

alias help := default

# Print this message
default:
    @just --list

# Build the project
[group("Development")]
build:
    uv build

# Clean the dist dir
[group("Development")]
clean:
    Remove-Item -Path "./dist/" -Recurse

# Publish to TestPyPI
[group("Release")]
publish-test *args: clean build
    uv publish --publish-url https://test.pypi.org/legacy/ {{ args }}

# Publish to PyPI
[group("Release")]
publish *args: clean build
    uv publish {{ args }}
