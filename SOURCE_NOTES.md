# Source identification

The course report was explicitly identified by the project author as `pkudsa-group13`. The original available file is `pkudsa-group13(2).docx` in the parent Data Structures and Algorithms directory. It is copied byte-for-byte to `paper/pkudsa-group13.docx`.

- Original report SHA-256: `e2374f7d5310344943d7c677a9366420c27fa2797105d6b8c66c5a42a5eb6fef`.
- Primary code: Team 13 member `group_2023_13_230603_192731.py` inside the existing class competition archive `大作业/Code/刘老师班代码.zip`.
- Original archived code SHA-256: `e74b1355a17fecc0611acf5aefb364581e56026cca394a60c426c272c2bd6d3f`.
- Public copy: `code/group13_agent.py`; only comments were translated. AST equality was checked with runtime strings and all executable expressions included.

The report explicitly discusses one-/two-/three-ply greedy search, declining unfavorable exchanges, same-color swaps, anti-stalling, final-round decisions and alpha-beta pruning. The recovered Team 13 entry implements this strategy family and is identified by a team-numbered competition filename, rather than inferred from a generic player filename.

The report and archived entry differ in their pass threshold (-4 versus 6) and some details. The filename is evidence of a saved Team 13 competition entry; it does not prove that no later revision existed. The archive preserves the evidence rather than editing historical parameters.

The document previously uploaded as `paper/report.*` was the course story `弈者`, not the algorithm report. It is removed from the current tree. The previous Monte Carlo player is also removed because it is not the report's central method.
