# Calculator Project Structure Required to Use runtests.py Program.
#
# runtests.py
# bin/
# obj/
# src/
# tests/
#   ignored_functions.json
#   group_of_related_tests/
#     test_1/
#       bin/
#       obj/
#       src/
#       autotest.json
#       makefile
#       test_info.json
#     test_2/
#     ...
#   test_1/
#     bin/
#     obj/
#     src/
#     autotest.json
#       makefile
#       test_info.json
#   test_2/
#   ...


import json
import os
import subprocess
from typing import Any, Optional, Union


SOURCE_DIRECTORY_NAME: str = "src"
TESTING_ROM_ABSOLUTE_PATH: str = os.path.abspath("testing_rom.rom")
ABSOLUTE_PATH_TO_ROOT_TEST_DIRECTORY: str = os.path.abspath("tests")
IGNORED_DEPENDENCIES_JSON_FILENAME: str = "ignored_dependencies.json"
TEST_INFO_JSON_FILENAME: str = "test_info.json"
TEST_SOURCE_DIRECTORY_NAME: str = "src"
AUTOTEST_JSON_FILENAME: str = "autotest.json"

TERMINAL_LINE_WIDTH: int = 80
CLEAN_THEN_BUILD_TESTS: bool = False
ABORT_ON_FIRST_FAILED_TEST: bool = False
PRINT_DEPENDENCY_TRACE_INFO: bool = True
PRINT_BATCHES: bool = False


class IgnoredFunctions:
    _identifiers: list[str] = []

    def __init__(self):
        with open(
            os.path.join(
                ABSOLUTE_PATH_TO_ROOT_TEST_DIRECTORY,
                IGNORED_DEPENDENCIES_JSON_FILENAME,
            )
        ) as file:
            self._identifiers = json.load(file)
        return

    def includes(self, function_identifier: str) -> bool:
        if function_identifier in self._identifiers:
            return True

        return False


def print_empty_line() -> None:
    print("")
    return


def print_divider() -> None:
    print("=" * TERMINAL_LINE_WIDTH)
    return


def print_subdivider() -> None:
    print("-" * TERMINAL_LINE_WIDTH)
    return


def print_centered(string: str) -> None:
    padding_width: int = (TERMINAL_LINE_WIDTH - len(string)) // 2

    print(" " * padding_width + string)
    return


def print_section_header(header_name: str) -> None:
    print_empty_line()
    print_subdivider()
    print_centered(header_name.upper())
    print_subdivider()
    print_empty_line()
    return


def print_and_wrap_on_space(string: str) -> None:
    start: int = 0
    end: int = 0
    skip_space: bool = False

    while end < len(string):
        end += min(TERMINAL_LINE_WIDTH, len(string) - end)
        skip_space = False

        if end < len(string):
            original_end: int = end
            while string[end] != " ":
                end -= 1

            if end < start:
                end = original_end
            else:
                skip_space = True

        print(string[start:end])
        start = end

        if skip_space:
            start += 1

    return


def print_program_banner() -> None:
    print_divider()
    print_centered("TI-84 Plus CE SDK Automated Test Framework")
    print_centered("By Captain Calc")
    print_divider()
    return


def print_function_name(mangled_function_name: str) -> None:
    print(
        unmangle_cxx_function_name(mangled_function_name)
        + " ("
        + mangled_function_name
        + ")"
    )
    return


def print_advice(advice: Optional[list[str]]) -> None:
    if advice is None:
        return

    LINE_LENGTH: int = TERMINAL_LINE_WIDTH - 5
    item_count: int = 1

    print("ADVICE:")

    for item in advice:
        start: int = 0
        end: int = 0
        skip_space: bool = False

        while end < len(item):
            end += min(TERMINAL_LINE_WIDTH, len(item) - end)
            skip_space = False

            if end < len(item):
                original_end: int = end
                while item[end] != " ":
                    end -= 1

                if end < start:
                    end = original_end
                else:
                    skip_space = True

            if start == 0:
                print(f"  {item_count}. {item[start:end]}")
            else:
                print(f"     {item[start:end]}")

            start = end

            if skip_space:
                start += 1

        item_count += 1

    return


def report_warning(message: str, advice: Optional[list[str]] = None) -> None:
    print_empty_line()
    print_and_wrap_on_space("WARNING: " + message)
    print_advice(advice)
    return


def report_fatal_error_then_exit(
    message: str, advice: Optional[list[str]] = None
) -> None:
    print_empty_line()
    print_and_wrap_on_space("FATAL ERROR: " + message)
    print_advice(advice)
    print_empty_line()
    print_divider()
    print_empty_line()
    print_centered("TESTING ABORTED")
    print_empty_line()
    exit(1)


def get_test_identifier(
    absolute_root_test_directory_path: str, absolute_test_directory_path: str
) -> str:
    return os.path.relpath(
        absolute_test_directory_path, absolute_root_test_directory_path
    )


def clean_old_build_files(
    absolute_test_directory_path: str, absolute_root_test_directory_path: str
) -> None:
    try:
        os.chdir(absolute_test_directory_path)
        subprocess.run(["make", "clean"], check=True)
        os.chdir(absolute_root_test_directory_path)
    except subprocess.CalledProcessError as error:
        print_empty_line()
        report_fatal_error_then_exit(
            error.__str__(), ["Unprecendented failure of make clean. Investigate."]
        )

    return


def build_test_in_debug_mode(
    absolute_test_directory_path: str, absolute_root_test_directory_path: str
) -> None:
    try:
        os.chdir(absolute_test_directory_path)
        # The capture_output flag will not work here because it prevents
        # the debug files from being written.
        subprocess.run(["make", "debug"], check=True)
        os.chdir(absolute_root_test_directory_path)
    except subprocess.CalledProcessError as error:
        print_empty_line()
        report_fatal_error_then_exit(
            error.__str__(), ["Manually build the test and fix the compiler errors."]
        )

    return


def unmangle_cxx_function_name(name: str) -> str:
    output: str = ""

    try:
        output = subprocess.check_output(
            ["c++filt", "--types", "--strip-underscore", f"{name}"]
        )
    except subprocess.CalledProcessError as error:
        print_empty_line()
        report_fatal_error_then_exit(error.__str__())

    return output.strip().decode()


def remove_ignored_dependencies(
    dependencies: list[str],
) -> list[dict[str, (str | list[str])]]:
    try:
        ignored_functions = IgnoredFunctions()
    except FileNotFoundError as error:
        report_fatal_error_then_exit(
            error.__str__(),
            [
                "The file may not exist.",
                "The file may not be in the location the testing program expects.",
                "The file may not have the filename that the testing program expects.",
            ],
        )

    final_dependencies: list[str] = []

    for dependency in dependencies:
        if not ignored_functions.includes(unmangle_cxx_function_name(dependency)):
            final_dependencies.append(dependency)

    return final_dependencies


def extract_all_functions_from_object_file(
    absolute_filepath: str,
) -> list[dict[str, (str | list[str])]]:
    contents: list[str] = []
    functions: list[dict[str, (str | list[str])]] = []

    with open(absolute_filepath, "rb") as file:
        contents = file.readlines()

    index: int = 0

    while index < len(contents):
        line: str = contents[index]

        if line.startswith(b"__") or line.startswith(b"_main"):
            mangled_function_name: str = line.strip().rstrip(b":").decode()
            functions.append(
                {
                    "name": mangled_function_name,
                    "dependencies": [],
                }
            )

            while index < len(contents):
                line = contents[index]

                if line.startswith(b"\tcall\t"):
                    line = line.strip()
                    function_name_start: int = 0

                    try:
                        function_name_start = line.rindex(b" ") + 1
                    except ValueError:
                        function_name_start = line.rindex(b"\t") + 1

                    line = line[function_name_start: ]
                    mangled_function_name: str = line.decode()

                    if mangled_function_name not in functions[-1]["dependencies"]:
                        functions[-1]["dependencies"].append(mangled_function_name)

                if b"cfi_endproc" in line:
                    break

                index += 1
        else:
            index += 1

    if PRINT_DEPENDENCY_TRACE_INFO == True:
        print_empty_line()
        print(f"All Functions Found In '{os.path.basename(absolute_filepath)}':")
        print_empty_line()
        for function in functions:
            print(
                unmangle_cxx_function_name(function["name"])
                + " ("
                + function["name"]
                + "):"
            )

            for dependency in function["dependencies"]:
                print("  ", end="")
                print_function_name(dependency)

    return functions


def extract_functions_test_uses(absolute_filepath: str) -> list[str]:
    """
    Merges the dependencies of all static and local functions in the test's
    main.cpp into the dependencies of the test's main() function.

    absolute_filepath: Absolute file path to the test's main.cpp.src object
                       file.
    """
    functions: list[
        dict[str, (str | list[str])]
    ] = extract_all_functions_from_object_file(absolute_filepath)

    for function in functions:
        if function["name"] == "_main":
            main_function = function

        # This prevents the dependency merger from endlessly following
        # recursive functions.
        if function["name"] in function["dependencies"]:
            function["dependencies"].remove(function["name"])

        for other_function in functions:
            if function["name"] in other_function["dependencies"]:
                other_function["dependencies"].remove(function["name"])
                other_function["dependencies"] = set(
                    other_function["dependencies"] + function["dependencies"]
                )

    if PRINT_DEPENDENCY_TRACE_INFO == True:
        print_empty_line()
        print("Linked Functions Test Uses:")
        print_empty_line()

        for dependency in main_function["dependencies"]:
            print("  ", end="")
            print_function_name(dependency)

    return main_function["dependencies"]


def trace_dependencies(
    dependencies: list[str], functions: list[dict[str, (str | list[str])]]
) -> list[str]:
    trace: list[str] = []

    def trace_dependencies_worker(
        dependencies: list[str],
        functions: list[dict[str, (str | list[str])]],
        trace,
        count=1,
    ) -> list[str]:
        for dependency in dependencies:
            if PRINT_DEPENDENCY_TRACE_INFO == True:
                print(("  " * count) + dependency)

            # The if-statement prevents recursive functions making the trace
            # continue indefinitely.
            if dependency not in trace:
                trace.append(dependency)
                for function in functions:
                    if dependency == function["name"]:
                        trace = list(
                            set(
                                trace
                                + list(
                                    trace_dependencies_worker(
                                        function["dependencies"],
                                        functions,
                                        trace,
                                        count + 1,
                                    )
                                )
                            )
                        )

        return trace

    return trace_dependencies_worker(dependencies, functions, trace)


def trace_dependencies_for_test(
    absolute_test_directory_path: str, used_functions: list[str]
) -> list[str]:
    linked_functions: list[dict[str, (str | list[str])]] = []

    absolute_obj_path: str = os.path.join(absolute_test_directory_path, "obj/_..")

    for dirpath, dirnames, filenames in os.walk(absolute_obj_path):
        for file in filenames:
            if file.endswith(".cpp.src"):
                linked_functions += extract_all_functions_from_object_file(
                        os.path.join(dirpath, file)
                    )

    if PRINT_DEPENDENCY_TRACE_INFO == True:
        print_empty_line()
        print("Tracing Dependencies:")
        print_empty_line()

    dependencies: list[str] = remove_ignored_dependencies(
        trace_dependencies(used_functions, linked_functions)
    )

    if PRINT_DEPENDENCY_TRACE_INFO == True:
        print_empty_line()
        print("Used functions:")
        print_empty_line()

        for function in used_functions:
            print("  ", end="")
            print_function_name(function)

        print_empty_line()
        print("Used functions and their dependencies (ignored dependencies removed):")
        print_empty_line()

        for dependency in dependencies:
            print("  ", end="")
            print_function_name(dependency)

        print_empty_line()

    return dependencies


def update_test_info_json(absolute_test_directory_path: str) -> None:
    absolute_test_info_json_filepath: str = os.path.join(
        absolute_test_directory_path, TEST_INFO_JSON_FILENAME
    )
    contents: list[str] = []

    used_functions: list[dict[str, (str | list[str])]] = remove_ignored_dependencies(
        extract_functions_test_uses(
            os.path.join(
                absolute_test_directory_path,
                "obj",
                SOURCE_DIRECTORY_NAME,
                "main.cpp.src",
            )
        )
    )

    if PRINT_DEPENDENCY_TRACE_INFO == True:
        print_empty_line()
        print("Functions Test Uses (ignored dependencies removed):")
        print_empty_line()

        for function in used_functions:
            print("  ", end="")
            print_function_name(function)

    with open(absolute_test_info_json_filepath, "r") as file:
        contents = json.load(file)

    contents["used"] = [
        unmangle_cxx_function_name(function) for function in used_functions
    ]

    used_functions = trace_dependencies_for_test(
        absolute_test_directory_path, used_functions
    )

    contents["dependencies"] = []
    dependencies = []

    for function in used_functions:
        unmangled_function_name = unmangle_cxx_function_name(function)
        if unmangled_function_name not in contents["targets"]:
            contents["dependencies"].append(unmangled_function_name)
            dependencies.append(function)

    with open(absolute_test_info_json_filepath, "w") as file:
        json.dump(contents, file, indent=2)

    targeted_but_unused_functions: list[dict[str, str]] = [
        function for function in contents["targets"] if function not in contents["used"]
    ]

    if len(targeted_but_unused_functions) > 0:
        report_fatal_error_then_exit(
            "Test does not have all of the functions it claims to evaluate.",
            [
                "Update the test with code to evaluate the missing functions, or",
                "Remove the names of the missing functions from the list of functions the test claims to evaluate.",
            ],
        )

    return


def build_test(
    absolute_root_test_directory_path: str, absolute_test_directory_path: str
) -> None:

    test_identifier: str = get_test_identifier(
        absolute_root_test_directory_path, absolute_test_directory_path
    )
    test_header: str = ""

    if CLEAN_THEN_BUILD_TESTS:
        test_header = f"Cleaning and compiling '{test_identifier}'"
    else:
        test_header = f"Compiling '{test_identifier}'"

    print_empty_line()
    print(test_header)
    print_subdivider()

    if CLEAN_THEN_BUILD_TESTS:
        clean_old_build_files(
            absolute_test_directory_path, absolute_root_test_directory_path
        )

    build_test_in_debug_mode(
        absolute_test_directory_path, absolute_root_test_directory_path
    )
    print("Compilation successful.")

    return


def directory_holds_test(
    absolute_root_test_directory_path: str, absolute_current_directory_path: str
) -> bool:
    directory_contents: list[str] = os.listdir(absolute_current_directory_path)
    test_identifier: str = get_test_identifier(
        absolute_root_test_directory_path, absolute_current_directory_path
    )
    source_directory_found: bool = False
    test_info_json_found: bool = False
    autotest_json_found: bool = False
    warning_occurred: bool = False

    if TEST_SOURCE_DIRECTORY_NAME in directory_contents:
        source_directory_found = True

    if TEST_INFO_JSON_FILENAME in directory_contents:
        test_info_json_found = True

    if AUTOTEST_JSON_FILENAME in directory_contents:
        autotest_json_found = True

    if source_directory_found or test_info_json_found or autotest_json_found:
        if not source_directory_found:
            report_warning(
                f"'{test_identifier}' does not have a source directory.",
                ["Create a source directory and add source code to test."],
            )
            warning_occurred = True

        if not test_info_json_found:
            report_warning(
                f"'{test_identifier}' does not have a JSON file for test information.",
                ["Create the JSON file for test information in the test directory."],
            )
            warning_occurred = True

        if not autotest_json_found:
            report_warning(
                f"'{test_identifier}' does not have an autotest JSON file.",
                ["Add an autotest JSON file to the test directory."],
            )
            warning_occurred = True

        if warning_occurred:
            report_fatal_error_then_exit(
                "Invalid test directory structure initiated program abort."
            )
    else:
        return False

    return True


def build_tests_in_directory(
    absolute_root_test_directory_path: str,
    absolute_current_directory_path: Optional[str] = None,
) -> int:
    if absolute_current_directory_path is None:
        absolute_current_directory_path = absolute_root_test_directory_path

    directory_contents = os.scandir(absolute_current_directory_path)
    num_built_tests: int = 0

    # TODO: Randomly shuffle the directory_contents.

    for entry in directory_contents:
        if entry.is_file():
            continue

        absolute_subdirectory_path: str = os.path.join(
            absolute_current_directory_path, entry
        )

        if directory_holds_test(
            absolute_root_test_directory_path, absolute_subdirectory_path
        ):
            build_test(absolute_root_test_directory_path, absolute_subdirectory_path)
            update_test_info_json(absolute_subdirectory_path)
            print("Updated test information JSON file.")
            num_built_tests += 1
        else:
            num_built_tests += build_tests_in_directory(
                absolute_root_test_directory_path, absolute_subdirectory_path
            )

    return num_built_tests


class TestBatcher:
    _batches: list[list[dict[str, (str | list[str])]]] = []
    _unfulfilled_batch: list[dict[str, (str | list[str])]] = []

    def __init__(self):
        self._batch_tests_in_directory(ABSOLUTE_PATH_TO_ROOT_TEST_DIRECTORY)
        self._batch_tests_that_have_recursive_dependencies()
        return

    def _batch_test(self, test: dict[str, (str | list[str])], batch_num: int) -> None:
        if batch_num > len(self._batches):
            report_fatal_error_then_exit("Unusually high batch number")
        elif batch_num == len(self._batches):
            self._batches.append([test])
        else:
            self._batches[batch_num].append(test)

        return

    def _batch_test_as_unfulfilled(self, test: dict[str, (str | list[str])]) -> None:
        self._unfulfilled_batch.append(test)
        return

    def _evaluate_unfulfilled_batch(
        self,
        latest_test_added: dict[str, (str, list[str])],
        batch_number_of_added_test: int,
    ) -> None:
        unfulfilled_batch: list[dict[str, (str | list[str])]] = self._unfulfilled_batch.copy()

        for test in self._unfulfilled_batch:
            test["dependencies"] = list(
                set(test["dependencies"]) - set(latest_test_added["targets"])
            )

            if len(test["dependencies"]) == 0:
                self._batch_test(test, batch_number_of_added_test + 1)
                unfulfilled_batch.remove(test)
                return

        self._unfulfilled_batch = unfulfilled_batch
        return

    def _assign_test_to_batch(self, absolute_test_directory_path: str) -> None:
        contents: list[str] = []
        test_info_json: str = os.path.join(
            absolute_test_directory_path, TEST_INFO_JSON_FILENAME
        )

        with open(test_info_json, "r") as file:
            contents = json.load(file)

        test: dict[str, (str | list[str])] = {}
        test["path"] = absolute_test_directory_path
        test["targets"] = contents["targets"]
        test["dependencies"] = contents["dependencies"]
        batch_number: Optional[int] = None

        if len(test["dependencies"]) == 0:
            batch_number = 0
        else:
            for index, batch in enumerate(self._batches):
                for batch_test in batch:
                    test["dependencies"] = list(
                        set(test["dependencies"]) - set(batch_test["targets"])
                    )

                    if len(test["dependencies"]) == 0:
                        batch_number = index + 1
                        break

                if batch_number is not None:
                    break

        if batch_number is None:
            self._batch_test_as_unfulfilled(test)
        else:
            self._batch_test(test, batch_number)
            self._evaluate_unfulfilled_batch(test, batch_number)
        return

    def _batch_tests_in_directory(self, absolute_directory_path: str) -> None:
        directory_contents = os.scandir(absolute_directory_path)

        for entry in directory_contents:
            if entry.is_file():
                continue

            absolute_subdirectory_path: str = os.path.join(
                absolute_directory_path, entry
            )

            if directory_holds_test(
                ABSOLUTE_PATH_TO_ROOT_TEST_DIRECTORY, absolute_subdirectory_path
            ):
                self._assign_test_to_batch(absolute_subdirectory_path)
            else:
                self._batch_tests_in_directory(absolute_subdirectory_path)

        return

    def _batch_tests_that_have_recursive_dependencies(self) -> None:
        if len(self._unfulfilled_batch) == 0:
            return

        total_targets: list[str] = []

        for test in self._unfulfilled_batch:
            total_targets += test["targets"]

        for test in self._unfulfilled_batch:
            if len(set(test["dependencies"]) - set(total_targets)) > 0:
                total_targets = list(set(total_targets) - set(test["dependencies"]))

        unfulfilled_batch: list[dict[str, (str | list[str])]] = self._unfulfilled_batch.copy()
        final_batch_number: int = len(self._batches)

        for test in self._unfulfilled_batch:
            test_identifier: str = get_test_identifier(ABSOLUTE_PATH_TO_ROOT_TEST_DIRECTORY, test["path"])
            count: int = 1

            if len(set(test["dependencies"]) - set(total_targets)) == 0:
                self._batch_test(test, final_batch_number)
                unfulfilled_batch.remove(test)
            else:
                print_empty_line()
                print(
                    "Untested Dependencies For '"
                    + get_test_identifier(
                        ABSOLUTE_PATH_TO_ROOT_TEST_DIRECTORY, test["path"]
                    )
                    + "':"
                )

                for dependency in test["dependencies"]:
                    print(f"  {count}. " + dependency)
                    count += 1

        self._unfulfilled_batch = unfulfilled_batch

        if PRINT_BATCHES:
            print_empty_line()

            for index, batch in enumerate(self._batches):
                print(f"Batch {index + 1}:")
                for test in batch:
                    test_identifier: str = get_test_identifier(ABSOLUTE_PATH_TO_ROOT_TEST_DIRECTORY, test["path"])
                    print("  " + test_identifier)

                print_empty_line()

            print("Unfulfilled Batch:")

            for test in self._unfulfilled_batch:
                test_identifier: str = get_test_identifier(ABSOLUTE_PATH_TO_ROOT_TEST_DIRECTORY, test["path"])
                print("  " + test_identifier)

        if len(self._unfulfilled_batch) == 0:
            return

        report_fatal_error_then_exit(
            "Some tests have untested dependencies.",
            [
                "Review the list of tests above and add tests whose targets evaluate the dependency functions listed."
            ],
        )
        return

    def _add_rom_field_to_autotest_json_file(self, absolute_autotest_json_path) -> None:
        contents: list[str] = []

        with open(absolute_autotest_json_path) as file:
            contents = json.load(file)

        contents["rom"] = TESTING_ROM_ABSOLUTE_PATH

        with open(absolute_autotest_json_path, "w") as file:
            json.dump(contents, file, indent=2)

        return

    def _remove_rom_field_from_autotest_json_file(
        self, absolute_autotest_json_path
    ) -> None:
        contents: list[str] = []

        with open(absolute_autotest_json_path) as file:
            contents = json.load(file)

        try:
            contents.pop("rom")
        except KeyError:
            pass

        with open(absolute_autotest_json_path, "w") as file:
            json.dump(contents, file, indent=2)

        return

    def _execute_test(self, absolute_test_directory_path: str) -> None:
        test_identifier: str = get_test_identifier(
            ABSOLUTE_PATH_TO_ROOT_TEST_DIRECTORY, absolute_test_directory_path
        )
        print_empty_line()
        print(f"Executing '{test_identifier}':")
        print_subdivider()

        os.chdir(absolute_test_directory_path)
        absolute_autotest_json_path: str = os.path.join(
            absolute_test_directory_path, AUTOTEST_JSON_FILENAME
        )

        self._add_rom_field_to_autotest_json_file(absolute_autotest_json_path)

        try:
            subprocess.run(["cemu-autotester", "./autotest.json"], check=True)
        except subprocess.CalledProcessError as error:
            self._remove_rom_field_from_autotest_json_file(absolute_autotest_json_path)

            if ABORT_ON_FIRST_FAILED_TEST:
                report_fatal_error_then_exit(error.__str__())

        self._remove_rom_field_from_autotest_json_file(absolute_autotest_json_path)

        os.chdir(ABSOLUTE_PATH_TO_ROOT_TEST_DIRECTORY)
        return

    def run_tests(self) -> int:
        num_tests_executed: int = 0

        for batch in self._batches:

            # TODO: Randomly shuffle the tests in each batch.

            for test in batch:
                self._execute_test(test["path"])
                num_tests_executed += 1

        return num_tests_executed


def main():
    print_program_banner()
    print_section_header("Building Tests")

    num_built_tests: int = build_tests_in_directory(
        ABSOLUTE_PATH_TO_ROOT_TEST_DIRECTORY
    )
    print_empty_line()
    print_centered(f"{num_built_tests} tests built.")

    print_section_header("Executing Tests")

    batcher = TestBatcher()
    num_tests_executed: int = batcher.run_tests()

    print_empty_line()
    print_centered(f"{num_tests_executed} tests executed.")
    print_empty_line()
    print_divider()
    print_empty_line()
    print_centered("TESTING COMPLETE")
    print_empty_line()
    return


if __name__ == "__main__":
    assert TERMINAL_LINE_WIDTH > 40
    main()
