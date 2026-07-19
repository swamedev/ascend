import argparse
import sys
from pathlib import Path

from ascend.api.runtime import Runtime
from ascend.runtime.report import ExecutionReport


def main() -> None:
    parser = argparse.ArgumentParser(prog="ascend", description="ASCEND Runtime")
    parser.add_argument("--version", action="store_true", help="Show version")
    sub = parser.add_subparsers(dest="command")

    pkg = sub.add_parser("package", help="Package commands")
    pkg_sub = pkg.add_subparsers(dest="subcommand")
    pkg_validate = pkg_sub.add_parser("validate", help="Validate a package")
    pkg_validate.add_argument("path", nargs="?", default=".", help="Package path")
    pkg_create = pkg_sub.add_parser("create", help="Create a new package")
    pkg_create.add_argument("name", help="Package name")

    run_parser = sub.add_parser("run", help="Run a package")
    run_parser.add_argument("path", nargs="?", default=".", help="Package path")
    run_parser.add_argument("--builder", default="default", help="Builder username")
    run_parser.add_argument("--evidence", help="Evidence file path or text")

    init_parser = sub.add_parser("init", help="Initialize a new package")
    init_parser.add_argument("name", nargs="?", default="my-package", help="Package name")

    sub.add_parser("doctor", help="Check system health")

    prog_parser = sub.add_parser("progress", help="Show builder progress")
    prog_parser.add_argument("--builder", default="default", help="Builder username")

    args = parser.parse_args()

    if args.version:
        _cmd_version()
    elif args.command == "run":
        _cmd_run(args)
    elif args.command == "package":
        _cmd_package(args)
    elif args.command == "init":
        _cmd_init(args)
    elif args.command == "doctor":
        _cmd_doctor()
    elif args.command == "progress":
        _cmd_progress(args)
    else:
        parser.print_help()


def _cmd_version() -> None:
    print("ASCEND Runtime v0.1.0")


def _cmd_run(args: argparse.Namespace) -> None:
    pkg_path = Path(args.path)
    if not (pkg_path / "package.yaml").exists():
        print(f"Error: no package.yaml found in {pkg_path}")
        sys.exit(1)

    evidence = args.evidence or ""
    rt = Runtime()
    report = rt.run(package=pkg_path, builder=args.builder, evidence=evidence)
    print(report.summary())


def _cmd_package(args: argparse.Namespace) -> None:
    if args.subcommand == "validate":
        _cmd_package_validate(args)
    elif args.subcommand == "create":
        _cmd_package_create(args)
    else:
        print("Usage: ascend package <validate|create> [options]")


def _cmd_package_validate(args: argparse.Namespace) -> None:
    from ascend.package_engine.loader import PackageLoader

    pkg_path = Path(args.path)
    loader = PackageLoader()
    pkg, result = loader.load(pkg_path)
    if result.valid:
        print(f"[OK] Package '{pkg.id}' v{pkg.version} is valid.")
        if result.warnings:
            for w in result.warnings:
                print(f"  [!] [{w.rule}] {w.message}")
    else:
        print(f"[FAIL] Package validation failed:")
        for e in result.errors:
            print(f"  [{e.level}] {e.rule}: {e.message}")
        sys.exit(1)


def _cmd_package_create(args: argparse.Namespace) -> None:
    name = args.name
    dest = Path.cwd() / name
    if dest.exists():
        print(f"Error: {dest} already exists")
        sys.exit(1)
    dest.mkdir(parents=True)
    (dest / "package.yaml").write_text(
        f'metadata:\n  id: {name}\n  version: 0.1.0\n  title: {name}\n  description: ""\n  author: ""\n  license: MIT\n\nspec:\n  runtime: ">=1.0"\n  language: en\n  estimated_hours: 1\n  dependencies: []\n\ncapabilities:\n  - evidence\n',
        encoding="utf-8",
    )
    (dest / "competencies").mkdir(exist_ok=True)
    (dest / "achievements").mkdir(exist_ok=True)
    (dest / "assessments").mkdir(exist_ok=True)
    (dest / "journeys").mkdir(exist_ok=True)
    (dest / "README.md").write_text(f"# {name}\n\nASCEND package.\n", encoding="utf-8")
    print(f"[OK] Package '{name}' created at {dest}")


def _cmd_init(args: argparse.Namespace) -> None:
    _cmd_package_create(args)


def _cmd_doctor() -> None:
    from ascend.cli.doctor import run as doctor_run
    doctor_run()


def _cmd_progress(args: argparse.Namespace) -> None:
    from ascend.infrastructure.persistence.sqlite.connection import ConnectionManager
    from ascend.infrastructure.persistence.sqlite.builder_repository import SQLiteBuilderRepository

    db_path = Path(".ascend.db")
    if not db_path.exists():
        print(f"[!] No local database found at {db_path.absolute()}")
        print("[!] Run a mission first to initialize your local ledger.")
        sys.exit(1)

    conn_manager = ConnectionManager(str(db_path))
    repo = SQLiteBuilderRepository(conn_manager)

    try:
        builder = repo.get_by_username(args.builder)
        if not builder:
            print(f"[!] Builder '{args.builder}' not found in the local ledger.")
            sys.exit(1)

        print(f"\n⚜️  ASCEND DOSSIER: {builder.username.upper()} ⚜️")
        print("=" * 40)
        print(f"NÍVEL: {builder.level}  |  XP TOTAL: {builder.xp}")
        print("-" * 40)

        print(f"COMPETÊNCIAS COMPROVADAS ({len(builder.competencies)}):")
        if not builder.competencies:
            print("  (Nenhuma competência desbloqueada ainda)")
        for c in builder.competencies:
            print(f"  ✓ {c.name} (Nível {c.level})")

        print("-" * 40)
        print(f"CONQUISTAS ({len(builder.achievements)}):")
        if not builder.achievements:
            print("  (Nenhuma conquista obtida)")
        for a in builder.achievements:
            print(f"  ★ {a.name}")
        print("=" * 40 + "\n")

    finally:
        conn_manager.close()


if __name__ == "__main__":
    main()
