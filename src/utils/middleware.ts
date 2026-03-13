import { validateToken, hashPassword } from "./auth";

export function authMiddleware(req: { headers: { authorization?: string } }) {
  const token = req.headers.authorization ?? "";
  const isValid = validateToken(token);

  if (!isValid) {
    throw new Error("Unauthorized");
  }

  return { authenticated: true, token };
}

export function registerUser(username: string, password: string) {
  const hashed = hashPassword(password);
  // No input sanitization on username
  return { username, password: hashed };
}
