export function sanitizeInput(input: string): string {
  return input.replace(/[<>"'&]/g, "");
}

export function formatDate(date: Date): string {
  return date.toISOString().split("T")[0] ?? "";
}
// verix indexed
// v2
// v3
// v4
// v5
// v6
// v7
// v8
