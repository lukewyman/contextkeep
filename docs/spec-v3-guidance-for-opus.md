# ContextKeep Spec V3 - Guidance for Opus

**Purpose**: Update the master ContextKeep specification to reflect our new feature-by-feature, UC-driven development approach.

**Date**: 2025-11-16

---

## The New Approach

We've shifted from spec-heavy, module-complete development to **incremental, feature-driven development** using Use Case documents (UCs). Each UC represents one demonstrable feature that can be built, tested, and verified independently.

### Key Principles

1. **Feature-First, Not Module-First**
   - Build one complete feature at a time (UI + backend + tests)
   - No code for future use ("YAGNI" - You Aren't Gonna Need It)
   - Each UC adds something the user can see and interact with

2. **Organized Like Microservices**
   - Backend modules organized as if they were microservices (clean APIs, clear boundaries)
   - Each module has: `api.py` (HTTP), `service.py` (business logic), `models.py` (Pydantic schemas)
   - Modules call each other's service functions directly (not HTTP since it's a monolith)

3. **Centralized Testing**
   - All tests in `backend/tests/` (not co-located with modules)
   - Unit tests mock dependencies, integration tests use real I/O
   - Easy to exclude from Electron builds

4. **Chunked Implementation**
   - Work in small chunks: models → services → API → frontend
   - Run tests after each chunk (fast feedback loop)
   - Iterate with Claude when hitting errors

5. **Living Specification**
   - Master spec evolves based on what we've actually built
   - Not a rigid plan, but a reflection of reality
   - Opus updates master spec periodically as UCs are completed

### What Changed From V2

**Keep from V2**:
- Core vision and philosophy (LLM-driven, TDD, spec-first)
- Pydantic-structured responses from Claude
- Phase state machine concept
- Reference cards and work orders
- Overall architecture diagrams

**Change from V2**:
- ~~Build entire modules (SS-01, SS-02, etc.)~~ → Build features (UC-001, UC-002, etc.)
- ~~Complete all file operations before moving on~~ → Build what's needed for each feature
- ~~Rigid implementation order~~ → Flexible, feature-driven order
- ~~Abstract module planning~~ → Concrete UI wireframes first, then discover modules

---

## Reference Documents

You have access to:

1. **`project-approach-revisit.md`** - Original write-up explaining the problems with the old approach and the new way forward
2. **`UC-template.md`** - Template for creating new UC specs
3. **`UC-001-list-projects.md`** - Complete example of a UC spec with all sections filled in

Use these as your guide for understanding the new structure.

---

## Your Task: Create ContextKeep Unified Spec V3

### What to Keep

- Executive Summary (update to reflect UC-driven approach)
- Core Architecture diagram
- Technology Stack
- Data Models (Pydantic examples)
- Phase State Machine
- Reference Cards concept
- Work Orders concept
- Configuration examples

### What to Update

1. **Development Workflow** → Feature-by-feature with UC specs
   - Replace SS-01, SS-02, etc. with UC-001, UC-002, etc.
   - Show how UCs build up the system incrementally
   - Emphasize wireframes → modules → contracts → tests → code

2. **Implementation Strategy** → Chunked approach
   - Remove "build entire modules first"
   - Add "build features in chunks"
   - Reference UC-template.md for chunk structure

3. **Module Organization** → Microservice-like structure
   - Show centralized tests (`backend/tests/`)
   - Emphasize clean module boundaries
   - Document how modules call each other

4. **Roadmap** → Replace with UC list
   - List completed UCs (currently just UC-001)
   - List planned UCs (see next section)
   - Remove SS-XX references

### What to Remove

- Specific SS-XX sub-spec references (replace with UC-XXX references)
- Detailed implementation for incomplete features
- Anything that contradicts the new UC-driven approach

---

## Planned Use Cases (Next Steps)

### Project Management
- **UC-001: List Projects** ✅ COMPLETE
  - Display all ContextKeep projects, alphabetically sorted
  - Expand/collapse for details, "Create New Project" widget

- **UC-002: Create GitHub Repository**
  - Create new GitHub repo from template using GitHub API
  - Template contains: basic Python/FastAPI structure, Makefile, .gitignore
  
- **UC-003: Clone and Initialize Project**
  - Clone newly created repo to `~/contextkeep-projects/[name]`
  - Initialize `.contextkeep/` directory structure
  - Create initial `project.json` metadata file
  - Display project files in UI (Files tab)

### Microservice Management
- **UC-004: Add Microservice to Project**
  - UI form to add new microservice to existing project
  - Creates microservice directory structure
  - Initializes phase states (handlers → SPEC_ADDABLE)
  - Creates service-specific Makefile

- **UC-005: List Microservices in Project**
  - Show all microservices in "Work" tab
  - Display phase status for each
  - Allow navigation to microservice details

### Spec Generation (From V2)
- **UC-006+**: Spec wizard, validation, acceptance
  - Interactive wizard for spec creation
  - Direct Claude API integration
  - Validation and acceptance flow
  - (Details in V2 spec, adapt to UC format)

---

## Structure for V3 Spec

```markdown
# ContextKeep IDE - Unified Technical Specification V3

## 1. Executive Summary
[Updated vision emphasizing UC-driven development]

## 2. Core Architecture
[Keep architecture diagram, update workflow section]

## 3. Development Approach
[NEW - Feature-first, UC-driven, chunked implementation]

## 4. Module Organization
[Microservice-like structure, centralized tests]

## 5. Use Case Roadmap
[List of UCs - completed and planned]

## 6. Phase State Machine
[Keep from V2]

## 7. Data Models
[Keep examples from V2]

## 8. Implementation Patterns
[How to use UC template, chunk strategy]

## 9. Technology Stack
[Keep from V2]

## 10. Configuration
[Keep from V2]

## Appendices
- Appendix A: UC Template Structure
- Appendix B: Example Pydantic Exchanges
- Appendix C: Git Workflow Patterns
```

---

## Guidance for Tone

- **Practical, not theoretical** - Emphasize what we're actually building
- **Grounded in UCs** - Reference UC-001 as proof of concept
- **Evolutionary** - Spec grows as we build, not dictated upfront
- **Flexible** - Allow for discovery and learning as we implement

---

## Key Message for V3

**ContextKeep is built feature-by-feature using UC specs. Each UC adds a complete, demonstrable capability. The master spec reflects what we've built and provides patterns for future UCs. We discover the best module boundaries by building real features, not by planning modules abstractly.**

---

## Summary

Create a V3 spec that:
1. Preserves the core vision and technical decisions from V2
2. Replaces module-driven (SS-XX) approach with feature-driven (UC-XXX) approach
3. Documents the UC template and chunked implementation pattern
4. Lists completed and planned UCs
5. Serves as a living document that evolves as we build

Use `project-approach-revisit.md`, `UC-template.md`, and `UC-001-list-projects.md` as your primary references.

---

**End of Guidance Document**
