# TDD Migration: Glossary Architecture Refactor

**Goal**: Move metadata configuration from parsers to spiders, making parsers pure data extraction functions.

**Env notes**:
- This is a poetry project.
- pytest must be prefixed with `poetry run` to run the correct pytest.
- pyright must be prefixed with `poetry run` to run the correct pyright.
- Some strings have apostrophes in them. NEVER change them.

## 🔧 **Phase 0: Infrastructure Setup**
- [x] Create _new_ enhanced AutoGlossarySpider-like base class with `parse_glossary()` and abstract `get_metadata()`. The new class allows graceful migration of existing spiders.
- [x] Update existing tests to verify they still pass with current architecture, if needed.

## 📋 **Per-Glossary Migration (TDD Order)**

### **1. USA Courts Glossary** (simplest - already uses metadata utils)
- [x] **Test**: Update `tests/glossaries/parsers/usa/courts_glossary_test.py` to test `parse_entries()` function only
- [x] **Test**: Create spider test for `get_metadata()` method  
- [x] **Test**: Create integration test for full spider `parse_glossary()`
- [x] **Red**: Run tests (should fail)
- [x] **Green**: Convert `usa_courts_glossary.py` parser to `parse_entries()` function
- [x] **Green**: Create spider with `get_metadata()` method
- [x] **Refactor**: Clean up any duplication

### **2. USA USCIS Glossary**
- [x] **Test**: Update `tests/glossaries/parsers/usa/uscis_glossary_test.py` 
- [x] **Test**: Create spider tests
- [x] **Red**: Run tests
- [x] **Green**: Convert parser `_parse_entries()` → `parse_entries()`
- [x] **Green**: Move `_make_metadata()` → spider `get_metadata()`
- [x] **Refactor**: Remove unused functions

### **3. Ireland Courts Glossary**
- [x] **Test**: Update `tests/glossaries/parsers/irl/courts_glossary_test.py`
- [x] **Test**: Create spider tests  
- [x] **Red**: Run tests
- [x] **Green**: Convert parser
- [x] **Green**: Create spider with metadata
- [x] **Refactor**: Clean up

### **4. Australia DV Glossary**
- [ ] **Test**: Update `tests/glossaries/parsers/aus/dv_glossary_test.py`
- [ ] **Test**: Create spider tests
- [ ] **Red**: Run tests  
- [ ] **Green**: Convert parser
- [ ] **Green**: Create spider
- [ ] **Refactor**: Clean up

### **5. Australia Design IP Glossary**
- [ ] **Test**: Update `tests/glossaries/parsers/aus/designip_glossary_test.py`
- [ ] **Test**: Create spider tests
- [ ] **Red**: Run tests
- [ ] **Green**: Convert parser
- [ ] **Green**: Create spider
- [ ] **Refactor**: Clean up

### **6. Australia IP Glossary**
- [ ] **Test**: Update `tests/glossaries/parsers/aus/ip_glossary_test.py`
- [ ] **Test**: Create spider tests
- [ ] **Red**: Run tests
- [ ] **Green**: Convert parser
- [ ] **Green**: Create spider
- [ ] **Refactor**: Clean up

### **7. Australia Law Handbook Glossary**
- [ ] **Test**: Update `tests/glossaries/parsers/aus/lawhandbook_glossary_test.py`
- [ ] **Test**: Create spider tests
- [ ] **Red**: Run tests
- [ ] **Green**: Convert parser
- [ ] **Green**: Create spider
- [ ] **Refactor**: Clean up

### **8. Canada Patents Glossary**
- [ ] **Test**: Update `tests/glossaries/parsers/can/patents_glossary_test.py`
- [ ] **Test**: Create spider tests
- [ ] **Red**: Run tests
- [ ] **Green**: Convert parser
- [ ] **Green**: Create spider
- [ ] **Refactor**: Clean up

### **9. Canada Parliamentary Glossary**
- [ ] **Test**: Update `tests/glossaries/parsers/can/parliamentary_glossary_test.py`
- [ ] **Test**: Create spider tests
- [ ] **Red**: Run tests
- [ ] **Green**: Convert parser
- [ ] **Green**: Create spider
- [ ] **Refactor**: Clean up

### **10. Canada DOJ Glossaries**
- [ ] **Test**: Update `tests/glossaries/parsers/can/doj_glossaries_test.py`
- [ ] **Test**: Create spider tests
- [ ] **Red**: Run tests
- [ ] **Green**: Convert parser
- [ ] **Green**: Create spider
- [ ] **Refactor**: Clean up

### **11. Great Britain FPR Glossary**
- [ ] **Test**: Update `tests/glossaries/parsers/gbr/fpr_glossary_test.py`
- [ ] **Test**: Create spider tests
- [ ] **Red**: Run tests
- [ ] **Green**: Convert parser
- [ ] **Green**: Create spider
- [ ] **Refactor**: Clean up

### **12. Great Britain CPR Glossary**
- [ ] **Test**: Update `tests/glossaries/parsers/gbr/cpr_glossary_test.py`
- [ ] **Test**: Create spider tests
- [ ] **Red**: Run tests
- [ ] **Green**: Convert parser
- [ ] **Green**: Create spider
- [ ] **Refactor**: Clean up

### **13. USA Criminal Glossary**
- [ ] **Test**: Update `tests/glossaries/parsers/usa/criminal_glossary_test.py`
- [ ] **Test**: Create spider tests
- [ ] **Red**: Run tests
- [ ] **Green**: Convert parser
- [ ] **Green**: Create spider
- [ ] **Refactor**: Clean up

### **14. New Zealand Justice Glossary**
- [ ] **Test**: Update `tests/glossaries/parsers/nzl/justice_glossary_test.py`
- [ ] **Test**: Create spider tests
- [ ] **Red**: Run tests
- [ ] **Green**: Convert parser
- [ ] **Green**: Create spider
- [ ] **Refactor**: Clean up

### **15. Documentation**
- [ ] Write an "Architecture" section in the README that among other things, lists the Benefits (below).

## 🧹 **Phase Final: Cleanup**
- [ ] **Test**: Verify all spider integration tests pass
- [ ] **Test**: Verify all parser unit tests pass  
- [ ] **Test**: Run full test suite
- [ ] **Cleanup**: Remove `public_law/glossaries/utils/metadata.py`
- [ ] **Cleanup**: Remove any unused `_make_metadata()` functions
- [ ] **Cleanup**: Update any remaining imports/references

## 📊 **Validation**
- [ ] All tests pass
- [ ] No `_make_metadata` functions remain in parsers
- [ ] All spiders inherit from AutoGlossarySpider
- [ ] All parsers export only `parse_entries()` function
- [ ] Metadata utils directory removed

## 🎯 **Architecture Goals**

**Before**: Parser = HTML extraction + metadata creation  
**After**: 
- Parser = Pure HTML extraction (`parse_entries()`)
- Spider = Configuration + orchestration (`get_metadata()` + inherited `parse_glossary()`)

**Benefits**:
- **DRY**: `parse_glossary()` logic written once in base class
- **Type Safety**: All configuration data strongly typed in Python
- **Separation of Concerns**: Configuration vs. data extraction clearly separated
- **Testability**: Can test parsers and spiders independently 
