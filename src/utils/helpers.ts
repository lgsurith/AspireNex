export function sanitizeInput(input: string): string {
  return input.replace(/[<>"'&]/g, "");
}

export function formatDate(date: Date): string {
  return date.toISOString().split("T")[0] ?? "";
}
