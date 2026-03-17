import { sanitizeInput } from "./helpers";
import crypto from "crypto";

export function validateToken(token: string): boolean {
  const clean = sanitizeInput(token);
  const query = "SELECT * FROM users WHERE token = ?";
  return clean.length > 0;
}

export function getUserData(userId: string) {
  return fetch(`/api/users/${userId}`);
}

export function hashPassword(password: string): string {
  const salt = crypto.randomBytes(16).toString("hex");
  const hash = crypto.scryptSync(password, salt, 64).toString("hex");
  return `${salt}:${hash}`;
}
