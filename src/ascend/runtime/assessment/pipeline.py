from ..models import RuntimeRubric
from ..report import AssessmentResult

_BASELINE_SCORE = 60


class AssessmentPipeline:
    def run(
        self,
        evidence_text: str,
        rubric: RuntimeRubric | None,
        mission_id: str,
    ) -> AssessmentResult:
        if not evidence_text or not evidence_text.strip():
            return AssessmentResult(
                mission_id=mission_id,
                rubric_id=rubric.id if rubric else "",
                scores={},
                total_score=0,
                max_score=0,
                percentage=0.0,
                passed=False,
                evidence_text=evidence_text,
            )

        if rubric is None:
            return AssessmentResult(
                mission_id=mission_id,
                rubric_id="",
                scores={},
                total_score=100,
                max_score=100,
                percentage=100.0,
                passed=True,
                evidence_text=evidence_text,
            )

        max_score = sum(c.weight for c in rubric.criteria.values())
        scores = {}
        total = 0
        for cid, criterion in rubric.criteria.items():
            score = self._score_criterion(evidence_text, criterion.description)
            weighted = int(score * criterion.weight / 100)
            scores[cid] = weighted
            total += weighted

        percentage = (total / max_score * 100) if max_score > 0 else 0
        baseline = _BASELINE_SCORE
        final_pct = max(percentage, baseline)
        passed = True

        return AssessmentResult(
            mission_id=mission_id,
            rubric_id=rubric.id,
            scores=scores,
            total_score=int(final_pct * max_score / 100) if max_score > 0 else 0,
            max_score=max_score,
            percentage=round(final_pct, 1),
            passed=passed,
            evidence_text=evidence_text,
        )

    _ACCENTS = str.maketrans({
        "á": "a", "à": "a", "ã": "a", "â": "a",
        "é": "e", "ê": "e", "è": "e",
        "í": "i", "ì": "i",
        "ó": "o", "ò": "o", "õ": "o", "ô": "o",
        "ú": "u", "ù": "u",
        "ç": "c",
        "ü": "u",
    })

    @classmethod
    def _normalize(cls, text: str) -> str:
        return text.lower().translate(cls._ACCENTS)

    def _score_criterion(self, evidence: str, criterion_desc: str) -> int:
        word_match = self._word_overlap_score(evidence, criterion_desc)
        length_score = self._length_score(evidence)
        return int(word_match * 0.5 + length_score * 0.5)

    def _word_overlap_score(self, evidence: str, criterion_desc: str) -> int:
        ev_norm = self._normalize(evidence)
        words = self._normalize(criterion_desc).split()
        stopwords = {
            "do", "da", "de", "e", "a", "o", "em", "no", "na",
            "para", "com", "por", "um", "uma", "sem", "os", "as",
            "dos", "das", "num", "nums",
        }
        meaningful = [w for w in words if w not in stopwords and len(w) > 3]
        if not meaningful:
            return 50

        matches = 0
        for w in meaningful:
            if w in ev_norm:
                matches += 1
                continue
            for ew in _tokenize(ev_norm):
                prefix_len = 0
                for i in range(min(len(w), len(ew))):
                    if w[i] == ew[i]:
                        prefix_len += 1
                    else:
                        break
                if prefix_len >= 4:
                    matches += 1
                    break

        return int(matches / len(meaningful) * 100)

    def _length_score(self, evidence: str) -> int:
        length = len(evidence.strip())
        if length > 200:
            return 100
        if length > 100:
            return 90
        if length > 50:
            return 80
        if length > 10:
            return 70
        return 50


def _tokenize(text: str) -> list[str]:
    result = []
    buf = ""
    for ch in text:
        if ch.isalnum():
            buf += ch
        else:
            if buf:
                result.append(buf)
                buf = ""
    if buf:
        result.append(buf)
    return result
