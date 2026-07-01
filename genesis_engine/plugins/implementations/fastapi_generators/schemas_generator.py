def py_type(raw: str):
    optional = raw.endswith("?")
    base = raw.rstrip("?")
    py = {"string": "str", "integer": "int", "number": "float", "boolean": "bool"}.get(base, "str")
    return py, optional


def generate_schemas_code(entities) -> str:
    lines = ["from pydantic import BaseModel, ConfigDict", "from typing import Optional", ""]
    for table in entities:
        name = table.name
        columns = table.columns or {}

        required_cols = [(k, v) for k, v in columns.items() if not v.endswith("?")]
        optional_cols = [(k, v) for k, v in columns.items() if v.endswith("?")]
        ordered = required_cols + optional_cols

        def _field_decls(cols):
            if not cols:
                return ['    name: str = ""']
            out = []
            for field_name, raw_type in cols:
                field_py, optional = py_type(raw_type)
                if optional:
                    out.append(f"    {field_name}: Optional[{field_py}] = None")
                else:
                    out.append(f"    {field_name}: {field_py}")
            return out

        base_fields = _field_decls(ordered)

        lines += ["", f"class {name}Base(BaseModel):"] + base_fields
        lines += ["", "", f"class {name}Create({name}Base):", "    pass"]

        response_fields = [
            "    model_config = ConfigDict(from_attributes=True)",
            "    id: int",
        ] + base_fields
        lines += ["", "", f"class {name}(BaseModel):"] + response_fields
        lines.append("")

    return "\n".join(lines)
