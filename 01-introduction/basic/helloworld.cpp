#include <format>
#include <iostream>
#include <print>
#include <sstream>

// using namespace std; Q: 为什么不用

// Hello World 的四种写法
int main() {
  std::cout << "Hello, World!" << std::endl;

  std::cout << std::format("Hello, {}!", "World") << std::endl;

  std::print("Hello, {}!\n", "World");

  std::ostringstream oss;
  oss << "Hello, World!" << std::endl;
  std::cout << oss.str();

  return 0;
}