# Washington RCW Development Task

## 🌲 CLEAN FORMAT STATE
**Working Directory**: `/workspace/state-development/washington-statutes`  
**Branch**: `feature/washington-statutes`

## 🎯 Mission
Develop a complete working spider for the **Revised Code of Washington (RCW)** with clean formatting.

## 🎯 Deliverables

### 1. Parser Module: `public_law/legal_texts/parsers/usa/washington_statutes.py`
- Implement `parse_statute_entries(response: HtmlResponse) -> tuple[StatuteEntry, ...]`
- Parse Washington citation format: "RCW 9.41.010" (Title.Chapter.Section)
- Create citations like "RCW 9.41.010"
- Handle Washington's clean HTML format
- Robust section extraction

### 2. Spider Module: `public_law/legal_texts/spiders/usa/washington_statutes.py`
- Create new spider following template pattern
- Navigate Washington State Legislature website
- Handle title → chapter → section hierarchy
- Standard crawling settings (1s delays)

### 3. Parser Tests: `tests/legal_texts/parsers/usa/washington_statutes_test.py`
- Test Washington HTML parsing
- Test RCW citation format parsing
- Test error handling
- Mock Washington HTML samples

### 4. Spider Tests: `tests/legal_texts/spiders/usa/washington_statutes_test.py`
- Test spider configuration and metadata
- Test navigation workflow
- Mock response testing

## 🌐 State Information
- **Spider Name**: `usa_washington_statutes`
- **Start URL**: `https://app.leg.wa.gov/RCW/`
- **Official Name**: Revised Code of Washington
- **Citation Format**: RCW [Title].[Chapter].[Section]
- **Section Format**: "9.41.010" (Title.Chapter.Section)
- **Coverage**: "Washington, USA"

## 🏗️ Architecture References
- **Base Classes**: `public_law/legal_texts/spiders/_base/statute_base.py`
- **Data Models**: `public_law/legal_texts/models/statute.py`
- **Florida Example**: Complete working reference
- **Georgia Template**: Complex site handling patterns

## ⚠️ Special Considerations

### Washington Legislature Website
- Clean, professional format
- Well-organized RCW structure
- Consistent HTML patterns
- Modern government web design

### Technical Requirements
- Standard HTML parsing strategies
- Handle RCW-specific citation format
- Efficient title/chapter navigation
- Washington-specific formatting

## 🧪 Testing Workflow

```bash
# Navigate to Washington worktree
cd /workspace/state-development/washington-statutes

# Run parser tests
poetry run pytest tests/legal_texts/parsers/usa/washington_statutes_test.py -v

# Run spider tests  
poetry run pytest tests/legal_texts/spiders/usa/washington_statutes_test.py -v

# Test spider with limited pages
poetry run scrapy crawl usa_washington_statutes -s CLOSESPIDER_PAGECOUNT=5

# Check spider listing
poetry run scrapy list | grep washington

# Test with output
poetry run scrapy crawl --output tmp/washington_test.json usa_washington_statutes -s CLOSESPIDER_PAGECOUNT=10
```

## ✅ Success Criteria

1. **All tests pass** with >80% coverage
2. **Spider can extract Washington RCW entries** efficiently
3. **Parser handles clean HTML format** reliably
4. **RCW citation format** handled correctly
5. **Ready for production deployment**

## 🎨 Implementation Strategy

### Phase 1: Research (Day 1)
1. Examine Washington Legislature website structure
2. Identify HTML patterns and navigation
3. Understand RCW organization
4. Create HTML fixtures for testing

### Phase 2: Parser Development (Day 2)
1. Implement `parse_statute_entries()`
2. Handle RCW citation parsing
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

Washington's clean format and professional website should provide excellent development experience.

**Leverage Washington's clean RCW format and organization!** 🌲