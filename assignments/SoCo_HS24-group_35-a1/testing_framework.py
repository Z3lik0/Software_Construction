import time

def find_tests(module=None, prefix="test_"):
    """Find test functions within a module or the global namespace."""
    all_tests = {}
    search_space = module.__dict__ if module else globals()  # Check module or current globals
    
    for name, test in search_space.items():
        if name.startswith(prefix) and callable(test):
            all_tests[name] = test
    return all_tests

def run_tests(all_tests: dict, pattern: str = ""):
    """Run all tests and report results."""
    results = {"pass": 0, "fail": 0, "error": 0}
    results_deets = {"pass": [], "fail": [], "error": []}

    # Filter tests based on pattern
    if pattern:
        all_tests = {name: test for name, test in all_tests.items() if pattern.lower() in name.lower()}

    # Run tests
    for name, test in all_tests.items():
        start_time = time.time()
        try:
            test()
            results["pass"] += 1
            results_deets["pass"].append(name)
            print(f"Running {name}... \033[42mPASS\033[0m")
        except AssertionError as e:
            results["fail"] += 1
            results_deets["fail"].append(name)
            print(f"Running {name}... \033[43mFAIL:\033[0m {e}")
        except Exception as e:
            results["error"] += 1
            results_deets["error"].append(name)
            print(f"Running {name}... \033[41mERROR:\033[0m {e}")
        finally:
            duration = time.time() - start_time
            print(f"Test duration: {duration:.5f}s")

    # Summary
    print(f"\nResults: {results}")
    return results_deets

if __name__ == "__main__":
    # This file shouldn't directly run tests
    print("This is the test framework. Use it by importing in test files.")


#paste the following code into the test files and import the own module:

# if __name__ == "__main__":
#     pattern = ""
#     if "--select" in sys.argv:
#         index = sys.argv.index("--select") + 1
#         if index < len(sys.argv):
#             pattern = sys.argv[index]
    
#     # Pass test_vacations as the module
#     tests = find_tests(module=test_vacation_booking)
#     run_tests(tests, pattern=pattern)
