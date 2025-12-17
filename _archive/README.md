# Archive Directory

This folder contains legacy duplicates and deprecated code moved during system cleanup.

## Contents

- **caleon_workspace_YYYYMMDD/**: Duplicate workspace containing 6 full UCM instances (demo, stress tests, production). Archived as redundant - canonical system is in root.

- **cerebral_cortex_YYYYMMDD/**: Duplicate cortex implementation with voice_processor. Archived - canonical cortex modules are in root `modules/`.

## Reason for Archival

During structural audit (see STRUCTURAL_AUDIT_CRITICAL.md), massive code duplication was discovered:
- 6 complete UCM instances in caleon_workspace/
- Duplicate voice_processor.py implementations
- Duplicate cerebral_cortex folder structures

These duplicates caused:
- Confusion about canonical codebase location
- Version drift between copies
- Storage waste

## Restoration

If needed, these can be restored from this archive. However, the canonical, actively maintained system is in the root workspace folder.

**Date Archived**: System cleanup during router and voice integration fixes
**Reason**: Eliminate code duplication and establish single source of truth
