# Virginia Code Development Task

## 🏛️ WELL-STRUCTURED STATE
**Working Directory**: `/workspace/state-development/virginia-statutes`  
**Branch**: `feature/virginia-statutes`

## 🎯 Mission
Develop a complete working spider for the **Code of Virginia** with well-structured government website.

## 🎯 Deliverables

### 1. Parser Module: `public_law/legal_texts/parsers/usa/virginia_statutes.py`
- Implement `parse_statute_entries(response: HtmlResponse) -> tuple[StatuteEntry, ...]`
- Parse Virginia citation format: "§ 18.2-1" (Title.Chapter-Section)
- Create citations like "Va. Code Ann. § 18.2-1"
- Handle Virginia's structured HTML
- Robust section extraction

### 2. Spider Module: `public_law/legal_texts/spiders/usa/virginia_statutes.py`
- Create new spider following template pattern
- Navigate Virginia Legislative Information System
- Handle title → chapter → section hierarchy
- Standard crawling settings (1s delays)

### 3. Parser Tests: `tests/legal_texts/parsers/usa/virginia_statutes_test.py`
- Test Virginia HTML parsing
- Test citation format parsing
- Test error handling
- Mock Virginia HTML samples

### 4. Spider Tests: `tests/legal_texts/spiders/usa/virginia_statutes_test.py`
- Test spider configuration and metadata
- Test navigation workflow
- Mock response testing

## 🌐 State Information
- **Spider Name**: `usa_virginia_statutes`
- **Start URL**: `https://law.lis.virginia.gov/vacode/`
- **Official Name**: Code of Virginia
- **Citation Format**: Va. Code Ann. § [Title].[Chapter]-[Section]
- **Section Format**: "18.2-1" (Title.Chapter-Section)
- **Coverage**: "Virginia, USA"

## 🏗️ Architecture References
- **Base Classes**: `public_law/legal_texts/spiders/_base/statute_base.py`
- **Data Models**: `public_law/legal_texts/models/statute.py`
- **Florida Example**: Complete working reference
- **Georgia Template**: Complex site handling patterns

## ⚠️ Special Considerations

### Virginia Legislative Information System
- Well-structured government portal
- Established HTML patterns
- Clear navigation hierarchy
- Professional layout and organization

### Technical Requirements
- Standard HTML parsing strategies
- Handle Virginia's title/chapter structure
- Efficient navigation patterns
- Virginia-specific citation formatting

## 🧪 Testing Workflow

```bash
# Navigate to Virginia worktree
cd /workspace/state-development/virginia-statutes

# Run parser tests
poetry run pytest tests/legal_texts/parsers/usa/virginia_statutes_test.py -v

# Run spider tests  
poetry run pytest tests/legal_texts/spiders/usa/virginia_statutes_test.py -v

# Test spider with limited pages
poetry run scrapy crawl usa_virginia_statutes -s CLOSESPIDER_PAGECOUNT=5

# Check spider listing
poetry run scrapy list | grep virginia

# Test with output
poetry run scrapy crawl --output tmp/virginia_test.json usa_virginia_statutes -s CLOSESPIDER_PAGECOUNT=10
```

## ✅ Success Criteria

1. **All tests pass** with >80% coverage
2. **Spider can extract Virginia statute entries** efficiently
3. **Parser handles structured HTML** reliably
4. **Navigation works smoothly** through titles/chapters
5. **Ready for production deployment**

## 🎨 Implementation Strategy

### Phase 1: Research (Day 1)
1. Examine Virginia LIS website structure
2. Identify HTML patterns and navigation
3. Understand title/chapter organization
4. Create HTML fixtures for testing

### Phase 2: Parser Development (Day 2)
1. Implement `parse_statute_entries()`
2. Handle Virginia citation parsing
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

Virginia's well-structured government website should provide reliable patterns and clean HTML.

**Leverage Virginia's professional government web design!** 🏛️