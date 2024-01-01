### Test Template

This directory contains all of the files necessary to create a new test.
Clone this directory and put your new test in the cloned directory.
You can create subdirectories within `tests/` to group related tests together.

Put your test in the `static bool test(void)` function in `src/main.cpp`.
Do not add any source files to `src` other than the existing `main.cpp`.
The testing framework will not know what to do with them.

Make sure you modify the `EXTRA_CPPSOURCES` variable in the `makefile` each
time you include a header file in your test's `main.cpp` file.

After you have written your test, run the testing script. It will complain that
your test does not have the functions it uses. Look in `test_info.json` and copy
the signatures of the function(s) you want to test from the `"used"` list to the
`"targets"` list.

Note: Even though the function signatures in the `test_info.json` will look
similar to the ones in your codebase, do not put the function signatures from
your codebase into the `test_info.json`. They will not match the ones that the
testing script will pull from the test's object files. Only function signatures
from the `"used"` list will work in the `"targets"` list.

To test graphics routines, you will need to change the `autotest.json`.
