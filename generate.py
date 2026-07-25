from pathlib import Path

print("=========================================")
print("      ABACUS OPENAPI GENERATOR")
print("=========================================")

ROOT = Path(__file__).parent

INPUT = ROOT / "input" / "swagger.json"
OUTPUT = ROOT / "output"

OUTPUT.mkdir(exist_ok=True)

if not INPUT.exists():
    print("Metadata file not found.")
    print(f"Expected: {INPUT}")
    raise SystemExit(1)

print()
print("Metadata found.")
print(INPUT)

print()
print("Output folder:")
print(OUTPUT)

print()
print("Generator initialization complete.")
print("Next step: Metadata Parser")
