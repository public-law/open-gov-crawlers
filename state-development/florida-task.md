# Florida Statutes Development Task

## 🌴 PRIORITY STATE
**Working Directory**: `/workspace/state-development/florida-statutes`  
**Branch**: `feature/florida-statutes`

## 🎯 Mission
Develop a complete working spider for the **Florida Statutes** with clean HTML structure for rapid development.

## 🎯 Deliverables

### 1. Parser Module: `public_law/legal_texts/parsers/usa/florida_statutes.py`
- ✅ **Template exists** - enhance as needed
- Parse Florida citation format: "768.28" (Chapter.Section)
- Create citations like "Fla. Stat. § 768.28"
- Handle Florida's clean HTML structure
- Robust section extraction from chapters

### 2. Spider Module: `public_law/legal_texts/spiders/usa/florida_statutes.py`
- ✅ **Complete example exists** - test and refine
- Navigate Florida Legislature's website
- Handle title → chapter → section hierarchy
- Standard crawling settings (1s delays)

### 3. Parser Tests: `tests/legal_texts/parsers/usa/florida_statutes_test.py`
- ✅ **Template exists** - complete implementation
- Test Florida HTML parsing
- Test citation format parsing
- Test multiple sections extraction

### 4. Spider Tests: `tests/legal_texts/spiders/usa/florida_statutes_test.py`
- ✅ **Template exists** - complete implementation
- Test spider configuration
- Test metadata generation
- Test navigation workflow

## 🌐 State Information
- **Spider Name**: `usa_florida_statutes`
- **Start URL**: `http://www.leg.state.fl.us/Statutes/index.cfm?Tab=statutes&submenu=1`
- **Official Name**: Florida Statutes
- **Citation Format**: Fla. Stat. § [Chapter].[Section]
- **Section Format**: "768.28" (Chapter.Section)
- **Coverage**: "Florida, USA"

## 🏗️ Architecture References
- **Complete Working Example**: All files exist as templates
- **Florida Parser**: `public_law/legal_texts/parsers/usa/florida_statutes.py`
- **Florida Spider**: `public_law/legal_texts/spiders/usa/florida_statutes.py`
- **Test Templates**: Both spider and parser test files exist

## ⚠️ Special Considerations

### Florida Legislature Website
- Clean, well-structured HTML
- Standard government website format
- Predictable navigation patterns
- Good for establishing development pattern

### Technical Requirements
- Simple HTML parsing strategies
- Standard error handling
- Efficient chapter/section navigation
- Clean citation formatting

## 🧪 Testing Workflow

```bash
# Navigate to Florida worktree
cd /workspace/state-development/florida-statutes

# Run parser tests
poetry run pytest tests/legal_texts/parsers/usa/florida_statutes_test.py -v

# Run spider tests  
poetry run pytest tests/legal_texts/spiders/usa/florida_statutes_test.py -v

# Test spider with limited pages
poetry run scrapy crawl usa_florida_statutes -s CLOSESPIDER_PAGECOUNT=5

# Check spider listing
poetry run scrapy list | grep florida

# Test with output
poetry run scrapy crawl --output tmp/florida_test.json usa_florida_statutes -s CLOSESPIDER_PAGECOUNT=10
```

## ✅ Success Criteria

1. **All tests pass** with >80% coverage
2. **Spider can extract Florida statute entries** efficiently
3. **Parser handles clean HTML structure** reliably  
4. **Standard crawling patterns** work smoothly
5. **Ready for production deployment**
6. **Serves as template** for other clean HTML states

## 🎨 Implementation Strategy

### Phase 1: Test Existing Code (Day 1)
1. Run existing Florida spider and parser
2. Identify any bugs or missing features
3. Complete test implementations
4. Fix any issues found

### Phase 2: Enhancement (Day 2)
1. Optimize parser performance
2. Add error handling improvements
3. Complete test coverage
4. Documentation updates

### Phase 3: Production Ready (Day 3)
1. Full integration testing
2. Performance optimization
3. Final testing and validation
4. Ready for merge

## 🏁 Advantage: Head Start!

Florida has complete working examples already implemented. Your job is to test, refine, and make production-ready.

**Perfect state to validate the architecture and establish the development pattern!** 🌴