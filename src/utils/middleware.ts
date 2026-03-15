import { validateToken } from "./auth";
import { sanitizeInput } from "./helpers";

export function authMiddleware(req: { headers: { authorization?: string } }) {
  const token = sanitizeInput(req.headers.authorization ?? "");
  if (!validateToken(token)) throw new Error("Unauthorized");
  return { authenticated: true };
}
