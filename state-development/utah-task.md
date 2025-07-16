# Utah Code Development Task

## 🏔️ MODERN WEBSITE STATE
**Working Directory**: `/workspace/state-development/utah-statutes`  
**Branch**: `feature/utah-statutes`

## 🎯 Mission
Develop a complete working spider for the **Utah Code** with modern website architecture.

## 🎯 Deliverables

### 1. Parser Module: `public_law/legal_texts/parsers/usa/utah_statutes.py`
- Implement `parse_statute_entries(response: HtmlResponse) -> tuple[StatuteEntry, ...]`
- Parse Utah citation format: "76-5-103" (Title-Chapter-Section)
- Create citations like "Utah Code Ann. § 76-5-103"
- Handle modern website HTML structure
- Robust section extraction

### 2. Spider Module: `public_law/legal_texts/spiders/usa/utah_statutes.py`
- Create new spider following template pattern
- Navigate Utah Legislature's website
- Handle title → chapter → section hierarchy
- Standard crawling settings (1s delays)

### 3. Parser Tests: `tests/legal_texts/parsers/usa/utah_statutes_test.py`
- Test Utah HTML parsing
- Test citation format parsing
- Test error handling
- Mock Utah HTML samples

### 4. Spider Tests: `tests/legal_texts/spiders/usa/utah_statutes_test.py`
- Test spider configuration and metadata
- Test navigation workflow
- Mock response testing

## 🌐 State Information
- **Spider Name**: `usa_utah_statutes`
- **Start URL**: `https://le.utah.gov/xcode/code.html`
- **Official Name**: Utah Code
- **Citation Format**: Utah Code Ann. § [Title]-[Chapter]-[Section]
- **Section Format**: "76-5-103" (Title-Chapter-Section)
- **Coverage**: "Utah, USA"

## 🏗️ Architecture References
- **Base Classes**: `public_law/legal_texts/spiders/_base/statute_base.py`
- **Data Models**: `public_law/legal_texts/models/statute.py`
- **Florida Example**: Complete working reference
- **Georgia Template**: LexisNexis handling patterns

## ⚠️ Special Considerations

### Utah Legislature Website
- Modern, responsive design
- Possible JavaScript components
- Clean government website
- Well-organized navigation

### Technical Requirements
- Modern HTML parsing strategies
- Handle potential dynamic content
- Efficient title/chapter navigation
- Utah-specific citation formatting

## 🧪 Testing Workflow

```bash
# Navigate to Utah worktree
cd /workspace/state-development/utah-statutes

# Run parser tests
poetry run pytest tests/legal_texts/parsers/usa/utah_statutes_test.py -v

# Run spider tests  
poetry run pytest tests/legal_texts/spiders/usa/utah_statutes_test.py -v

# Test spider with limited pages
poetry run scrapy crawl usa_utah_statutes -s CLOSESPIDER_PAGECOUNT=5

# Check spider listing
poetry run scrapy list | grep utah

# Test with output
poetry run scrapy crawl --output tmp/utah_test.json usa_utah_statutes -s CLOSESPIDER_PAGECOUNT=10
```

## ✅ Success Criteria

1. **All tests pass** with >80% coverage
2. **Spider can extract Utah statute entries** efficiently
3. **Parser handles modern HTML structure** reliably
4. **Handles any JavaScript components** gracefully
5. **Ready for production deployment**

## 🎨 Implementation Strategy

### Phase 1: Research (Day 1)
1. Examine Utah Legislature website structure
2. Identify HTML patterns and navigation
3. Document any JavaScript requirements
4. Create HTML fixtures for testing

### Phase 2: Parser Development (Day 2)
1. Implement `parse_statute_entries()`
2. Handle Utah citation parsing
3. Create comprehensive parser tests
4. Test with real HTML samples

### Phase 3: Spider Development (Day 3)
1. Create spider following template
2. Test navigation and crawling
3. Verify metadata generation
4. Create spider tests

### Phase 4: Testing & Polish (Day 4)
1. Full integration testing
2. Performance optimization
3. Error handling improvements
4. Documentation completion

## 🏁 Ready to Start!

Utah's modern website should provide clean HTML and good navigation patterns.

**Build on Florida's success with modern web architecture!** 🏔️