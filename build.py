# -*- coding: utf-8 -*-
"""job.json(봇이 보낸 장면 데이터) → render/index.html + subs.ass   [hf-1.1]

사용: python build.py job.json            (기본 출력: render/index.html, subs.ass)
job = {"job_id", "tag", "date", "total", "size":[가로,세로](없으면 1080x1920),
       "scenes": [{start, dur, chip, t1, t2, big:{text,color,desc}|null, body:{type,...}}], "ass": "..."}
렌더: cd render && npx --yes hyperframes@0.8.208 render

[hf-1.1] 가로(1920x1080) 지원
  · job.size 로 화면 크기를 받는다. 없으면 예전처럼 1080x1920 세로.
  · 디자인은 '본문 1360px 높이' 기준 그대로 두고, zoom 으로 실제 크기에 맞춘다
    → 글자·여백 px 값을 하나도 안 고쳐도 비율이 유지된다.
  · 가로에서는 머리말(칩·제목·큰 숫자)을 왼쪽, 본문을 오른쪽에 두는 2단으로 바뀐다.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent

DESIGN_H = 1360            # 디자인 기준 본문 높이(px) — 세로 1920 - 자막 560
SUB_PORTRAIT = 560         # 자막 자리(실제 px)
SUB_LANDSCAPE = 230


def _size(job):
    s = job.get("size") or [job.get("width") or 1080, job.get("height") or 1920]
    return int(s[0]), int(s[1])


def build(job, out_dir=HERE / "render"):
    total = round(float(job["total"]), 3)
    W, H = _size(job)
    land = W > H
    sub = SUB_LANDSCAPE if land else SUB_PORTRAIT
    z = round((H - sub) / float(DESIGN_H), 4)          # 세로 1080x1920 이면 정확히 1.0
    tpl = (HERE / "engine.html").read_text(encoding="utf-8")
    html = (tpl
            .replace("/*__JOB__*/null", json.dumps(job, ensure_ascii=False).replace("</", "<\\/"))
            .replace("__TOTAL__", str(total))
            .replace("__W__", str(W)).replace("__H__", str(H))
            .replace("__Z__", str(z))
            .replace("__ROOTW__", str(round(W / z))).replace("__ROOTH__", str(round(H / z)))
            .replace("__RES__", "landscape" if land else "portrait")
            .replace("__MODE__", "landscape" if land else "portrait"))
    out_dir = Path(out_dir)
    (out_dir / "index.html").write_text(html, encoding="utf-8")
    if job.get("ass"):
        (HERE / "subs.ass").write_text(job["ass"], encoding="utf-8")
    return out_dir / "index.html", total, (W, H, z)


if __name__ == "__main__":
    job = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    p, t, (W, H, z) = build(job, Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "render")
    print("[OK] %s (%s초 · %d장면 · %dx%d · zoom %.4f)" % (p, t, len(job["scenes"]), W, H, z))
