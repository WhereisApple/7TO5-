
# 7TO5

**7TO5** is a programming language I'm building from scratch to understand how programming languages actually work internally.

This project started as a way for me to learn about **lexing, parsing, syntax, and program execution** by actually implementing them instead of just studying the theory.

> **7TO5 is currently a work in progress.**

## Current Features

At the moment, 7TO5 supports some basic programming functionality, including:

* Variables
* Basic data types
* Arithmetic operations
* Basic input/output
* Conditional statements
* Loops
* Basic expressions
* Custom syntax
* Lexical analysis
* Parsing
* Basic program execution

The language is still fairly small, but I'm gradually expanding it as I learn more.

## How It Works

The current implementation roughly follows this process:

```text
7TO5 Source Code
       ↓
     Lexer
       ↓
    Tokens
       ↓
     Parser
       ↓
   Program Structure
       ↓
    Execution
```

I'm implementing these parts myself so I can understand what happens between writing code and actually executing it.

## Example

A simple 7TO5 program can look like:

```text
let num A be 10
let num B be 5
let num result be add A and B
print result

if result eq 15 then {
  print "result is 15"
} else {
  print "result is not 15"
} end
```

The syntax is still experimental, so some parts of the language may change as development continues.

## What I Want to Add

There is still a lot I want to build into 7TO5.

Some of the features I plan to add include:

* Arrays
* Strings and improved string operations
* Functions
* Better type handling
* More operators
* More control-flow features
* Error handling
* A better parser
* Improved runtime
* More built-in functions
* Modules/imports
* A proper standard library

Eventually, I'd like 7TO5 to become a much more complete programming language rather than just a small interpreter.

## Why I Built It

I'm building 7TO5 mainly as a learning project.

Instead of using an existing parser or language framework, I want to understand the fundamentals by building the pieces myself.

Through this project I'm learning about:

* Lexers
* Tokens
* Parsers
* Grammars
* Abstract syntax
* Interpreters
* Runtime execution
* Programming language design

## Current Status

🚧 **Under Development**

7TO5 currently supports basic language functionality, but it is nowhere near finished.

I'm treating this as an ongoing project and adding features as I learn more about language design and implementation.

## Future Goal

My goal is to eventually have a small but usable programming language that I can run programs in, with its own syntax, data structures, functions, standard library, and execution system.

For now, I'm focusing on getting the fundamentals right and building it one feature at a time.

---

**Built from scratch by me as a learning project.**

## Notes
The About Developer page contains a placeholder portfolio link that you can replace with your own profile URL.
