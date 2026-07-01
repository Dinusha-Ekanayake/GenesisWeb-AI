def pluralize(name: str) -> str:
    lower = name.lower()
    if lower.endswith('y') and len(lower) > 1 and lower[-2] not in 'aeiou':
        return lower[:-1] + 'ies'
    if lower.endswith('s') or lower.endswith('x') or lower.endswith('z'):
        return lower + 'es'
    return lower + 's'


def sa_type(raw: str) -> str:
    base = raw.rstrip("?")
    return {"string": "String", "integer": "Integer", "number": "Float", "boolean": "Boolean"}.get(base, "String")


def generate_models_code(entities) -> str:
    lines = [
        "from sqlalchemy import Column, Integer, String, Float, Boolean",
        "from .database import Base",
        "",
        "",
    ]
    for table in entities:
        name = table.name
        plural = pluralize(name)
        columns = table.columns or {}
        lines += [f"class {name}(Base):", f'    __tablename__ = "{plural}"', ""]
        lines.append("    id = Column(Integer, primary_key=True, index=True)")
        if columns:
            for field_name, raw_type in columns.items():
                col_type = sa_type(raw_type)
                nullable = raw_type.endswith("?")
                lines.append(f"    {field_name} = Column({col_type}, nullable={nullable})")
        else:
            lines.append("    name = Column(String, nullable=False)")
        lines.append("")
    return "\n".join(lines)
