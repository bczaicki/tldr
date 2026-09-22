"""Print the single-turn prompt that simulates `/tldr [args]` after a real response."""
import re, sys
from common import DATA, samples, variant_path

variant, name = sys.argv[1], sys.argv[2]
args = samples()[name]["args"]
body = re.sub(r"^---\n.*?\n---\n", "", open(variant_path(variant)).read(), flags=re.S).strip()
if "$ARGUMENTS" in body:
    body = body.replace("$ARGUMENTS", args)
elif args:
    body += f"\n\nARGUMENTS: {args}"
user = open(f"{DATA}/corpus/{name}.user.md").read().strip()
response = open(f"{DATA}/corpus/{name}.assistant.md").read().strip()
print(f"""The following is the most recent exchange in this Claude Code session. Tool calls and their results from your turn are omitted; the text is exactly what you wrote to the user.

<previous_user_message>
{user}
</previous_user_message>

<your_previous_response>
{response}
</your_previous_response>

The user now runs `/tldr{(' ' + args) if args else ''}`, which expands to:

<command-name>/tldr</command-name>
{body}""")
