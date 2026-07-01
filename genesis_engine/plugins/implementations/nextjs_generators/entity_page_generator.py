from .types_generator import ts_type


def generate_entity_page_code(table, plural: str) -> str:
    name = table.name
    columns = table.columns or {}
    effective_columns = columns if columns else {"name": "string"}
    pascal_plural = plural[0].upper() + plural[1:]

    form_fields_parts = []
    for field_name, raw_type in effective_columns.items():
        field_ts, _ = ts_type(raw_type)
        if field_ts == "number":
            form_fields_parts.append(f'{field_name}: 0')
        elif field_ts == "boolean":
            form_fields_parts.append(f'{field_name}: false')
        else:
            form_fields_parts.append(f'{field_name}: ""')
    form_init_inner = ", ".join(form_fields_parts)

    edit_fields_parts = [f"{f}: item.{f}" for f in effective_columns.keys()]
    edit_form_inner = ", ".join(edit_fields_parts)

    all_fields = ["id"] + list(effective_columns.keys())
    th_row = "".join(f"<th>{f}</th>" for f in all_fields) + "<th>actions</th>"

    td_parts = []
    for f in all_fields:
        if f == "id":
            td_parts.append(f"<td>{{item.id}}</td>")
        else:
            raw = effective_columns.get(f, "string?")
            if raw.endswith("?"):
                td_parts.append(f"<td>{{item.{f} ?? ''}}</td>")
            else:
                td_parts.append(f"<td>{{item.{f}}}</td>")
    td_row = "".join(td_parts)

    input_lines = []
    for field_name, raw_type in effective_columns.items():
        field_ts, optional = ts_type(raw_type)
        req = "" if optional else " required"
        if field_ts == "boolean":
            input_lines.append(
                f'        <label><input type="checkbox" checked={{Boolean(form.{field_name})}} onChange={{(e) => setForm({{...form, {field_name}: e.target.checked}})}} />{{" "}}{field_name}</label>'
            )
        elif field_ts == "number":
            input_lines.append(
                f'        <input type="number" name="{field_name}" value={{form.{field_name} ?? 0}} onChange={{(e) => setForm({{...form, {field_name}: Number(e.target.value)}})}} placeholder="{field_name}"{req} />'
            )
        else:
            input_lines.append(
                f'        <input type="text" name="{field_name}" value={{form.{field_name} ?? ""}} onChange={{(e) => setForm({{...form, {field_name}: e.target.value}})}} placeholder="{field_name}"{req} />'
            )

    lines = [
        '"use client"',
        "",
        'import { useEffect, useState, FormEvent } from "react"',
        f'import {{ listItems, createItem, updateItem, deleteItem }} from "../../lib/api"',
        f'import type {{ {name}, {name}Create }} from "../../lib/types"',
        "",
        "",
        f"export default function {pascal_plural}Page() {{",
        f"  const [items, setItems] = useState<{name}[]>([])",
        "  const [loading, setLoading] = useState(true)",
        "  const [error, setError] = useState<string | null>(null)",
        f"  const [form, setForm] = useState<{name}Create>({{ {form_init_inner} }})",
        '  const [editingId, setEditingId] = useState<number | null>(null)',
        "",
        "  useEffect(() => {",
        f'    listItems<{name}>("{plural}")',
        "      .then(setItems)",
        "      .catch((e: Error) => setError(e.message))",
        "      .finally(() => setLoading(false))",
        "  }, [])",
        "",
        "  async function handleSubmit(e: FormEvent<HTMLFormElement>) {",
        "    e.preventDefault()",
        "    try {",
        "      if (editingId !== null) {",
        f'        const updated = await updateItem<{name}Create, {name}>("{plural}", editingId, form)',
        "        setItems((prev) => prev.map((i) => (i.id === editingId ? updated : i)))",
        "        setEditingId(null)",
        f"        setForm({{ {form_init_inner} }})",
        "      } else {",
        f'        const created = await createItem<{name}Create, {name}>("{plural}", form)',
        "        setItems((prev) => [...prev, created])",
        f"        setForm({{ {form_init_inner} }})",
        "      }",
        "    } catch (e: unknown) {",
        '      setError(e instanceof Error ? e.message : "Unknown error")',
        "    }",
        "  }",
        "",
        f"  async function handleDelete(id: number) {{",
        "    try {",
        f'      await deleteItem("{plural}", id)',
        "      setItems((prev) => prev.filter((i) => i.id !== id))",
        "    } catch (e: unknown) {",
        '      setError(e instanceof Error ? e.message : "Unknown error")',
        "    }",
        "  }",
        "",
        "  return (",
        "    <div>",
        f"      <h1>{pascal_plural}</h1>",
        "      {loading && <p>Loading...</p>}",
        '      {error && <p style={{ color: "red" }}>{error}</p>}',
        "      <form onSubmit={handleSubmit}>",
        *input_lines,
        '        <button type="submit">{editingId !== null ? "Save" : "Add"}</button>',
        f'        {{editingId !== null && <button type="button" onClick={{() => {{ setEditingId(null); setForm({{ {form_init_inner} }}) }}}}>Cancel</button>}}',
        "      </form>",
        "      <table>",
        "        <thead>",
        f"          <tr>{th_row}</tr>",
        "        </thead>",
        "        <tbody>",
        "          {items.map((item) => (",
        "            <tr key={item.id}>",
        f'              {td_row}<td><button onClick={{() => {{ setEditingId(item.id); setForm({{ {edit_form_inner} }}) }}}}>Edit</button><button onClick={{() => handleDelete(item.id)}}>Delete</button></td>',
        "            </tr>",
        "          ))}",
        "        </tbody>",
        "      </table>",
        "    </div>",
        "  )",
        "}",
        "",
    ]
    return "\n".join(lines)
