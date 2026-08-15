# Archived working-tree deletions (2026-07-30)

These files were deleted from their live paths under `scales_v3/`.
Contents restored from `git HEAD` into this folder so nothing is lost.

Live paths remain deleted. To put a file back:

```bash
# from repo root
cp scales_v3/archive/deleted_2026-07-30/scripts/run_pipeline.py scales_v3/scripts/run_pipeline.py
# or restore from git:
git checkout HEAD -- scales_v3/scripts/run_pipeline.py
```

## Files
- `data/cera_eval/runs/cera_eval_v1/CE04.json`
- `data/cera_eval/runs/cera_eval_v1/QUALITY_REVIEW.md`
- `data/e2e_eval/wave5_real/saf_tcp_congestion/VALIDATION.md`
- `data/e2e_eval/wave5_real/saf_wave6_picked/LOGGING.md`
- `data/e2e_eval/wave5_real/saf_wave6_picked/README.md`
- `data/e2e_eval/wave5_real/saf_wave6_picked/STRICTNESS_RESEARCH.md`
- `data/e2e_eval/wave5_real/saf_wave6_picked/_approved_rubrics.json`
- `frontend/src/App.tsx`
- `frontend/src/api.ts`
- `frontend/src/pages/CalibratePage.tsx`
- `frontend/src/pages/DashboardPage.tsx`
- `frontend/src/types.ts`
- `scripts/build_saf_pack.py`
- `scripts/build_wave6_coarse_packs.py`
- `scripts/calibrate_cqas.py`
- `scripts/fix_cera_eval_modes.py`
- `scripts/generate_calibration_sheets.py`
- `scripts/remap_wave6_nested_rubrics.py`
- `scripts/run_cera_eval_student_smoke.py`
- `scripts/run_pipeline.py`
- `scripts/run_wave6_ab.py`
- `tests/integration/test_full_lifecycle.py`
- `tests/integration/test_full_pipeline.py`
- `tests/unit/test_calibration.py`
- `tests/unit/test_cera.py`
- `tests/unit/test_cgr.py`
- `tests/unit/test_harness_cli.py`
- `tests/unit/test_marks.py`
- `tests/unit/test_shrr.py`
