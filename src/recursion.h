#ifndef RECURSION_H
#define RECURSION_H


int dependency_of_foo(char* string);
unsigned int dependency_of_bar(char* string);
int dependency_of_cat(char* string);

unsigned int foo_calls_foo_and_bar_and_cat(char* string);
unsigned int bar_calls_foo_and_bar_and_cat(char* string);
unsigned int cat_calls_foo_and_bar_and_cat(char* string);

unsigned int triple_recursion_test();


#endif
