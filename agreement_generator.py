from docxtpl import DocxTemplate
from datetime import date
from pathlib import Path

def generate_agreement(template_path: str, output_dir: str, ctx: dict) -> str:
    required = ["first_name", "last_name", "weekly_commitment", "flolabs_email", "tuition_fee", "monthly_fee", "teams"]
    missing = [k for k in required if not ctx.get(k)]
    if missing:
        raise ValueError(f"Missing required agreement fields: {', '.join(missing)}")

    tpl = DocxTemplate(template_path)

    today = date.today().isoformat()
    full_name = f"{ctx['first_name']} {ctx['last_name']}"
    render_ctx = {
        "first_name": ctx["first_name"],
        "last_name": ctx["last_name"],
        "participant_full_name": full_name,
        "weekly_commitment": ctx["weekly_commitment"],
        "flolabs_email": ctx["flolabs_email"],
        "tuition_fee": ctx["tuition_fee"],
        "monthly_fee": ctx["monthly_fee"],
        "teams": ", ".join(ctx["teams"]) if isinstance(ctx["teams"], list) else str(ctx["teams"]),
        "effective_date": ctx.get("effective_date", today),
    }

    tpl.render(render_ctx)

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    fname = f"Agreement_{ctx['last_name']}_{ctx['first_name']}_{today.replace('-','')}.docx"
    out_path = out_dir / fname
    tpl.save(str(out_path))
    return str(out_path)