def pluralize(name: str) -> str:
    lower = name.lower()
    if lower.endswith('y') and len(lower) > 1 and lower[-2] not in 'aeiou':
        return lower[:-1] + 'ies'
    if lower.endswith('s') or lower.endswith('x') or lower.endswith('z'):
        return lower + 'es'
    return lower + 's'


def ts_type(raw: str):
    optional = raw.endswith("?")
    base = raw.rstrip("?")
    ts = {"string": "string", "integer": "number", "number": "number", "boolean": "boolean"}.get(base, "string")
    return ts, optional


def generate_types_code(entities) -> str:
    lines = []
    for table in entities:
        name = table.name
        columns = table.columns or {}
        effective_columns = columns if columns else {"name": "string"}

        required_cols = [(k, v) for k, v in effective_columns.items() if not v.endswith("?")]
        optional_cols = [(k, v) for k, v in effective_columns.items() if v.endswith("?")]
        ordered = required_cols + optional_cols

        lines.append(f"export interface {name} {{")
        lines.append("  id: number")
        for field_name, raw_type in ordered:
            ts, optional = ts_type(raw_type)
            if optional:
                lines.append(f"  {field_name}?: {ts} | null")
            else:
                lines.append(f"  {field_name}: {ts}")
        lines.append("}")
        lines.append("")
        lines.append(f'export type {name}Create = Omit<{name}, "id">')
        lines.append("")
    return "\n".join(lines)
