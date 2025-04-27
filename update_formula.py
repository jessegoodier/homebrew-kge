#!/usr/bin/env python3
"""
Update the Homebrew formula for kge-kubectl-get-events to the latest version.
"""

import sys
import requests
import re
import subprocess
import tomli
from pathlib import Path
import json

package_name = "kge-kubectl-get-events"
formula_name = "kge"

def get_package_metadata(package_name):
    """Get package metadata including download URL and SHA256."""
    try:
        response = requests.get(f"https://pypi.org/pypi/{package_name}/json")
        response.raise_for_status()
        package_info = response.json()

        latest_version = package_info["info"]["version"]

        # Find the sdist URL and SHA256
        sdist_url = None
        sha256 = None
        for url_info in package_info["urls"]:
            if url_info["packagetype"] == "sdist":
                sdist_url = url_info["url"]
                sha256 = url_info["digests"]["sha256"]
                break

        if not sdist_url or not sha256:
            print(f"Error: Could not find sdist URL or SHA256 for {package_name}")
            sys.exit(1)

        return latest_version, sdist_url, sha256
    except requests.RequestException as e:
        print(f"Error fetching package info from PyPI: {e}")
        sys.exit(1)

def get_explicit_dependencies():
    """Get explicit dependencies from pyproject.toml."""
    try:
        with open("pyproject.toml", "rb") as f:
            pyproject = tomli.load(f)
            return [dep.split(">=")[0].split("<")[0].strip() for dep in pyproject["project"]["dependencies"]]
    except Exception as e:
        print(f"Error reading pyproject.toml: {e}")
        sys.exit(1)

def get_sub_dependencies(package_name):
    """Get all sub-dependencies for a package using pipdeptree."""
    try:
        # Get the complete dependency tree in JSON format
        result = subprocess.run(
            ["pipdeptree", "-p", package_name, "--json"],
            capture_output=True,
            text=True,
            check=True
        )

        # Parse the JSON output
        dependencies = json.loads(result.stdout)

        # Extract all unique package names
        sub_dependencies = set()
        for dep in dependencies:
            package = dep["package"]["package_name"]
            if package != package_name:
                sub_dependencies.add(package)
            # Add dependencies of dependencies
            for sub_dep in dep.get("dependencies", []):
                sub_dependencies.add(sub_dep["package_name"])

        return sorted(sub_dependencies)

    except subprocess.CalledProcessError as e:
        print(f"Error getting sub-dependencies for {package_name}: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error parsing pipdeptree JSON output: {e}")
        return []

def get_resource_block(package_name):
    """Generate a resource block for a package."""
    try:
        response = requests.get(f"https://pypi.org/pypi/{package_name}/json")
        response.raise_for_status()
        package_info = response.json()

        # Find the sdist URL and SHA256
        sdist_url = None
        sha256 = None
        for url_info in package_info["urls"]:
            if url_info["packagetype"] == "sdist":
                sdist_url = url_info["url"]
                sha256 = url_info["digests"]["sha256"]
                break

        if not sdist_url or not sha256:
            return None

        return f'''  resource "{package_name}" do
    url "{sdist_url}"
    sha256 "{sha256}"
  end

'''
    except requests.RequestException:
        return None

def update_formula():
    """Update the formula to the latest version."""

    formula_file = Path("./Formula") / f"{formula_name}.rb"

    if not formula_file.exists():
        print(f"Error: Formula file {formula_file} not found")
        sys.exit(1)

    # Get main package metadata
    latest_version, sdist_url, sha256 = get_package_metadata(package_name)

    # Read the current formula
    formula_content = formula_file.read_text()

    # Update the URL and SHA256
    formula_content = re.sub(
        r'url "([^"]+)"',
        f'url "{sdist_url}"',
        formula_content
    )
    formula_content = re.sub(
        r'sha256 "([^"]+)"',
        f'sha256 "{sha256}"',
        formula_content
    )

    # Remove existing resource blocks and extra newlines
    formula_content = re.sub(
        r'  resource "[^"]+" do\n    url "[^"]+"\n    sha256 "[^"]+"\n  end\n',
        '',
        formula_content
    )
    formula_content = re.sub(
        r'\n{3,}',
        '\n\n',
        formula_content
    )

    # Get explicit dependencies from pyproject.toml
    explicit_deps = get_explicit_dependencies()
    print("\nExplicit dependencies from pyproject.toml:")
    for dep in explicit_deps:
        print(f"  - {dep}")

    # Get all dependencies (explicit + sub-dependencies)
    all_dependencies = set(explicit_deps)
    for dep in explicit_deps:
        sub_deps = get_sub_dependencies(dep)
        all_dependencies.update(sub_deps)

    # Add resource blocks for all dependencies
    resource_blocks = []
    for dep in sorted(all_dependencies):
        resource_block = get_resource_block(dep)
        if resource_block:
            resource_blocks.append(resource_block)

    # Insert resource blocks before the install method
    formula_content = re.sub(
        r'  def install',
        f"{''.join(resource_blocks)}  def install",
        formula_content
    )

    # Write the updated formula
    formula_file.write_text(formula_content)

    print(f"\nUpdated {package_name} formula to version {latest_version}")
    print(f"URL: {sdist_url}")
    print(f"SHA256: {sha256}")
    print("\nAdded resources for all dependencies:")
    for dep in sorted(all_dependencies):
        print(f"  - {dep}")

if __name__ == "__main__":
    update_formula()
