# CHANGELOG - Unified Cognition Module

## [2.0.1] - 2025-12-17

### 🎯 Major Architecture Cleanup & Voice Integration

#### Fixed
- **Router Initialization**: Fixed ConnectionRouter to use proper class instantiation with direct_cognitive_handler
- **Duplicate Registrations**: Removed duplicate router registrations from main.py (bubble, health, iss routers already in routes.py)
- **Fallback Mode Bug**: All adversarial tests were running through fallback exception handler instead of proper routing
- **Module Dependencies**: Restored persona/, articulator/, generative/ folders as active dependencies

#### Added
- **Voice Integration**: Integrated Cochlear Processor (Whisper ASR) and Phonatory Output (Coqui TTS) into CaleonCore.process()
  - Audio input detection and speech-to-text preprocessing
  - Text-to-speech output generation for voice responses
  - Graceful degradation if voice systems unavailable
- **Architecture Documentation**: Created comprehensive STRUCTURAL_AUDIT_CRITICAL.md documenting system issues
- **Archive System**: Moved duplicate code to _archive/ with documentation:
  - caleon_workspace/ (6 duplicate UCM instances)
  - cerebral_cortex/ (duplicate cortex implementation)
  - unused_routers/ (orphaned but functional routers)

#### Changed
- **CaleonCore**: Enhanced with voice I/O processing stages
- **Routing Logic**: Cleaned up to use single registration point in main.py
- **Module Structure**: Clarified dependencies vs unused code

#### Architecture Improvements
- **Connection Router**: Now properly routes through direct_cognitive_handler → CaleonCore
- **Voice Pipeline**: Full integration from audio input → Cochlear → Brain → Phonatory → audio output
- **Code Deduplication**: Eliminated massive redundancy in workspace folders
- **Dependency Management**: Clear separation of active vs archived code

### Testing Notes
- Previous adversarial test results (15 tests) were invalid - ran through fallback, not real routing
- System requires retesting after cleanup to validate proper routing engagement
- Voice integration tested with graceful fallback for systems without audio hardware

### Known Issues
- Cali X One (ISS Module on port 8003) still isolated from core - requires integration
- Orphaned routers (articulator, generative, persona) functional but not exposed via FastAPI endpoints
- System startup requires all dependencies present despite graceful degradation features

---

## [2.0.0] - 2025-11-01

### Initial AGI Release
- Super-Knowledge Graph (SKG) architecture
- Unified Cognition Module with brain modules (Resonator, Helixes, Echo, Harmonizer)
- Reflection Vault with cycle storage
- Connection Router for task routing
- ISS Module integration framework
- Voice system foundation (Cochlear Processor, Phonatory Output)
- Comprehensive API endpoints (/reason, /api/skg/*, /api/uqv/*, etc.)
- Docker containerization support
- Adversarial testing framework

---

## Version History

- **2.0.1** (2025-12-17): Architecture cleanup, voice integration, bug fixes
- **2.0.0** (2025-11-01): Initial AGI system release
- **1.x**: Pre-release development and prototyping
