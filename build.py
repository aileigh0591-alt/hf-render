# -*- coding: utf-8 -*-
"""job.json(봇이 보낸 장면 데이터) → render/index.html + subs.ass   [hf-1.0]

사용: python build.py job.json            (기본 출력: render/index.html, subs.ass)
job = {"job_id", "tag", "date", "total", "scenes": [{start, dur, chip, t1, t2, big:{text,color,desc}|null, body:{type,...}}], "ass": "..."}
렌더: cd render && npx --yes hyperframes@0.8.208 render
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent


def build(job, out_dir=HERE / "render"):
    total = round(float(job["total"]), 3)
    tpl = (HERE / "engine.html").read_text(encoding="utf-8")
    html = tpl.replace("/*__JOB__*/null", json.dumps(job, ensure_ascii=False).replace("</", "<\\/")).replace("__TOTAL__", str(total))
    out_dir = Path(out_dir)
    (out_dir / "index.html").write_text(html, encoding="utf-8")
    if job.get("ass"):
        (HERE / "subs.ass").write_text(job["ass"], encoding="utf-8")
    return out_dir / "index.html", total


if __name__ == "__main__":
    job = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    p, t = build(job, Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "render")
    print("[OK] %s (%s초 · %d장면)" % (p, t, len(job["scenes"])))
