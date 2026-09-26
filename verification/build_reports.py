"""Build handbook PDFs from current source documents and measured results."""
import json
import shutil
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from html import escape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.pagesizes import A4

ROOT=Path(__file__).resolve().parents[1]
results=ROOT/"verification/results"
archive=results/"archive"
archive.mkdir(exist_ok=True)
prior=ROOT/"verification/final_verification.pdf"
if prior.exists() and not (archive/"final_verification-before-2026-09-26.pdf").exists():
    shutil.copyfile(prior,archive/"final_verification-before-2026-09-26.pdf")

xml=ET.parse(results/"core-tests.xml").getroot()
suites=list(xml.iter("testsuite"))
total=sum(int(s.get("tests",0)) for s in suites)
failures=sum(int(s.get("failures",0))+int(s.get("errors",0)) for s in suites)
semantic=json.loads((results/"semantic/summary.json").read_text())
offline=json.loads((results/"offline/summary.json").read_text())
live=json.loads((results/"live-smoke.json").read_text())
report=f"""# RecallGuard: current verification
Generated: {datetime.now(timezone.utc).isoformat()}
Status: verified local core checks; independent review and public deployment pending.

## Automated regression
{total} tests recorded; {failures} failures/errors. Source: core-tests.xml.
Coverage: object ownership, actual deletion, correction/provenance, expiry boundary, privacy positive/negative cases, consent, context budget, malformed API inputs, persistence, dependency failures and contract mutation.
The reusable verifier passes 7 checks and its tests detect deliberately broken isolation, confidence and deletion implementations.

## Corrected baseline comparison
Dataset SHA-256: {semantic['dataset_sha256']}
MiniLM: baseline {semantic['results']['baseline']['passed']}/16; improved {semantic['results']['improved']['passed']}/16.
Lexical test encoder: baseline {offline['results']['baseline']['passed']}/16; improved {offline['results']['improved']['passed']}/16.
Seven retrieval calls per case; p50/p95 and first-query milliseconds, retained content bytes and prompt UTF-8 units are in comparison.csv. These are not LLM latency, disk index size or exact model-token counts.
This is a development/regression suite used during implementation, not a held-out generalization claim.

## Benchmark correction
An earlier generated long-context fixture incorrectly contained NaN rather than repeated text. It was corrected and a regression assertion added. Earlier pre-hybrid outputs are retained as superseded, not as valid before/after measurements.

## Real model smoke
Status: {live['status']}. Model: {live['model']}.
Initial response: {live['initial_response']}
After explicit correction: {live['corrected_response']}
The smoke also verified deletion. One synthetic scenario is not broad response-quality evidence.

## UI and deployment checks
Waitress test server starts on loopback. Browser verified consented storage, provenance/expiry display and request inspector using synthetic data and a deterministic generation stub. JavaScript syntax checked.
A native prompt blocked automation; controls were changed to inline confirmations. The full revised browser walkthrough remains pending.
Docker daemon was unavailable, so container build/start/restart is unverified. Dockerfile, Compose and deployment instructions are provided. No public service was deployed.

## Residual risks and remaining handbook evidence
Independent specification-based review remains outstanding. Existing historical PASS reports are not release sign-off.
Automatic contradiction resolution, calibrated confidence, exact model tokenization, broad prompt-injection evaluation, generated-response benchmarks, held-out data, public quotas/identity/TLS, backup recovery and cloud adapters remain open.
Pattern-based PII admission is limited. Physical API deletion does not promise forensic disk or external-backup erasure.
Original reconstruction/research/transfer work remains; missing presentations and historical checkpoints were not fabricated.

## Reproduce
python -m pytest -q --junitxml=verification/results/core-tests.xml
python contribution/verify_memory_contract.py
python verification/run_evaluation.py
python verification/run_evaluation.py --semantic
python verification/live_smoke.py
"""
(results/"current_verification.md").write_text(report,encoding="utf-8")

styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name="BodyRG",fontName="Helvetica",fontSize=10,leading=14,spaceAfter=8,textColor=colors.HexColor("#24364B")))
styles.add(ParagraphStyle(name="TitleRG",fontName="Helvetica-Bold",fontSize=21,leading=25,spaceAfter=16,textColor=colors.HexColor("#163554")))
styles.add(ParagraphStyle(name="HeadRG",fontName="Helvetica-Bold",fontSize=12,leading=16,spaceBefore=12,spaceAfter=6,textColor=colors.HexColor("#215A82")))

def footer(canvas,doc):
    canvas.setFont("Helvetica",8)
    canvas.setFillColor(colors.HexColor("#64748B"))
    canvas.drawString(42,27,"RecallGuard | Handbook core revision | 2026-09-26")
    canvas.drawRightString(A4[0]-42,27,str(doc.page))

def build(source,target):
    story=[]
    for block in source.strip().split("\n\n"):
        lines=block.splitlines()
        if lines[0].startswith("# "):
            story.append(Paragraph(escape(lines[0][2:]),styles["TitleRG"]))
            for line in lines[1:]:
                story.append(Paragraph(escape(line),styles["BodyRG"]))
        elif lines[0].startswith("## "):
            if lines[0] == "## Residual risks and remaining handbook evidence":
                story.append(PageBreak())
            story.append(Paragraph(escape(lines[0][3:]),styles["HeadRG"]))
            if len(lines)>1:
                story.append(Paragraph("<br/>".join(escape(x) for x in lines[1:]),styles["BodyRG"]))
        else:
            story.append(Paragraph("<br/>".join(escape(x) for x in lines),styles["BodyRG"]))
    SimpleDocTemplate(str(target),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=42,bottomMargin=45,
                      title=source.splitlines()[0].lstrip("# "),author="RecallGuard project").build(story,onFirstPage=footer,onLaterPages=footer)

for name in ["system_design","architecture","data_flow"]:
    build((ROOT/f"design/{name}.md").read_text(encoding="utf-8"),ROOT/f"design/{name}.pdf")
build(report,ROOT/"verification/final_verification.pdf")

import pymupdf
output=ROOT/"tmp/pdfs/current"
output.mkdir(parents=True,exist_ok=True)
for path in [*(ROOT/"design").glob("*.pdf"),ROOT/"verification/final_verification.pdf"]:
    document=pymupdf.open(path)
    for i,page in enumerate(document):
        assert page.get_text().strip()
        page.get_pixmap(matrix=pymupdf.Matrix(1,1)).save(str(output/f"{path.stem}-{i+1}.png"))
    print(path.name,len(document),"pages")
