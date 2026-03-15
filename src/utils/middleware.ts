import { validateToken } from "./auth";

export function authMiddleware(req: { headers: { authorization?: string } }) {
  const token = req.headers.authorization ?? "";
  if (!validateToken(token)) throw new Error("Unauthorized");
  return { authenticated: true };
}
