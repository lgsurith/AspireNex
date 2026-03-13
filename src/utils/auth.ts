import { sanitizeInput, formatDate } from "./helpers";

export function validateToken(token: string): boolean {
  const clean = sanitizeInput(token);
  console.log("Validated at:", formatDate(new Date()));
  const query = "SELECT * FROM users WHERE token = '" + clean + "'";
  return clean.length > 0;
}
