def generate_api_lib_code() -> str:
    # Plain string — ${...} below is TypeScript template literal syntax, not Python substitution.
    return """\
export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8010"

export async function listItems<T>(resource: string): Promise<T[]> {
  const res = await fetch(`${API_BASE_URL}/api/v1/${resource}/`)
  if (!res.ok) throw new Error(`listItems ${resource} failed: ${res.status}`)
  return res.json() as Promise<T[]>
}

export async function getItem<T>(resource: string, id: number): Promise<T> {
  const res = await fetch(`${API_BASE_URL}/api/v1/${resource}/${id}`)
  if (!res.ok) throw new Error(`getItem ${resource}/${id} failed: ${res.status}`)
  return res.json() as Promise<T>
}

export async function createItem<TInput, TOutput>(
  resource: string,
  data: TInput,
): Promise<TOutput> {
  const res = await fetch(`${API_BASE_URL}/api/v1/${resource}/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  })
  if (!res.ok) throw new Error(`createItem ${resource} failed: ${res.status}`)
  return res.json() as Promise<TOutput>
}

export async function updateItem<TInput, TOutput>(
  resource: string,
  id: number,
  data: TInput,
): Promise<TOutput> {
  const res = await fetch(`${API_BASE_URL}/api/v1/${resource}/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  })
  if (!res.ok) throw new Error(`updateItem ${resource}/${id} failed: ${res.status}`)
  return res.json() as Promise<TOutput>
}

export async function deleteItem(resource: string, id: number): Promise<void> {
  const res = await fetch(`${API_BASE_URL}/api/v1/${resource}/${id}`, {
    method: "DELETE",
  })
  if (!res.ok) throw new Error(`deleteItem ${resource}/${id} failed: ${res.status}`)
}
"""
