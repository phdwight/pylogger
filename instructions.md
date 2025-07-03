# Python Code Generation Instructions

## Python Version Requirements
- **Must use Python 3.12** or later
- Leverage Python 3.12 specific features when appropriate:
  - Generic type syntax (`list[str]` instead of `List[str]`)
  - `@override` decorator for method overriding
  - Improved error messages and debugging features
  - Performance improvements in comprehensions and generators

## Code Quality Standards

### Pythonic Code Requirements
- Use list/dict/set comprehensions instead of loops where appropriate
- Prefer `pathlib.Path` over `os.path` for file operations
- Use context managers (`with` statements) for resource management
- Implement `__str__` and `__repr__` methods for custom classes
- Use `dataclasses` or `pydantic` for data structures
- Prefer `enumerate()` over manual indexing
- Use `zip()` for parallel iteration
- Implement proper exception handling with specific exception types

### Modern Python Idioms (3.12+)
- Use type hints consistently with modern syntax:
  ```python
  def process_items(items: list[dict[str, Any]]) -> Iterator[str]:
      ...
  ```
- Use `match/case` statements for complex conditionals
- Leverage `walrus operator` (`:=`) for assignment expressions
- Use `f-strings` for string formatting
- Prefer `pathlib` for all file system operations
- Use `@dataclass` with `slots=True` for performance
- Implement `__slots__` in regular classes when appropriate

### Flake8 Compliance
- **Line length**: Maximum 88 characters (Black formatter standard)
- **Import organization**: Use `isort` compatible ordering
  - Standard library imports first
  - Third-party imports second  
  - Local application imports last
  - Separate groups with blank lines
- **Naming conventions**:
  - `snake_case` for functions, variables, and modules
  - `PascalCase` for classes
  - `UPPER_CASE` for constants
  - Prefix private members with single underscore `_`
- **Whitespace**: Follow PEP 8 guidelines strictly
- **Documentation**: Use docstrings for all public functions, classes, and modules

## SOLID Principles Implementation

### Single Responsibility Principle (SRP)
- Each class should have only one reason to change
- Functions should do one thing well
- Separate concerns into different modules/classes

### Open/Closed Principle (OCP)
- Use abstract base classes and protocols
- Implement dependency injection
- Prefer composition over inheritance
- Use strategy pattern for varying algorithms

### Liskov Substitution Principle (LSP)
- Derived classes must be substitutable for base classes
- Use `@override` decorator when overriding methods
- Maintain behavioral contracts in inheritance hierarchies

### Interface Segregation Principle (ISP)
- Use `typing.Protocol` for defining interfaces
- Create small, focused interfaces
- Don't force classes to depend on unused methods

### Dependency Inversion Principle (DIP)
- Depend on abstractions, not concretions
- Use dependency injection containers when appropriate
- Define interfaces for external dependencies

## Code Structure Guidelines

### Project Organization
```
project/
├── src/
│   └── package_name/
│       ├── __init__.py
│       ├── core/
│       ├── interfaces/
│       ├── services/
│       └── utils/
├── tests/
├── docs/
└── pyproject.toml
```

### Module Design
- Keep modules focused and cohesive
- Use `__all__` to explicitly define public APIs
- Implement proper logging with structured logging
- Use configuration classes instead of global variables

### Error Handling
- Create custom exception hierarchies
- Use specific exception types
- Implement proper error context and messages
- Log errors appropriately with structured data

### Testing Requirements
- Write unit tests using `pytest`
- Achieve minimum 80% code coverage
- Use `pytest` fixtures for test setup
- Implement property-based testing with `hypothesis` when applicable
- Mock external dependencies properly

### Documentation Standards
- Use Google-style docstrings
- Include type information in docstrings
- Provide examples in docstrings for complex functions
- Maintain README.md with usage examples

## Performance Considerations
- Use `__slots__` for classes with many instances
- Prefer generators over lists for large datasets
- Use `functools.lru_cache` for expensive computations
- Profile code when performance is critical
- Use `dataclasses` with `frozen=True` for immutable objects

## Security Guidelines
- Validate all input data
- Use `secrets` module for cryptographic randomness
- Sanitize file paths using `pathlib`
- Never use `eval()` or `exec()` with user input
- Use environment variables for sensitive configuration

## Example Code Template
```python
"""Module docstring describing purpose and usage."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol

logger = logging.getLogger(__name__)


class ServiceProtocol(Protocol):
    """Protocol defining service interface."""
    
    def process(self, data: dict[str, Any]) -> str:
        """Process data and return result."""
        ...


@dataclass(slots=True, frozen=True)
class DataModel:
    """Immutable data model with validation."""
    
    name: str
    value: int
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self) -> None:
        """Validate data after initialization."""
        if not self.name:
            raise ValueError("Name cannot be empty")
        if self.value < 0:
            raise ValueError("Value must be non-negative")


class ConcreteService:
    """Service implementation following SOLID principles."""
    
    def __init__(self, config_path: Path) -> None:
        self._config_path = config_path
        self._logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    def process(self, data: dict[str, Any]) -> str:
        """Process data according to business logic."""
        try:
            model = DataModel(**data)
            self._logger.info("Processing data", extra={"model": model})
            return f"Processed: {model.name}"
        except ValueError as e:
            self._logger.error("Invalid data", extra={"error": str(e), "data": data})
            raise
```

Follow these guidelines consistently to ensure high-quality, maintainable Python code.