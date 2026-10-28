# hf-render — 증시한스푼 브리핑 화면 렌더 (HyperFrames · GitHub Actions)

봇(VM, `hf_video.py`)이 장면 데이터를 보내면 이 저장소의 Actions 가 애니메이션 화면 + 자막을 무음 MP4 로 만든다.
음성·배경음 합치기와 텔레그램·유튜브는 봇이 한다. 이 저장소에는 비밀 정보가 없다(공개 저장소).

## 구성
- `engine.html` — 장면 엔진 (블록: bars · tiles · card(s) · gauges · line). 데이터는 HTML 안에 JSON 으로 박힘(렌더 중 네트워크 없음)
- `build.py` — `job.json` → `render/index.html` + `subs.ass`
- `render/` — HyperFrames 프로젝트(Pretendard 글꼴·GSAP 내장, hyperframes@0.8.208 고정)
- `.github/workflows/render.yml` — `repository_dispatch(render)` 로 실행, 결과 artifact `video-<job_id>` (1일 보관)
- `samples/sample_job.json` — 수동 시험용(10/26 장후 브리핑 모의 데이터)

## 처음 한 번
1. GitHub 에 **공개** 저장소 `hf-render` 만들기 → 이 폴더 내용을 그대로 올리기 (`_test_bundle.tgz` 는 .gitignore 로 빠짐)
2. 저장소 Actions 탭 → render → **Run workflow** (수동 시험) → 완료 후 artifact `video-manual` 내려받아 확인
3. 토큰: GitHub → Settings → Developer settings → Fine-grained tokens → 새 토큰
   - Repository access: **hf-render 하나만**
   - Permissions: **Contents: Read and write**(작업 시작용), **Actions: Read**(결과 내려받기)
4. VM `~/stock-bot/.env` 에 추가 (채팅에 토큰을 붙이지 말 것)
   ```
   VIDEO_ENGINE=hf
   HF_REPO=<계정>/hf-render
   HF_TOKEN=<토큰>
   HF_TIMEOUT=900
   ```
5. 봇 재시작 → '장전 승인' / '리포트영상 승인' / '브리핑영상 승인' 때 자동 사용. 실패하면 기존 화면으로 자동 복귀.
   끄기: `VIDEO_ENGINE=mpl`

## PC 에서 미리 보기
```
python build.py samples\sample_job.json
cd render
npx --yes hyperframes@0.8.208 snapshot --at 3,10,23
npx --yes hyperframes@0.8.208 render
```
