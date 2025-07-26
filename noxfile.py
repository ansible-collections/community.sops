# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

# The following metadata allows Python runners and nox to install the required
# dependencies for running this Python script:
#
# /// script
# dependencies = ["nox>=2025.02.09", "antsibull-nox"]
# ///

import os
import sys
from pathlib import Path

import nox


# We try to import antsibull-nox, and if that doesn't work, provide a more useful
# error message to the user.
try:
    import antsibull_nox
except ImportError:
    print("You need to install antsibull-nox in the same Python environment as nox.")
    sys.exit(1)


antsibull_nox.load_antsibull_nox_toml()


# Integration test
session_names = []


def create_setup_callback(
    *,
    sops_version: str | None,
    github_latest_detection: str | None,
) -> None:
    def callback() -> None:
        path = Path("tests", "integration", "integration_config.yml")
        content = "---\n"
        if sops_version:
            content += f"override_sops_version: {sops_version}\n"
        if github_latest_detection:
            content += f"github_latest_detection: {github_latest_detection}\n"
        github_token = os.environ.get("GITHUB_TOKEN")
        if github_token:
            content += f"github_token: {github_token}\n"
        path.write_text(content)

    return callback


def add_target(
    *,
    core_version: str,
    docker_container: str,
    sops_version: str | None = None,
    python_version: str | None = None,
    github_latest_detection: str | None = None,
    gha_container: str = "ubuntu-latest",
    target: str = "gha/main/",
) -> None:
    docker_container_short = docker_container
    if docker_container_short.startswith("quay.io/ansible-community/test-image:"):
        docker_container_short = docker_container_short[len("quay.io/ansible-community/test-image:"):]
    target_name = target.split("/", 1)[1].rstrip("/").replace("/", "-")
    # Compose name
    name = f"ansible-test-integration-{target_name}-{core_version}-{docker_container_short}"
    if sops_version:
        name = f"{name}-{sops_version}"
    # Compose command
    command = ["integration", "--color", "-v", "--docker", docker_container]
    if python_version:
        command.extend(["--python", python_version])
    command.append(target)
    # Compose display name
    display_name = [target_name, f"Ⓐ{core_version}"]
    if sops_version:
        display_name.append(f"SOPS-{sops_version}")
    display_name.append(docker_container_short)
    if python_version:
        display_name.append(f"py{python_version}")
    if 'arm' in gha_container:
        display_name.append('ARM')
    # Compose description
    descr = [
        f"ansible-core {core_version}",
    ]
    if python_version:
        descr.append(f"{docker_container_short}/py-{python_version}")
    else:
        descr.append(f"{docker_container_short}")
    if sops_version:
        descr.append(f"SOPS {sops_version}")
    # Add task
    extra_data = {
        "display-name": "+".join(display_name),
        "gha-container": gha_container,
    }
    if target.startswith("gha/install/"):
        extra_data["has-coverage"] = "false"
    antsibull_nox.add_ansible_test_session(
        name=name,
        description=f"Run integration tests with {', '.join(descr)}",
        extra_deps_files=["tests/integration/requirements.yml"],
        ansible_test_params=command,
        default=False,
        ansible_core_version=core_version,
        register_name="integration",
        register_extra_data=extra_data,
        callback_before=create_setup_callback(
            sops_version=sops_version,
            github_latest_detection=github_latest_detection,
        ),
    )
    session_names.append(name)


archlinux = "quay.io/ansible-community/test-image:archlinux"
debian_bullseye = "quay.io/ansible-community/test-image:debian-bullseye"
debian_bookworm = "quay.io/ansible-community/test-image:debian-bookworm"

for core_version in ["devel"]:
    for docker_container in ["ubuntu2204", "ubuntu2404", "fedora42"]:
        for sops_version in ["3.5.0", "3.6.1", "3.7.3", "3.8.1", "3.9.3", "3.10.2"]:
            add_target(core_version=core_version, docker_container=docker_container, sops_version=sops_version)
add_target(core_version="2.15", docker_container="ubuntu2004", sops_version="3.10.0")
add_target(core_version="2.15", docker_container="ubuntu2204", sops_version="3.6.0")
add_target(core_version="2.15", docker_container=debian_bullseye, python_version="3.9", sops_version="latest")
add_target(core_version="2.16", docker_container="ubuntu2004", sops_version="3.7.0")
add_target(core_version="2.16", docker_container="ubuntu2204", sops_version="3.7.3")
add_target(core_version="2.17", docker_container="ubuntu2204", sops_version="3.8.0")
add_target(core_version="2.17", docker_container="fedora39", sops_version="3.10.1")
add_target(core_version="2.18", docker_container="ubuntu2404", sops_version="3.9.0")
add_target(core_version="2.18", docker_container="fedora40", sops_version="3.9.2")
add_target(core_version="2.19", docker_container="ubuntu2404", sops_version="3.10.0")
add_target(core_version="2.19", docker_container="fedora41", sops_version="3.10.2")
add_target(core_version="devel", docker_container="ubuntu2204", sops_version="3.6.0")
add_target(core_version="devel", docker_container="ubuntu2204", sops_version="3.7.0")
add_target(core_version="devel", docker_container="ubuntu2404", sops_version="3.9.1")
add_target(core_version="devel", docker_container=archlinux, python_version="3.13", sops_version="latest")
add_target(core_version="devel", docker_container=debian_bookworm, python_version="3.11", sops_version="latest")
add_target(core_version="devel", docker_container="ubuntu2404", sops_version="latest", gha_container="ubuntu-24.04-arm")

# Install specific sops
add_target(core_version="2.17", docker_container="ubuntu2204", target="gha/install/1/")
add_target(core_version="2.17", docker_container="fedora39", target="gha/install/1/")
add_target(core_version="2.18", docker_container="ubuntu2404", target="gha/install/1/")
add_target(core_version="2.18", docker_container="fedora40", target="gha/install/1/")
add_target(core_version="2.19", docker_container="ubuntu2404", target="gha/install/1/")
add_target(core_version="2.19", docker_container="fedora41", target="gha/install/1/")
# Install on localhost vs. remote host
add_target(core_version="devel", docker_container="ubuntu2204", target="gha/install/2/")
# Install latest sops
add_target(core_version="devel", docker_container=archlinux, python_version="3.13", target="gha/install/3/", github_latest_detection="auto")
add_target(core_version="devel", docker_container=debian_bookworm, python_version="3.11", target="gha/install/3/", github_latest_detection="auto")
add_target(core_version="2.16", docker_container=debian_bullseye, python_version="3.9", target="gha/install/3/", github_latest_detection="auto")
add_target(core_version="2.19", docker_container="fedora41", target="gha/install/3/", github_latest_detection="auto")
add_target(core_version="devel", docker_container="fedora42", target="gha/install/3/", github_latest_detection="auto")
add_target(core_version="devel", docker_container="ubuntu2204", target="gha/install/3/", github_latest_detection="api")
add_target(core_version="devel", docker_container="ubuntu2404", target="gha/install/3/", github_latest_detection="latest-release")
add_target(core_version="2.19", docker_container="alpine321", target="gha/install/3/", github_latest_detection="auto")
add_target(core_version="devel", docker_container="alpine322", target="gha/install/3/", github_latest_detection="auto")
# ARM 64
add_target(core_version="devel", docker_container="fedora42", target="gha/install/1/", github_latest_detection="auto", gha_container="ubuntu-24.04-arm")
add_target(core_version="devel", docker_container="ubuntu2204", target="gha/install/2/", github_latest_detection="auto", gha_container="ubuntu-24.04-arm")
add_target(core_version="devel", docker_container="alpine322", target="gha/install/3/", github_latest_detection="auto", gha_container="ubuntu-24.04-arm")


@nox.session(name="ansible-test-integration", default=False, python=False, requires=session_names)
def update_docs_fragments(session: nox.Session) -> None:
    """
    Meta session for running all ansible-test-integration-* sessions.
    """


# Allow to run the noxfile with `python noxfile.py`, `pipx run noxfile.py`, or similar.
# Requires nox >= 2025.02.09
if __name__ == "__main__":
    nox.main()
