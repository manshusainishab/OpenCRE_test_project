Step 1: Regex Filter
  - lockfiles
  - pure formatting
  - obvious junk

Step 2: File-Type Routing

  If source code:
      → CodeRabbit
         If semantic change:
             → Gemini
         Else:
             discard

  If Markdown/YAML/config:
      → Gemini directly

Step 3: Knowledge Queue


Note:- the code rabbit can reduce API call cost as a pre filter for lint,format changes