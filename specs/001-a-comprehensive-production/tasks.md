# Tasks: RAG Toolkit

**Input**: Design documents from `/specs/001-a-comprehensive-production/`
**Prerequisites**: plan.md (required), research.md, data-model.md, quickstart.md

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
- **Single project**: `core/`, `tests/` at repository root

## Phase 3.1: Setup
- [ ] T001 Create the directory structure for the RAG toolkit in `core/`.
- [ ] T002 Install all dependencies from `requirements.txt`.
- [ ] T003 [P] Configure `ruff` for linting and formatting.

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**
- [ ] T004 [P] Create `tests/test_chunker.py` to test the document chunking functionality.
- [ ] T005 [P] Create `tests/test_embedder.py` to test the sentence embedding functionality.
- [ ] T006 [P] Create `tests/integration/test_integration_services.py` to test the full RAG pipeline.
- [ ] T007 [P] Create a test for the `file_loader` in `core/loaders/`.
- [ ] T008 [P] Create a test for the `url_loader` in `core/loaders/`.

## Phase 3.3: Core Implementation (ONLY after tests are failing)
- [ ] T009 Implement the `Document` data class in `core/utils.py`.
- [ ] T010 Implement the `Chunker` class in `core/chunker.py`.
- [ ] T011 Implement the `Embedder` class in `core/embedder.py`.
- [ ] T012 Implement the `Indexer` base class in `core/indexer.py`.
- [ ] T013 Implement the `IndexerFaissIVFPQ` class in `core/indexer_faiss_ivfpq.py`.
- [ ] T014 Implement the `LoaderBase` class in `core/loader_base.py`.
- [ ] T015 Implement the `FileLoader` class in `core/loaders/file_loader.py`.
- [ ] T016 Implement the `UrlLoader` class in `core/loaders/url_loader.py`.
- [ ] T017 Implement the `Retriever` class in `core/retriever.py`.
- [ ] T018 Implement the `RAGService` class in `mcp/rag_service.py` to orchestrate the RAG pipeline.
- [ ] T019 Implement the FastAPI endpoint in `mcp/api.py` to expose the RAG service.

## Phase 3.4: Integration
- [ ] T020 Integrate the `Chunker`, `Embedder`, `Indexer`, and `Retriever` into the `RAGService`.
- [ ] T021 Add logging to all major components.

## Phase 3.5: Polish
- [ ] T022 [P] Write comprehensive unit tests for all components.
- [ ] T023 [P] Add docstrings to all public classes and methods.
- [ ] T024 [P] Create a `README.md` with detailed instructions on how to use the RAG toolkit.

## Dependencies
- Tests (T004-T008) before implementation (T009-T019)
- T009 blocks T010, T015, T016
- T010, T011, T013, T017 block T020
- T018 blocks T019, T020
- Implementation before polish (T022-T024)

## Parallel Example
```
# Launch T004-T008 together:
Task: "Create tests/test_chunker.py to test the document chunking functionality."
Task: "Create tests/test_embedder.py to test the sentence embedding functionality."
Task: "Create tests/integration/test_integration_services.py to test the full RAG pipeline."
Task: "Create a test for the file_loader in core/loaders/."
Task: "Create a test for the url_loader in core/loaders/."
```
