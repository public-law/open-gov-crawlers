# oregon-administrative-rules-parser
Parse the Oregon Administrative Rules into well formed JSON

```bash
$ scrapy crawl secure.sos.state.or.us
```

This produces the output:

```json
{
  "chapters": [
    {
      "kind": "Chapter",
      "db_id": "36",
      "number": "101",
      "name": "Oregon Health Authority, Public Employees' Benefit Board",
      "url": "https://secure.sos.state.or.us/oard/displayChapterRules.action?selectedChapter=36",
      "divisions": [
        {
          "kind": "Division",
          "db_id": "1",
          "number": "1",
          "name": "PROCEDURAL RULES",
          "url": "https://secure.sos.state.or.us/oard/displayDivisionRules.action?selectedDivision=1",
          "rules": [
            {
              "kind": "Rule",
              "number": "101-001-0000",
              "name": "Notice of Proposed Rule Changes",
              "url": "https://secure.sos.state.or.us/oard/view.action?ruleNumber=101-001-0000",
              "text": "<p>Prior to adoption, amendment, or repeal of any rule, the Public Employees' Benefit Board...
```
(etc.)
