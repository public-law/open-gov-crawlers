# Wisconsin Statutes Development Task

## 🧀 ORGANIZED HTML STATE
**Working Directory**: `/workspace/state-development/wisconsin-statutes`  
**Branch**: `feature/wisconsin-statutes`

## 🎯 Mission
Develop a complete working spider for the **Wisconsin Statutes** with organized HTML structure.

## 🎯 Deliverables

### 1. Parser Module: `public_law/legal_texts/parsers/usa/wisconsin_statutes.py`
- Implement `parse_statute_entries(response: HtmlResponse) -> tuple[StatuteEntry, ...]`
- Parse Wisconsin citation format: "Wis. Stat. § 939.05" (Chapter.Section)
- Create citations like "Wis. Stat. § 939.05"
- Handle Wisconsin's organized HTML structure
- Robust section extraction

### 2. Spider Module: `public_law/legal_texts/spiders/usa/wisconsin_statutes.py`
- Create new spider following template pattern
- Navigate Wisconsin Legislature website
- Handle chapter → section hierarchy
- Standard crawling settings (1s delays)

### 3. Parser Tests: `tests/legal_texts/parsers/usa/wisconsin_statutes_test.py`
- Test Wisconsin HTML parsing
- Test citation format parsing
- Test error handling
- Mock Wisconsin HTML samples

### 4. Spider Tests: `tests/legal_texts/spiders/usa/wisconsin_statutes_test.py`
- Test spider configuration and metadata
- Test navigation workflow
- Mock response testing

## 🌐 State Information
- **Spider Name**: `usa_wisconsin_statutes`
- **Start URL**: `https://docs.legis.wisconsin.gov/statutes`
- **Official Name**: Wisconsin Statutes
- **Citation Format**: Wis. Stat. § [Chapter].[Section]
- **Section Format**: "939.05" (Chapter.Section)
- **Coverage**: "Wisconsin, USA"

## 🏗️ Architecture References
- **Base Classes**: `public_law/legal_texts/spiders/_base/statute_base.py`
- **Data Models**: `public_law/legal_texts/models/statute.py`
- **Florida Example**: Complete working reference
- **Georgia Template**: Complex site handling patterns

## ⚠️ Special Considerations

### Wisconsin Legislature Website
- Well-organized HTML structure
- Clear chapter/section hierarchy
- Consistent formatting patterns
- Government website standards

### Technical Requirements
- Standard HTML parsing strategies
- Handle Wisconsin's chapter-based organization
- Efficient chapter/section navigation
- Wisconsin-specific citation formatting

## 🧪 Testing Workflow

```bash
# Navigate to Wisconsin worktree
cd /workspace/state-development/wisconsin-statutes

# Run parser tests
poetry run pytest tests/legal_texts/parsers/usa/wisconsin_statutes_test.py -v

# Run spider tests  
poetry run pytest tests/legal_texts/spiders/usa/wisconsin_statutes_test.py -v

# Test spider with limited pages
poetry run scrapy crawl usa_wisconsin_statutes -s CLOSESPIDER_PAGECOUNT=5

# Check spider listing
poetry run scrapy list | grep wisconsin

# Test with output
poetry run scrapy crawl --output tmp/wisconsin_test.json usa_wisconsin_statutes -s CLOSESPIDER_PAGECOUNT=10
```

## ✅ Success Criteria

1. **All tests pass** with >80% coverage
2. **Spider can extract Wisconsin statute entries** efficiently
3. **Parser handles organized HTML** reliably
4. **Chapter/section navigation** works smoothly
5. **Ready for production deployment**

## 🎨 Implementation Strategy

### Phase 1: Research (Day 1)
1. Examine Wisconsin Legislature website structure
2. Identify HTML patterns and navigation
3. Understand chapter/section organization
4. Create HTML fixtures for testing

### Phase 2: Parser Development (Day 2)
1. Implement `parse_statute_entries()`
2. Handle Wisconsin citation parsing
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

Wisconsin's organized HTML structure should provide reliable patterns and straightforward development.

**Leverage Wisconsin's organized approach to statute publication!** 🧀