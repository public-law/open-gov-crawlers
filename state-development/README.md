# State Statute Development Worktrees

This directory contains git worktrees for parallel development of Phase 1 state statute spiders.

## 🏆 Phase 1 States (Priority Order)

1. **Georgia** (HIGHEST PRIORITY) - Following Georgia v. Public.Resource.Org Supreme Court victory
2. **Florida** - Clean HTML structure
3. **Utah** - Modern website
4. **Virginia** - Well-structured
5. **Washington** - Clean format  
6. **Wisconsin** - Organized HTML

## 📁 Directory Structure

```
state-development/
├── georgia-statutes/     (feature/georgia-statutes branch)
├── florida-statutes/     (feature/florida-statutes branch)
├── utah-statutes/        (feature/utah-statutes branch)
├── virginia-statutes/    (feature/virginia-statutes branch)
├── washington-statutes/  (feature/washington-statutes branch)
└── wisconsin-statutes/   (feature/wisconsin-statutes branch)
```

## 🔄 Git Worktree Commands

### List all worktrees
```bash
git worktree list
```

### Switch to a state's development directory
```bash
cd state-development/georgia-statutes    # Highest priority
cd state-development/florida-statutes
# etc.
```

### Check current branch in a worktree
```bash
cd state-development/georgia-statutes
git branch --show-current
```

### Remove a worktree (if needed)
```bash
git worktree remove state-development/georgia-statutes
git branch -d feature/georgia-statutes  # Delete the branch too
```

## 🛠️ Development Workflow

### For each state, implement:

1. **Spider** (`public_law/legal_texts/spiders/usa/{state}_statutes.py`)
2. **Parser** (`public_law/legal_texts/parsers/usa/{state}_statutes.py`)
3. **Tests** (`tests/legal_texts/spiders/usa/{state}_statutes_test.py`)
4. **Parser Tests** (`tests/legal_texts/parsers/usa/{state}_statutes_test.py`)

### Template files are already created in main workspace:
- `public_law/legal_texts/models/statute.py` (data models)
- `public_law/legal_texts/spiders/_base/statute_base.py` (base classes)
- `public_law/legal_texts/spiders/usa/florida_statutes.py` (Florida example)
- `public_law/legal_texts/spiders/usa/georgia_statutes.py` (Georgia example)
- `public_law/legal_texts/parsers/usa/florida_statutes.py` (Florida parser)
- Test files for both examples

### Testing workflow:
```bash
# From within a state's worktree directory
cd state-development/georgia-statutes

# Run parser tests
poetry run pytest tests/legal_texts/parsers/usa/georgia_statutes_test.py

# Run spider tests  
poetry run pytest tests/legal_texts/spiders/usa/georgia_statutes_test.py

# Test spider with limited pages
poetry run scrapy crawl usa_georgia_statutes -s CLOSESPIDER_PAGECOUNT=5

# Run full spider (be careful with this!)
poetry run scrapy crawl --output tmp/georgia_statutes.json usa_georgia_statutes
```

## 🎯 Implementation Priority

**Start with Georgia** to honor the Supreme Court victory and establish the pattern for other states.

Each state worktree is independent and can be developed in parallel by different team members.

## 🔗 Merging Back

When a state implementation is complete:

1. Ensure all tests pass
2. Create a pull request from the feature branch
3. After review and merge, the worktree can be removed
4. The implementation will be available in the main branch

## 📚 Reference

- Main plan: `../US_State_Statute_Crawling_Plan.md`
- Architecture guide: See existing glossary spiders for patterns
- Florida example: Complete working implementation provided