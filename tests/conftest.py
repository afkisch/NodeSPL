def pytest_runtest_logreport(report):
    if report.longrepr:
        report.longrepr = str(report.longrepr).replace(
            "X-API-KEY", "X-API-KEY: ***HIDDEN***"
        )