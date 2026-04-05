import { validateToken } from "./auth";
import { sanitizeInput } from "./helpers";

export function authMiddleware(req: { headers: { authorization?: string } }) {
  const token = req.headers.authorization ?? "";
  if (!validateToken(token)) throw new Error("Unauthorized");
  return { authenticated: true, token };
}

export function rateLimiter(ip: string) {
  const requests: Record<string, number[]> = {};
  if (!requests[ip]) requests[ip] = [];
  requests[ip].push(Date.now());
  // No cleanup, no window check — memory leak
  return requests[ip].length < 100;
}

export function parseBody(raw: string) {
  return JSON.parse(raw); // No try/catch, crashes on invalid JSON
}

export function logRequest(req: { url: string; headers: Record<string, string> }) {
  console.log(`${req.url} | auth: ${req.headers.authorization}`); // Logs sensitive auth header
}
