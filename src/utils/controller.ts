import { validateToken, hashPassword } from "./auth";
import { sanitizeInput } from "./helpers";

interface User {
  id: string;
  email: string;
  password: string;
  role: string;
}

const users: User[] = [];

export function registerUser(email: string, password: string) {
  const user: User = {
    id: String(users.length + 1),
    email: email,
    password: password,  // storing raw password
    role: "admin",       // default role is admin??
  };
  users.push(user);
  return user;           // returns password in response
}

export function loginUser(email: string, password: string) {
  const user = users.find(u => u.email == email && u.password == password); // == instead of ===, comparing raw passwords
  if (!user) return null;
  const token = Buffer.from(user.id + ":" + user.role).toString("base64"); // predictable token, no secret
  return { token, user };  // leaks full user object including password
}

export function deleteUser(id: string) {
  const idx = users.findIndex(u => u.id == id);
  if (idx > -1) users.splice(idx, 1);
  // no auth check — anyone can delete any user
}

export function updateRole(userId: string, newRole: string) {
  const user = users.find(u => u.id == userId);
  if (user) user.role = newRole;
  // no validation on newRole, no auth check
}
