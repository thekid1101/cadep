"""Knowledge vault retrieval — concept index + TF-IDF fallback (PRD Section 9.3)."""

from __future__ import annotations

import json
from pathlib import Path

import yaml
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from cadep import config
from cadep.models import (
    RetrievalBundle,
    RetrievalConfidence,
    RetrievalResult,
    VaultDocument,
)


class VaultRetriever:
    """Two-pass retrieval: concept index → TF-IDF fallback."""

    def __init__(self, vault_id: str):
        self.vault_id = vault_id
        self.vault_path = config.VAULT_DIR / vault_id
        self.documents: dict[str, VaultDocument] = {}
        self.concept_index: dict[str, list[str]] = {}
        self._load_vault()

    def _load_vault(self):
        """Load all documents and the concept index from the vault directory."""
        docs_dir = self.vault_path / "documents"
        if docs_dir.exists():
            for doc_file in docs_dir.glob("*.md"):
                doc = self._parse_document(doc_file)
                if doc:
                    self.documents[doc.doc_id] = doc

        index_file = self.vault_path / "concept_index.json"
        if index_file.exists():
            self.concept_index = json.loads(index_file.read_text(encoding="utf-8"))

    def _parse_document(self, path: Path) -> VaultDocument | None:
        """Parse a vault document from a markdown file with YAML frontmatter."""
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---"):
            return None

        parts = text.split("---", 2)
        if len(parts) < 3:
            return None

        try:
            meta = yaml.safe_load(parts[1])
        except yaml.YAMLError:
            return None

        if not meta or "doc_id" not in meta:
            return None

        content = parts[2].strip()
        return VaultDocument(
            doc_id=meta["doc_id"],
            title=meta.get("title", ""),
            authors=meta.get("authors", []),
            year=meta.get("year", 0),
            citation_count=meta.get("citation_count", 0),
            source_url=meta.get("source_url"),
            concept_tags=meta.get("concept_tags", []),
            superseded_by=meta.get("superseded_by"),
            coverage_quality=meta.get("coverage_quality", "abstract-only"),
            math_syntax_status=meta.get("math_syntax_status", "no-math"),
            cadep_citation_count=meta.get("cadep_citation_count", 0),
            last_verified=meta.get("last_verified"),
            slot_justification=meta.get("slot_justification", ""),
            content=content,
        )

    def retrieve(self, concept_tags: list[str], query_text: str) -> RetrievalBundle:
        """Two-pass retrieval per PRD Section 9.3."""
        if not self.documents:
            return RetrievalBundle(confidence=RetrievalConfidence.LOW)

        # Pass 1: Concept index
        concept_results = self._concept_lookup(concept_tags)
        concept_confidence = self._assess_concept_confidence(concept_tags, concept_results)

        # Pass 2: TF-IDF fallback on MEDIUM or LOW concept confidence
        tfidf_triggered = concept_confidence in (RetrievalConfidence.MEDIUM, RetrievalConfidence.LOW)
        tfidf_results = []
        if tfidf_triggered:
            tfidf_results = self._tfidf_search(query_text)

        # Merge results (concept results first, then TF-IDF additions)
        seen = {r.doc_id for r in concept_results}
        merged = list(concept_results)
        for r in tfidf_results:
            if r.doc_id not in seen:
                merged.append(r)
                seen.add(r.doc_id)

        # Compute overall confidence
        overall = self._compute_overall_confidence(
            concept_confidence, concept_results, tfidf_results
        )

        return RetrievalBundle(
            results=merged,
            confidence=overall,
            concept_tags_matched=[t for t in concept_tags if self._tag_in_index(t)],
            tfidf_triggered=tfidf_triggered,
        )

    def get_documents(self, doc_ids: list[str]) -> list[VaultDocument]:
        """Fetch full documents by ID."""
        return [self.documents[did] for did in doc_ids if did in self.documents]

    def _concept_lookup(self, tags: list[str]) -> list[RetrievalResult]:
        """Look up doc_ids from concept index via tags."""
        matched_docs: dict[str, float] = {}
        for tag in tags:
            doc_ids = self._resolve_tag(tag)
            for doc_id in doc_ids:
                matched_docs[doc_id] = matched_docs.get(doc_id, 0) + 1.0

        results = [
            RetrievalResult(doc_id=did, score=score, method="concept_index")
            for did, score in sorted(matched_docs.items(), key=lambda x: -x[1])
        ]
        return results

    def _resolve_tag(self, tag: str) -> list[str]:
        """Resolve a concept tag to doc_ids, handling max 2 nesting levels."""
        if tag in self.concept_index:
            value = self.concept_index[tag]
            if isinstance(value, list):
                # Could be doc_ids or nested tags
                result = []
                for item in value:
                    if isinstance(item, str) and item in self.concept_index:
                        nested = self.concept_index[item]
                        if isinstance(nested, list):
                            result.extend(nested)
                    elif isinstance(item, str):
                        result.append(item)
                return result
        return []

    def _tag_in_index(self, tag: str) -> bool:
        return tag in self.concept_index

    def _assess_concept_confidence(
        self, tags: list[str], results: list[RetrievalResult]
    ) -> RetrievalConfidence:
        matched = sum(1 for t in tags if self._tag_in_index(t))
        if matched > 0 and len(results) >= 3:
            return RetrievalConfidence.HIGH
        if matched > 0:
            return RetrievalConfidence.MEDIUM
        return RetrievalConfidence.LOW

    def _tfidf_search(self, query_text: str) -> list[RetrievalResult]:
        """TF-IDF search over document contents."""
        if not self.documents:
            return []

        doc_ids = list(self.documents.keys())
        corpus = [
            f"{self.documents[did].title} {' '.join(self.documents[did].concept_tags)} {self.documents[did].content}"
            for did in doc_ids
        ]

        vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
        try:
            tfidf_matrix = vectorizer.fit_transform(corpus)
        except ValueError:
            return []

        query_vec = vectorizer.transform([query_text])
        similarities = cosine_similarity(query_vec, tfidf_matrix)[0]

        results = []
        for idx in similarities.argsort()[::-1][: config.TFIDF_TOP_K]:
            score = float(similarities[idx])
            if score > 0:
                results.append(
                    RetrievalResult(doc_id=doc_ids[idx], score=score, method="tfidf")
                )
        return results

    def _compute_overall_confidence(
        self,
        concept_conf: RetrievalConfidence,
        concept_results: list[RetrievalResult],
        tfidf_results: list[RetrievalResult],
    ) -> RetrievalConfidence:
        """Compute overall retrieval confidence per PRD Section 9.3."""
        total_docs = len(set(
            r.doc_id for r in concept_results + tfidf_results
        ))

        if concept_conf == RetrievalConfidence.HIGH and total_docs >= 3:
            return RetrievalConfidence.HIGH
        if concept_conf == RetrievalConfidence.MEDIUM:
            return RetrievalConfidence.MEDIUM
        if tfidf_results and tfidf_results[0].score > config.TFIDF_MIN_SIMILARITY:
            return RetrievalConfidence.MEDIUM
        if total_docs < 2:
            return RetrievalConfidence.LOW
        return RetrievalConfidence.LOW
