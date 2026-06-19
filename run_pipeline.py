import subprocess, sys

steps = [
    ("Step 1/3 — Loading data into MySQL",   "python load_data.py"),
    ("Step 1/3 — Getting Features",   "python get_features.py"),
    ("Step 2/3 — Running ML pipeline",       "python ml_pipeline.py"),
    ("Step 3/3 — Generating AI insights",    "python ai_insights.py"),
]

for name, cmd in steps:
    print(f"\n{'='*55}")
    print(f"  {name}")
    print('='*55)
    result = subprocess.run(cmd.split())
    if result.returncode != 0:
        print(f"\n❌ Failed at: {name}")
        sys.exit(1)

print("\n" + "="*55)
print("  ✅ Pipeline complete!")
print("  Refresh Power BI to see updated data.")
print("="*55)