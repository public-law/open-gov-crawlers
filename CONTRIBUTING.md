# Contributing to Open-Gov Crawlers

Thank you for your interest in contributing to our project! This document provides guidelines and instructions to help you get started.

## Skill Level

We welcome contributors with **intermediate to advanced Python skills**. Familiarity with the following is a plus:

- Type annotations and strict typing
- Functional programming patterns
- Web scraping (Scrapy)
- Testing with pytest

If you're newer to these concepts, we encourage you to start with documentation or test contributions and grow from there!

## Development Environment Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/public-law/open-gov-crawlers.git
   cd open-gov-crawlers
   ```

2. **Install dependencies using Poetry:**
   ```bash
   poetry install
   ```

3. **Activate the virtual environment:**
   ```bash
   poetry shell
   ```

4. **Run tests:**
   ```bash
   pytest
   ```

## Code Style and Best Practices

- **Type Annotations:** Use type hints consistently. We use `pyright` in strict mode.
- **Functional Style:** Prefer functional programming patterns (e.g., `pipe`, comprehensions, pure functions) over imperative loops.
- **Testing:** Write tests for new features or bug fixes. Use pytest and follow the existing test structure.
- **Documentation:** Update the README or add docstrings as needed.

## Pull Request Process

1. Fork the repository and create a new branch for your feature or fix.
2. Make your changes, ensuring tests pass and code style is maintained.
3. Submit a pull request with a clear description of your changes.

## Issue Labels

- **good first issue:** Suitable for newcomers.
- **advanced:** Requires deeper knowledge of the codebase or Python's type system.

## Questions or Help?

Feel free to open an issue or contact the maintainers for guidance.

Happy coding! 
