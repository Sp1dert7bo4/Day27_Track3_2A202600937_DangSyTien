import json
import sys

with open("submission.json") as f:
    d = json.load(f)

print("Valid JSON: YES")
print("prompt_safety present:", bool(d.get("prompt_safety")))

tools = list(d["tools"].keys())
print("Tools:", tools)
print("Tool count:", len(tools))

expected = {"send_user", "lakehouse_query", "lakehouse_write", "list_files",
            "search_content", "read_file", "write_file", "edit_file", "run_bash"}
print("All 9 tools present:", set(tools) == expected)

errors = []
for t in tools:
    rules = d["tools"][t]["rules"]
    actions = [r["action"] for r in rules]
    print(f"  {t}: {len(rules)} rules -> {actions}")
    for i, r in enumerate(rules):
        keys = set(r.keys())
        if keys != {"action", "condition"}:
            errors.append(f"{t} rule {i}: unexpected keys {keys}")
        if r["action"] not in ("HITL", "REJECT"):
            errors.append(f"{t} rule {i}: invalid action {r['action']}")
        if not r.get("condition"):
            errors.append(f"{t} rule {i}: empty condition")
        if r["action"] == "ALLOW":
            errors.append(f"{t} rule {i}: uses ALLOW (forbidden)")

if errors:
    print("\nERRORS:")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
else:
    print("\nAll validations passed!")
