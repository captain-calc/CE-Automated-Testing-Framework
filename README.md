# CE Automated Testing Framework

The CE Automated Testing Framework is a Python script and a few files that can be added to a TI-84 Plus CE C++ project that uses the CE-Programming toolchain.

It only supports C++ projects at present, but support for C projects should be easy to add.

If you want to try it out, clone this repository and treat it like a CE-Programming SDK template.

## Project Structure

The CE Automated Testing Framework uses the same directory structure as the CE-Programming SDK template. All of the tests for the program go into a directory called `tests/` that sits next to the program's `src/` directory.

The `tests/` directory can have subdirectories for groups of related tests, as shown below.

```
calculator_project/
  runtests.py
  bin/
  obj/
  src/
  tests/
    ignored_dependencies.json
    group_of_related_tests/
      test_1/
        bin/
        obj/
        src/
        autotest.json
        makefile
        test_info.json
      test_2/
        ...

    test_1/
      bin/
      obj/
      src/
      autotest.json
      makefile
      test_info.json
    test_2/
      ...
```

## How It Works

Each test contains a `test_info.json` that looks like this:

```
{
  "targets": [
    "triple_recursion_test()"
  ],
  "used": [
    "triple_recursion_test()"
  ],
  "dependencies": [
    "dependency_of_bar(char*)",
    "bar_calls_foo_and_bar_and_cat(char*)",
    "dependency_of_foo(char*)",
    "cat_calls_foo_and_bar_and_cat(char*)",
    "foo_calls_foo_and_bar_and_cat(char*)",
    "dependency_of_cat(char*)"
  ]
}
```

When a programmer creates a new test, they will put the signature of each function the test evaluates into the `"targets"` list. When the Python script builds the test, it will determine what functions the test calls and put them into the `"used"` list.

The script classifies any functions that are in the `"used"` list but not in the `"targets"` list as "dependencies". These functions, and any functions that they call, go into the `"dependencies"` list.

If the programmer wants any of the dependencies ignored, they can add the dependency's function signature to the `ignored_dependencies.json`.

Once all of the tests are built, the script determines in what order the tests should be run. In the above example, all of the tests that target the functions in the `"dependencies"` list should be run first. Using this logic, the script sorts each test into its appropriate "batch," or group, and then executes each batch in order. The script uses the `cemu-autotester` to run each test.

The Python script requires that every dependency be targeted by at least one test; otherwise, it will abort. This limitation is intended to encourage rigorous test coverage.

## Platform Requirements

This program has only been tested on Fedora Linux. Compatibility with Windows and macOS is untested.

**Required Programs:**

* Python 3.11+
* CE-Programming SDK v11+ with `cemu-autotester`
* `c++filt`, a C++ function name unmangler

## Limitations

* There is no support to test `static` functions.
* No support for C-based projects.