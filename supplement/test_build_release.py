#!/usr/bin/env python3
"""Adversarial regressions for the main-paper release gate."""

from __future__ import annotations

import argparse
import copy
import io
import json
import tarfile
import tempfile
from pathlib import Path

import build_release


def expect_value_error(function, label: str) -> None:
    try:
        function()
    except ValueError:
        return
    raise AssertionError(f"{label} was accepted")


def write_single_member(
    path: Path,
    name: str,
    data: bytes,
    *,
    uname: str = "",
    linkname: str = "",
    pax_headers: dict[str, str] | None = None,
) -> None:
    with tarfile.open(
        path,
        mode="w:xz",
        format=tarfile.PAX_FORMAT,
        preset=0,
    ) as archive:
        info = tarfile.TarInfo(name)
        info.size = len(data)
        info.mode = 0o644
        info.mtime = 0
        info.uid = 0
        info.gid = 0
        info.uname = uname
        info.gname = ""
        info.linkname = linkname
        info.pax_headers = pax_headers or {}
        archive.addfile(info, io.BytesIO(data))


def main() -> None:
    paths = build_release.selected_paths()
    provenance = build_release.git_provenance(paths)
    payloads = build_release.snapshot_payloads(paths)
    manifest = build_release.release_manifest(paths, provenance, payloads)
    encoded = build_release.manifest_bytes(manifest)
    build_release.validate_release_manifest(json.loads(encoded))

    empty = copy.deepcopy(manifest)
    empty["files"] = []
    expect_value_error(
        lambda: build_release.validate_release_manifest(empty),
        "empty main-paper profile",
    )
    if build_release.safe_member_name(
        f"{build_release.ARCHIVE_ROOT}/a\\..\\..\\escape.txt"
    ):
        raise AssertionError("backslash traversal name was accepted")
    committed = b"committed snapshot\n"
    snapshot_provenance = {
        "git_object_format": "sha1",
        "selected_index_blobs": {
            "payload": build_release.git_blob_hash(committed, "sha1")
        },
    }
    if build_release.snapshot_index_mismatches(
        {"payload": committed},
        snapshot_provenance,
    ):
        raise AssertionError("index-identical payload snapshot was rejected")
    if build_release.snapshot_index_mismatches(
        {"payload": b"transient bytes\n"},
        snapshot_provenance,
    ) != ["payload"]:
        raise AssertionError("transient payload snapshot was accepted")

    with tempfile.TemporaryDirectory() as output_directory:
        outside_manifest = Path(output_directory) / "manifest.json"
        expect_value_error(
            lambda: build_release.build(
                argparse.Namespace(
                    archive=build_release.ROOT / "paper/main.tex",
                    manifest=outside_manifest,
                    allow_dirty=True,
                )
            ),
            "archive/source collision",
        )
        expect_value_error(
            lambda: build_release.build(
                argparse.Namespace(
                    archive=Path(output_directory) / "archive.tar.xz",
                    manifest=build_release.ROOT / "paper/main.tex",
                    allow_dirty=True,
                )
            ),
            "manifest/source collision",
        )

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)

        wrong_order = root / "wrong-order.tar.xz"
        first_payload = (
            f"{build_release.ARCHIVE_ROOT}/"
            f"{build_release.PROFILE_PATHS[0]}"
        )
        write_single_member(wrong_order, first_payload, b"")
        expect_value_error(
            lambda: build_release.verify_archive(wrong_order, encoded),
            "non-canonical member order",
        )

        unsafe = root / "unsafe.tar.xz"
        write_single_member(
            unsafe,
            f"{build_release.ARCHIVE_ROOT}/a\\..\\..\\escape.txt",
            b"",
        )
        expect_value_error(
            lambda: build_release.verify_archive(unsafe, encoded),
            "Windows-unsafe member name",
        )

        bad_owner = root / "bad-owner.tar.xz"
        write_single_member(
            bad_owner,
            build_release.MANIFEST_MEMBER,
            encoded,
            uname="attacker",
        )
        expect_value_error(
            lambda: build_release.verify_archive(bad_owner, encoded),
            "non-canonical owner metadata",
        )

        bad_link = root / "bad-link.tar.xz"
        write_single_member(
            bad_link,
            build_release.MANIFEST_MEMBER,
            encoded,
            linkname="ignored-target",
        )
        expect_value_error(
            lambda: build_release.verify_archive(bad_link, encoded),
            "non-canonical link metadata",
        )

        bad_pax = root / "bad-pax.tar.xz"
        write_single_member(
            bad_pax,
            build_release.MANIFEST_MEMBER,
            encoded,
            pax_headers={"comment": "non-canonical"},
        )
        expect_value_error(
            lambda: build_release.verify_archive(bad_pax, encoded),
            "non-canonical PAX metadata",
        )

    print(
        "PASS release-gate adversarial checks: explicit profile, "
        "snapshot binding, output isolation, path safety, order, owner, "
        "link, and PAX metadata"
    )


if __name__ == "__main__":
    main()
