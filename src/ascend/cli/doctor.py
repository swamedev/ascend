import ast
import sys
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
SRC_DIR = PROJECT_ROOT / "src" / "ascend"
TESTS_DIR = PROJECT_ROOT / "tests"
PACKAGES_DIR = PROJECT_ROOT / "packages"
APPS_WEB_DIR = PROJECT_ROOT / "apps" / "web"


@dataclass
class CheckResult:
    check: str
    status: str
    detail: str = ""


@dataclass
class DoctorReport:
    checks: list[CheckResult] = field(default_factory=list)
    summary: str = ""

    def add(self, check: str, status: str, detail: str = "") -> None:
        self.checks.append(CheckResult(check=check, status=status, detail=detail))

    def print_report(self) -> None:
        passed = sum(1 for c in self.checks if c.status == "OK")
        failed = sum(1 for c in self.checks if c.status == "FAIL")
        warnings = sum(1 for c in self.checks if c.status == "WARN")
        total = len(self.checks)

        print("=" * 60)
        print("  ASCEND Doctor - Checkup")
        print("=" * 60)
        print()

        for c in self.checks:
            icon = {"OK": "[OK]", "FAIL": "[FAIL]", "WARN": "[WARN]"}.get(c.status, "[?]")
            print(f"  {icon} [{c.status}] {c.check}")
            if c.detail:
                print(f"      {c.detail}")

        print()
        print("-" * 60)
        print(f"  Result: {passed}/{total} passed, {failed} failed, {warnings} warnings")
        if failed > 0:
            print(f"  [FAIL] Some checks failed — review details above")

    @property
    def has_failed(self) -> bool:
        return any(c.status == "FAIL" for c in self.checks)

    @property
    def exit_code(self) -> int:
        return 1 if self.has_failed else 0


def get_py_files(directory: Path) -> list[Path]:
    return sorted(directory.rglob("*.py")) if directory.exists() else []


def count_lines(files: list[Path]) -> int:
    total = 0
    for f in files:
        try:
            total += len(f.read_text(encoding="utf-8").splitlines())
        except Exception:
            pass
    return total


def count_test_functions(files: list[Path]) -> int:
    count = 0
    for f in files:
        try:
            tree = ast.parse(f.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if node.name.startswith("test_"):
                        count += 1
                elif isinstance(node, ast.ClassDef):
                    if node.name.startswith("Test"):
                        count += 1
        except Exception:
            pass
    return count


def count_module_dirs() -> int:
    if not SRC_DIR.exists():
        return 0
    return sum(1 for d in SRC_DIR.iterdir() if d.is_dir() and not d.name.startswith("_") and not d.name.startswith("."))


def check_module_imports(module_path: Path, forbidden_patterns: list[str]) -> list[str]:
    violations = []
    for py_file in module_path.rglob("*.py"):
        try:
            tree = ast.parse(py_file.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        for pat in forbidden_patterns:
                            if alias.name.startswith(pat):
                                rel = py_file.relative_to(SRC_DIR)
                                violations.append(f"{rel} imports {alias.name}")
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        for pat in forbidden_patterns:
                            if node.module.startswith(pat):
                                rel = py_file.relative_to(SRC_DIR)
                                violations.append(f"{rel} imports {node.module}")
        except Exception:
            pass
    return violations


def run_git_command(cmd: list[str]) -> str:
    try:
        result = subprocess.run(
            ["git"] + cmd,
            capture_output=True, text=True, cwd=PROJECT_ROOT, timeout=30,
        )
        return result.stdout
    except Exception as e:
        return str(e)


def check_git_status() -> CheckResult:
    output = run_git_command(["status", "--porcelain"])
    if not output.strip():
        return CheckResult("Working tree", "OK", "clean")
    lines = output.strip().split("\n")
    modified = sum(1 for l in lines if l.startswith(" M") or l.startswith("M "))
    untracked = sum(1 for l in lines if l.startswith("?"))
    total = len(lines)
    detail = f"{total} files (M:{modified} U:{untracked})"
    if total == 0:
        return CheckResult("Working tree", "OK", "clean")
    return CheckResult("Working tree", "FAIL", detail)


def check_git_files_changed() -> CheckResult:
    output = run_git_command(["diff", "--stat"])
    staged = run_git_command(["diff", "--cached", "--stat"])
    untracked = run_git_command(["status", "--porcelain"])
    changed = 0
    for line in untracked.strip().split("\n"):
        if line.strip():
            changed += 1
    if output.strip():
        changed += len(output.strip().split("\n"))
    if changed <= 10:
        return CheckResult("Files changed", "OK", f"{changed} (limit: 10)")
    return CheckResult("Files changed", "FAIL", f"{changed} (limit: 10)")


def check_git_lines_changed() -> CheckResult:
    output = run_git_command(["diff", "--stat"])
    total_lines = 0
    for line in output.strip().split("\n"):
        parts = line.split()
        for i, p in enumerate(parts):
            if p.isdigit() and i + 1 < len(parts) and parts[i + 1] == "insertion":
                total_lines += int(p)
    if total_lines <= 500:
        return CheckResult("Lines changed", "OK", f"{total_lines} (limit: 500)")
    return CheckResult("Lines changed", "FAIL", f"{total_lines} (limit: 500)")


def check_tests_pass() -> CheckResult:
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", str(TESTS_DIR), "-q", "--no-header"],
            capture_output=True, text=True, timeout=60,
        )
        passed = result.returncode == 0
        if passed:
            return CheckResult("Tests", "OK", "All tests passing")
        return CheckResult("Tests", "FAIL", result.stdout.strip()[-200:])
    except Exception as e:
        return CheckResult("Tests", "FAIL", str(e))


def check_lint() -> CheckResult:
    if not (APPS_WEB_DIR / "package.json").exists():
        return CheckResult("Lint", "WARN", "No web app found, skipping")
    try:
        result = subprocess.run(
            ["npm", "run", "lint"],
            capture_output=True, text=True, cwd=APPS_WEB_DIR, timeout=60,
        )
        if result.returncode == 0:
            return CheckResult("Lint", "OK", "Lint clean")
        return CheckResult("Lint", "WARN", result.stdout.strip()[-200:])
    except Exception as e:
        return CheckResult("Lint", "WARN", str(e))


def check_build() -> CheckResult:
    if not (APPS_WEB_DIR / "package.json").exists():
        return CheckResult("Build", "WARN", "No web app found, skipping")
    try:
        result = subprocess.run(
            ["npm", "run", "build"],
            capture_output=True, text=True, cwd=APPS_WEB_DIR, timeout=120,
        )
        if result.returncode == 0:
            return CheckResult("Build", "OK", "Build successful")
        return CheckResult("Build", "FAIL", result.stdout.strip()[-200:])
    except Exception as e:
        return CheckResult("Build", "WARN", str(e))


def check_branch() -> CheckResult:
    output = run_git_command(["branch", "--show-current"])
    branch = output.strip()
    if branch:
        return CheckResult("Branch", "OK", branch)
    return CheckResult("Branch", "WARN", "Not on a branch")


def check_conflicts() -> CheckResult:
    output = run_git_command(["diff", "--name-only", "--diff-filter=U"])
    if not output.strip():
        return CheckResult("Merge conflicts", "OK", "None")
    return CheckResult("Merge conflicts", "FAIL", output.strip())


def check_doctor_passes() -> CheckResult:
    try:
        result = subprocess.run(
            [sys.executable, "-m", "ascend.cli.main", "doctor"],
            capture_output=True, text=True, timeout=60,
        )
        if result.returncode == 0:
            return CheckResult("ascend doctor", "OK", "All architecture checks pass")
        return CheckResult("ascend doctor", "FAIL", "Some architecture checks failed")
    except Exception as e:
        return CheckResult("ascend doctor", "WARN", str(e))


def check_docs_synced() -> CheckResult:
    return CheckResult("Documentation", "INFO", "Manual verification recommended")


def check_adr_present() -> CheckResult:
    adr_dir = PROJECT_ROOT / "docs" / "adr"
    if adr_dir.exists() and list(adr_dir.glob("*.md")):
        return CheckResult("ADRs", "OK", f"{len(list(adr_dir.glob('*.md')))} ADRs found")
    return CheckResult("ADRs", "WARN", "No ADRs found")


def check_rfc_present() -> CheckResult:
    rfc_dir = PROJECT_ROOT / "docs" / "rfc"
    if rfc_dir.exists() and list(rfc_dir.glob("*.md")):
        return CheckResult("RFCs", "OK", f"{len(list(rfc_dir.glob('*.md')))} RFCs found")
    return CheckResult("RFCs", "INFO", "No RFCs found (not always required)")


def check_versions_aligned() -> CheckResult:
    version_file = SRC_DIR / "api" / "version.py"
    if not version_file.exists():
        return CheckResult("Versions", "FAIL", "version.py not found")
    try:
        text = version_file.read_text(encoding="utf-8")
        versions = {}
        for line in text.split("\n"):
            if "=" in line and "VERSION" in line:
                parts = line.split("=")
                key = parts[0].strip().lower()
                val = parts[1].strip().strip('"')
                versions[key] = val
        all_aligned = all(v == versions.get("api_version") for k, v in versions.items())
        if all_aligned:
            return CheckResult("Versions aligned", "OK", ", ".join(f"{k}={v}" for k, v in versions.items()))
        return CheckResult("Versions aligned", "WARN", ", ".join(f"{k}={v}" for k, v in versions.items()))
    except Exception as e:
        return CheckResult("Versions", "WARN", str(e))


def check_changelog() -> CheckResult:
    changelog = PROJECT_ROOT / "CHANGELOG.md"
    if changelog.exists():
        return CheckResult("CHANGELOG", "OK", "Present")
    return CheckResult("CHANGELOG", "INFO", "Not required for all commits")


def check_min_coverage() -> CheckResult:
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", str(TESTS_DIR), "--cov=src/ascend", "--cov-report=term:skip-covered", "-q", "--no-header"],
            capture_output=True, text=True, timeout=120,
        )
        for line in result.stdout.splitlines():
            if "TOTAL" in line and "%" in line:
                parts = line.strip().split()
                for p in parts:
                    if p.endswith("%"):
                        cov = int(p.replace("%", ""))
                        status = "OK" if cov >= 50 else "WARN"
                        return CheckResult("Code coverage", status, p)
                break
        return CheckResult("Code coverage", "INFO", "Could not determine")
    except Exception as e:
        return CheckResult("Code coverage", "WARN", str(e))


# ─── Invariant Checks ────────────────────────────────────────────────────────


def check_invariant_domain_independence() -> CheckResult:
    domain_path = SRC_DIR / "domain"
    if not domain_path.exists():
        return CheckResult("I1 — Domain independe de Infrastructure", "FAIL", "domain/ not found")
    forbidden = ["infrastructure", "sqlite", "sqlalchemy", "flask", "django", "fastapi"]
    violations = check_module_imports(domain_path, forbidden)
    if violations:
        details = "; ".join(violations[:3])
        return CheckResult("I1 — Domain independe de Infrastructure", "FAIL", details)
    return CheckResult("I1 — Domain independe de Infrastructure", "OK")


def check_invariant_content_is_data() -> CheckResult:
    if not PACKAGES_DIR.exists():
        return CheckResult("I4 — Conteúdo é dado, não código", "WARN", "packages/ not found")
    py_files = list(PACKAGES_DIR.rglob("*.py"))
    if py_files:
        names = [f.relative_to(PACKAGES_DIR) for f in py_files[:3]]
        return CheckResult("I4 — Conteúdo é dado, não código", "FAIL", f"Python files in packages: {names}")
    return CheckResult("I4 — Conteúdo é dado, não código", "OK", f"{len(list(PACKAGES_DIR.glob('*/package.yaml')))} pacotes YAML")


def check_invariant_testable_without_gui() -> CheckResult:
    test_files = get_py_files(TESTS_DIR)
    if not test_files:
        return CheckResult("I7 — Testável sem GUI", "FAIL", "No test files found")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", str(TESTS_DIR), "-q", "--no-header"],
            capture_output=True, text=True, timeout=60,
        )
        passed = "passed" in result.stdout or "failed" in result.stdout
        if passed:
            return CheckResult("I7 — Testável sem GUI", "OK", "Tests executable via CLI")
        return CheckResult("I7 — Testável sem GUI", "WARN", result.stdout.strip()[:100])
    except Exception as e:
        return CheckResult("I7 — Testável sem GUI", "WARN", str(e))


def check_invariant_no_telemetry() -> CheckResult:
    src_files = get_py_files(SRC_DIR)
    for f in src_files:
        if f.name == "doctor.py":
            continue
        try:
            text = f.read_text(encoding="utf-8")
            if "telemetry" in text.lower() or "analytics" in text.lower():
                rel = f.relative_to(SRC_DIR)
                return CheckResult("I8 — Dados pertencem ao usuário (sem telemetria)", "WARN", f"Found reference in {rel}")
        except Exception:
            pass
    return CheckResult("I8 — Dados pertencem ao usuário (sem telemetria)", "OK")


# ─── Standard Health Checks ──────────────────────────────────────────────────


def check_project_structure() -> list[CheckResult]:
    results = []
    src_files = get_py_files(SRC_DIR)
    test_files = get_py_files(TESTS_DIR)
    src_lines = count_lines(src_files)
    test_lines = count_lines(test_files)
    results.append(CheckResult("Arquivos fonte", "OK", f"{len(src_files)} .py files, {src_lines} lines"))
    results.append(CheckResult("Arquivos de teste", "OK", f"{len(test_files)} .py files, {test_lines} lines"))
    results.append(CheckResult("Módulos", "OK", f"{count_module_dirs()} módulos em src/ascend/"))
    results.append(CheckResult("Pacotes de conteúdo", "OK", f"{len(list(PACKAGES_DIR.glob('*/package.yaml')))} pacotes APS"))
    results.append(CheckResult("Documentos fundação", "OK", f"{len(list((PROJECT_ROOT / 'foundation').glob('*.md')))} documentos"))
    results.append(CheckResult("Especificações (spec)", "OK", f"{len(list((PROJECT_ROOT / 'docs/spec').glob('*.md')))} specs"))
    return results


def check_runtime_health() -> list[CheckResult]:
    results = []
    runtime_path = SRC_DIR / "runtime"
    if not runtime_path.exists():
        results.append(CheckResult("Runtime Kernel", "FAIL", "runtime/ not found"))
        return results
    required = {
        "kernel.py": "RuntimeKernel",
        "orchestrator.py": "RuntimeOrchestrator",
        "context.py": "RuntimeContext",
        "hooks.py": "RuntimeHooks",
        "report.py": "ExecutionReport",
        "models.py": "RuntimePackage",
    }
    for fname, component in required.items():
        fpath = runtime_path / fname
        if fpath.exists():
            results.append(CheckResult(f"Runtime: {component}", "OK"))
        else:
            results.append(CheckResult(f"Runtime: {component}", "FAIL", f"{fname} not found"))
    runners_path = runtime_path / "runners"
    if runners_path.exists():
        runner_files = ["challenge_runner.py", "mission_runner.py", "journey_runner.py"]
        for fname in runner_files:
            if (runners_path / fname).exists():
                results.append(CheckResult(f"Runner: {fname.replace('.py', '')}", "OK"))
    return results


def check_package_health() -> list[CheckResult]:
    results = []
    if not PACKAGES_DIR.exists():
        results.append(CheckResult("Package Loader", "FAIL", "packages/ not found"))
        return results
    try:
        from ascend.package_engine.loader import PackageLoader
        loader = PackageLoader()
        pkg_dirs = sorted(PACKAGES_DIR.glob("*/package.yaml"))
        valid = 0
        invalid = 0
        for pkg_file in pkg_dirs:
            pkg_dir = pkg_file.parent
            try:
                pkg, result = loader.load(pkg_dir)
                if result.valid:
                    valid += 1
                else:
                    invalid += 1
            except Exception:
                invalid += 1
        if invalid == 0:
            results.append(CheckResult("Pacotes válidos", "OK", f"{valid}/{len(pkg_dirs)} pacotes válidos"))
        else:
            results.append(CheckResult("Pacotes válidos", "FAIL", f"{valid}/{len(pkg_dirs)} válidos, {invalid} inválidos"))
    except ImportError as e:
        results.append(CheckResult("Package Loader", "FAIL", str(e)))
    return results


def check_test_health() -> list[CheckResult]:
    results = []
    test_files = get_py_files(TESTS_DIR)
    if not test_files:
        results.append(CheckResult("Testes", "FAIL", "No tests found"))
        return results
    try:
        test_count = 0
        for f in test_files:
            try:
                tree = ast.parse(f.read_text(encoding="utf-8"))
                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        if node.name.startswith("test_"):
                            test_count += 1
            except Exception:
                pass
        result = subprocess.run(
            [sys.executable, "-m", "pytest", str(TESTS_DIR), "-q", "--no-header"],
            capture_output=True, text=True, timeout=60,
        )
        output = result.stdout.strip()
        passed = result.returncode == 0
        if passed:
            results.append(CheckResult("Testes passando", "OK", output.split("\n")[-1] if output else f"{test_count} tests"))
        else:
            results.append(CheckResult("Testes passando", "FAIL", output.split("\n")[-1] if output else "Falha nos testes"))
        cov_result = subprocess.run(
            [sys.executable, "-m", "pytest", str(TESTS_DIR), "--cov=src/ascend", "--cov-report=term:skip-covered", "-q", "--no-header"],
            capture_output=True, text=True, timeout=120,
        )
        for line in cov_result.stdout.splitlines():
            if "TOTAL" in line and "%" in line:
                parts = line.strip().split()
                for p in parts:
                    if p.endswith("%"):
                        results.append(CheckResult("Cobertura de código", "OK", p))
                        break
                break
    except Exception as e:
        results.append(CheckResult("Testes", "WARN", str(e)))
    return results


def check_architecture_layers() -> list[CheckResult]:
    results = []
    layer_map = {
        "domain": "domain",
        "application": "application",
        "infrastructure": "infrastructure",
        "runtime": "runtime",
        "cli": "cli",
        "api": "api",
        "package_engine": "package_engine",
        "shared": "shared",
    }
    for name, subdir in layer_map.items():
        path = SRC_DIR / subdir
        init_file = path / "__init__.py" if (path / "__init__.py").exists() else None
        files = list(path.rglob("*.py")) if path.exists() else []
        status = "OK" if files else "FAIL"
        detail = f"{len(files)} arquivos" if files else "não encontrado"
        results.append(CheckResult(f"Camada: {name}", status, detail))
    domain_path = SRC_DIR / "domain"
    infra_imports = check_module_imports(domain_path, ["infrastructure", "sqlite"])
    if infra_imports:
        results.append(CheckResult("Clean Architecture: Domain puro", "FAIL", "domain importa infrastructure"))
    else:
        results.append(CheckResult("Clean Architecture: Domain puro", "OK"))
    return results


# ─── Doctor Modes ────────────────────────────────────────────────────────────


def run_architecture() -> DoctorReport:
    report = DoctorReport()
    report.add("ASCEND Runtime", "OK", f"v0.1.0 | Python {sys.version.split()[0]}")
    for check in check_project_structure():
        report.checks.append(check)
    for check in check_architecture_layers():
        report.checks.append(check)
    report.checks.append(check_invariant_domain_independence())
    report.checks.append(check_invariant_content_is_data())
    report.checks.append(check_invariant_testable_without_gui())
    report.checks.append(check_invariant_no_telemetry())
    for check in check_runtime_health():
        report.checks.append(check)
    for check in check_package_health():
        report.checks.append(check)
    for check in check_test_health():
        report.checks.append(check)
    return report


def run_workflow() -> DoctorReport:
    report = DoctorReport()
    report.add("ASCEND Workflow Check", "OK", "OPERAÇÃO HERMES II enforcement")
    report.checks.append(check_git_status())
    report.checks.append(check_git_files_changed())
    report.checks.append(check_git_lines_changed())
    report.checks.append(check_branch())
    report.checks.append(check_conflicts())
    report.checks.append(check_tests_pass())
    report.checks.append(check_lint())
    report.checks.append(check_build())
    report.checks.append(check_doctor_passes())
    report.checks.append(check_docs_synced())
    report.checks.append(check_adr_present())
    report.checks.append(check_rfc_present())
    return report


def run_release() -> DoctorReport:
    report = DoctorReport()
    report.add("ASCEND Release Check", "OK", "Release readiness verification")
    report.checks.append(check_git_status())
    report.checks.append(check_branch())
    report.checks.append(check_conflicts())
    report.checks.append(check_tests_pass())
    report.checks.append(check_build())
    report.checks.append(check_lint())
    report.checks.append(check_min_coverage())
    report.checks.append(check_docs_synced())
    report.checks.append(check_versions_aligned())
    report.checks.append(check_changelog())
    return report


def run(mode: str = "architecture") -> None:
    if mode == "architecture":
        report = run_architecture()
    elif mode == "workflow":
        report = run_workflow()
    elif mode == "release":
        report = run_release()
    else:
        print(f"[FAIL] Unknown doctor mode: {mode}")
        sys.exit(1)
    report.print_report()
    sys.exit(report.exit_code)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "architecture"
    run(mode)
