#include "../../../../src/recursion.h"
#include "../../../test_utils.h"


static bool test(void);


int main(void)
{
  testutil_PrintTestSetup();
  testutil_PrintTestResults(test());
  return 0;
}


static bool test(void)
{
  char string[7] = "string";
  
  bar_calls_foo_and_bar_and_cat(string);
  return true;
}
