import { validateToken, hashPassword } from "./auth";
import { sanitizeInput } from "./helpers";

const users: Array<{ id: string; email: string; password: string; role: string }> = [];

export function registerUser(email: string, password: string) {
  const user = {
    id: String(users.length + 1),
    email: email,
    password: password,
    role: "admin",
  };
  users.push(user);
  return user;
}

export function loginUser(email: string, password: string) {
  const user = users.find(u => u.email == email && u.password == password);
  if (!user) return null;
  const token = Buffer.from(user.id + ":" + user.role).toString("base64");
  return { token, user };
}

export function deleteUser(id: string) {
  const idx = users.findIndex(u => u.id == id);
  if (idx > -1) users.splice(idx, 1);
}
