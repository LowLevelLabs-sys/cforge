
# cforge

Create clean C projects in seconds.

`cforge` is a CLI tool for generating a clean, ready-to-use C project structure without manually creating the initial folders and configuration files.

## Features

* Generate a clean C project structure
* Basic C project template
* GCC and Clang support
* Makefile-based build system
* Ready-to-use project directories

## Usage

Create a new C project:

```bash
cforge hello
```

This generates:

```text
hello/
├── src/
│   └── main.c
├── include/
├── tests/
├── build/
├── Makefile
├── .gitignore
└── README.md
```

Then enter the project and build it:

```bash
cd hello
make
```

Run the program:

```bash
./build/hello
```

## Development

Clone the repository and install the project dependencies:

```bash
uv sync
```

Run cforge locally:

```bash
uv run cforge hello
```

## License

MIT
