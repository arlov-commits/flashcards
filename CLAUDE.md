Git Workflow
ALWAYS commit directly to main. Never create a branch unless explicitly told to.
After every numbered task item, stage all changes and push directly to main.
Bump the patch version (v2.Y → v2.Y+1) in the HTML meta/comment header with each commit. When at vX.9, the next version is v(X+1).0 (e.g. v2.9 → v3.0).
Commit message format: vX.Y – [brief description]
Never open a PR. Never use git checkout -b.
