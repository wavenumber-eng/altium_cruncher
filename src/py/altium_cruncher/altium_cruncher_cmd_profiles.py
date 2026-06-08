"""Altium ProgramData profile inspection and cleanup command."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from altium_cruncher.altium_environment import (
    AltiumProfile,
    clean_altium_profiles,
    discover_altium_profiles,
)


def cmd_profiles(args: argparse.Namespace) -> int:
    """Run the profiles list or clean action."""
    action = str(getattr(args, "profiles_action", "list") or "list")
    profiles = _load_profiles(args)
    if action == "clean":
        return _cmd_profiles_clean(args, profiles)
    return _cmd_profiles_list(args, profiles)


def _load_profiles(args: argparse.Namespace) -> list[AltiumProfile]:
    programdata_root = (
        Path(args.programdata_root).resolve() if args.programdata_root else None
    )
    return discover_altium_profiles(
        module_name=str(getattr(args, "module", "ad-panel-monkey")),
        programdata_root=programdata_root,
    )


def _cmd_profiles_clean(
    args: argparse.Namespace,
    profiles: list[AltiumProfile],
) -> int:
    try:
        actions = clean_altium_profiles(
            profiles,
            profile_guid=getattr(args, "profile_guid", None),
            all_profiles=bool(getattr(args, "all", False)),
            dry_run=bool(getattr(args, "dry_run", False)),
        )
    except Exception as exc:
        print(f"profiles clean failed: {exc}", file=sys.stderr)
        return 1
    payload = {
        "schema": "altium_cruncher.profiles.clean.a0",
        "actions": actions,
    }
    if getattr(args, "json", False):
        print(json.dumps(payload, indent=2))
        return 0
    _print_clean_actions(actions)
    return 0


def _cmd_profiles_list(
    args: argparse.Namespace,
    profiles: list[AltiumProfile],
) -> int:
    payload = {
        "schema": "altium_cruncher.profiles.a0",
        "profiles": [profile.to_dict() for profile in profiles],
    }
    if getattr(args, "json", False):
        print(json.dumps(payload, indent=2))
        return 0
    if not profiles:
        print("No Altium ProgramData profiles found.")
        return 0
    for profile in profiles:
        state = _profile_state_labels(profile)
        suffix = f" ({', '.join(state)})" if state else ""
        print(f"{profile.guid}  {profile.path}{suffix}")
    return 0


def _print_clean_actions(actions: list[dict[str, object]]) -> None:
    if not actions:
        print("No matching Altium profiles found.")
    for action_row in actions:
        state = "dry-run" if action_row["dry_run"] else "cleaned"
        print(
            f"{state}: {action_row['profile_guid']} "
            f"module_dir={action_row['removed_module_dir']} "
            f"registry={action_row['removed_registry_item']}"
        )


def _profile_state_labels(profile: AltiumProfile) -> list[str]:
    state = []
    if profile.registered:
        state.append("registered")
    if profile.module_dir_exists:
        state.append("module-dir")
    if profile.dll_exists:
        state.append("dll")
    return state


def _add_common_profile_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--module",
        default="ad-panel-monkey",
        help="extension module name to inspect or clean (default: ad-panel-monkey)",
    )
    parser.add_argument(
        "--programdata-root",
        type=Path,
        help="override Altium ProgramData root for tests or custom installs",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="write machine-readable JSON",
    )


def register_parser(
    subparsers: argparse._SubParsersAction,
) -> argparse.ArgumentParser:
    """Register the profiles command parser."""
    parser = subparsers.add_parser(
        "profiles",
        help="list or clean Altium ProgramData profile extension state",
        description=(
            "Inspect Altium Designer ProgramData profile folders and selected "
            "extension registry entries. Cleanup targets extension module state "
            "and requires an explicit clean action plus --all or --profile-guid."
        ),
    )
    action_subparsers = parser.add_subparsers(
        dest="profiles_action",
        metavar="<profiles-action>",
    )

    list_parser = action_subparsers.add_parser(
        "list",
        help="list profile folders and extension state",
    )
    _add_common_profile_arguments(list_parser)
    list_parser.set_defaults(handler=cmd_profiles)

    clean_parser = action_subparsers.add_parser(
        "clean",
        help="remove selected extension module dirs and registry items",
    )
    _add_common_profile_arguments(clean_parser)
    clean_parser.add_argument(
        "--profile-guid",
        help="clean one profile GUID",
    )
    clean_parser.add_argument(
        "--all",
        action="store_true",
        help="clean all discovered profiles",
    )
    clean_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="report cleanup actions without deleting files",
    )
    clean_parser.set_defaults(handler=cmd_profiles)

    _add_common_profile_arguments(parser)
    parser.set_defaults(handler=cmd_profiles, profiles_action="list")
    return parser
