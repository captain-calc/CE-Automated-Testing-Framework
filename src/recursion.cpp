#include <string.h>

#include "recursion.h"


static unsigned int static_function(char* string)
{
  return strspn(string, "ing");
}


int dependency_of_foo(char* string)
{
  return static_function(string) + strncmp(string, string, strlen(string));
}


unsigned int dependency_of_bar(char* string)
{
  return static_function(string) + strlen(strcat(string, string));
}


int dependency_of_cat(char* string)
{
  return static_function(string) + strcmp(string, string);
}


unsigned int foo_calls_foo_and_bar_and_cat(char* string)
{
  dependency_of_foo(string);
  bar_calls_foo_and_bar_and_cat(string);
  cat_calls_foo_and_bar_and_cat(string);
  foo_calls_foo_and_bar_and_cat(string);
  return 0;
}


unsigned int bar_calls_foo_and_bar_and_cat(char* string)
{
  dependency_of_bar(string);
  cat_calls_foo_and_bar_and_cat(string);
  foo_calls_foo_and_bar_and_cat(string);
  bar_calls_foo_and_bar_and_cat(string);
  return 0;
}


unsigned int cat_calls_foo_and_bar_and_cat(char* string)
{
  dependency_of_cat(string);
  foo_calls_foo_and_bar_and_cat(string);
  bar_calls_foo_and_bar_and_cat(string);
  cat_calls_foo_and_bar_and_cat(string);
  return 0;
}


unsigned int triple_recursion_test(void)
{
  char string[7] = "string";

  if (static_function(string))
      return foo_calls_foo_and_bar_and_cat(string);

  return 0;
}
