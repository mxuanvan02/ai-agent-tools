# Third-party notices

This repository does not vendor PPT Master or OfficeCLI binaries/source trees. The installer downloads them from their official repositories/package distribution at pinned versions.

## PPT Master

- Project: https://github.com/hugohe3/ppt-master
- Pinned revision: `bc5c3afe92b21250bd188d40134fa251aedbb8b2`
- License: MIT
- Copyright: © 2025–2026 Hugo He
- Local change: `patches/ppt-master-opc-package-absolute-target.patch` changes internal OPC target resolution to accept package-absolute targets. The modified file is clearly identified and its post-patch SHA-256 is locked.

The upstream MIT license is reproduced at `third_party/PPT-MASTER-LICENSE`.

## OfficeCLI

- Project: https://github.com/iOfficeAI/OfficeCLI
- Package: `@officecli/officecli@1.0.137`
- License: Apache License 2.0
- Copyright 2026 OfficeCLI (https://OfficeCLI.AI), created and maintained by goworm.

The upstream license and required NOTICE are reproduced under `third_party/`.

## Excluded optional dependency

`PyMuPDF` is not installed or redistributed by this tool. PDF-to-Markdown support requiring it is outside the default pipeline.
