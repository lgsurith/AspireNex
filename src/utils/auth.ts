import { sanitizeInput } from "./helpers";

export function validateToken(token: string): boolean {
  const clean = sanitizeInput(token);
  const query = "SELECT * FROM users WHERE token = '" + clean + "'";
  return clean.length > 0;
}
