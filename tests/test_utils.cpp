#include <ti/getcsc.h>
#include <ti/screen.h>

#include "test_utils.h"


void testutil_PrintTestSetup()
{
  os_ClrHomeFull();
  os_PutStrLine("Testing...");
  while (!os_GetCSC());
  return;
}


void testutil_PrintTestResults(bool result)
{
  os_ClrHomeFull();

  if (result)
  {
    os_PutStrLine("Test passed.");
  }
  else
  {
    os_PutStrLine("Test failed.");
  }

  while (!os_GetCSC());
  return;
}
