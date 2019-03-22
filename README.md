[![Build Status](https://travis-ci.com/public-law/oregon-administrative-rules-parser.svg?branch=master)](https://travis-ci.com/public-law/oregon-administrative-rules-parser)

# Oregon Administrative Rules Parser
Parse the OAR into well formed JSON

```bash
$ scrapy crawl secure.sos.state.or.us
```

This produces the output:

```json
{
  "date_accessed": "2019-03-21",
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
          "name": "Procedural Rules",
          "url": "https://secure.sos.state.or.us/oard/displayDivisionRules.action?selectedDivision=1",
          "rules": [
            {
              "kind": "Rule",
              "number": "101-001-0000",
              "name": "Notice of Proposed Rule Changes",
              "url": "https://secure.sos.state.or.us/oard/view.action?ruleNumber=101-001-0000",
              "authority": [
                "ORS 243.061 - 243.302"
              ],
              "implements": [
                "ORS 183.310 - 183.550",
                "192.660",
                "243.061 - 243.302",
                "292.05"
              ],
              "history": "PEBB 2-2009, f. 7-29-09, cert. ef. 8-1-09<br>PEBB 1-2009(Temp), f. &amp; cert. ef. 2-24-09 thru 8-22-09<br>PEBB 1-2004, f. &amp; cert. ef. 7-2-04<br>PEBB 1-1999, f. 12-8-99, cert. ef. 1-1-00",
              "text": "<p>Prior to adoption, amendment, or repeal of any rule,"
```
(etc.)


Development Environment Notes
-----------------------------

Run the pytest tests like this:

```bash
pytest
```
