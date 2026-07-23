/** More efficient evidence range finder via normalized index mapping. */
export function findEvidenceRange(
  answer: string,
  evidence: string,
): { start: number; end: number } | null {
  if (!evidence.trim()) return null;
  const exact = answer.indexOf(evidence);
  if (exact >= 0) return { start: exact, end: exact + evidence.length };

  const punct: Record<string, string> = {
    "\u2018": "'",
    "\u2019": "'",
    "\u201a": "'",
    "\u201b": "'",
    "\u201c": '"',
    "\u201d": '"',
    "\u201e": '"',
    "\u2013": "-",
    "\u2014": "-",
    "\u2212": "-",
    "\u2192": "->",
    "\u21d2": "->",
    "\u2026": "...",
    "\u00a0": " ",
  };

  function fold(ch: string): string {
    return punct[ch] ?? ch;
  }

  // Build normalized answer + map from norm index → original index
  let normAnswer = "";
  const map: number[] = [];
  let prevSpace = false;
  const raw = answer.normalize("NFKC");
  for (let i = 0; i < raw.length; i++) {
    let piece = fold(raw[i]).toLowerCase();
    if (/\s/.test(piece)) {
      if (prevSpace || normAnswer.length === 0) continue;
      piece = " ";
      prevSpace = true;
    } else {
      prevSpace = false;
    }
    for (let k = 0; k < piece.length; k++) {
      normAnswer += piece[k];
      map.push(i);
    }
  }
  normAnswer = normAnswer.trimEnd();

  let normEvidence = "";
  prevSpace = false;
  const ev = evidence.normalize("NFKC");
  for (let i = 0; i < ev.length; i++) {
    let piece = fold(ev[i]).toLowerCase();
    if (/\s/.test(piece)) {
      if (prevSpace || normEvidence.length === 0) continue;
      piece = " ";
      prevSpace = true;
    } else {
      prevSpace = false;
    }
    normEvidence += piece;
  }
  normEvidence = normEvidence.trim();
  if (!normEvidence) return null;

  const at = normAnswer.indexOf(normEvidence);
  if (at < 0) {
    const token = normEvidence.split(" ").find((t) => t.length > 2);
    if (!token) return null;
    const ti = answer.toLowerCase().indexOf(token);
    if (ti < 0) return null;
    return { start: ti, end: ti + token.length };
  }
  const start = map[at] ?? 0;
  const endIdx = map[at + normEvidence.length - 1] ?? start;
  return { start, end: endIdx + 1 };
}

export function highlightEvidence(
  answer: string,
  evidence: string,
): { before: string; match: string; after: string } | null {
  const range = findEvidenceRange(answer, evidence);
  if (!range) return null;
  return {
    before: answer.slice(0, range.start),
    match: answer.slice(range.start, range.end),
    after: answer.slice(range.end),
  };
}
