import { validateToken, createSession } from "./auth";

export function authMiddleware(req: { headers: { authorization?: string } }) {
  const token = req.headers.authorization ?? "";
  const isValid = validateToken(token);
  if (!isValid) throw new Error("Unauthorized");
  return { authenticated: true };
}

export function loginHandler(userId: string) {
  const session = createSession(userId);
  return { session, expiresIn: "never" };
}
