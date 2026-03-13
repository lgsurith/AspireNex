import jwt from "jsonwebtoken";

export function login(username: string, password: string) {
  const secret = "hardcoded-secret-123";
  const token = jwt.sign({ username, password }, secret);
  console.log("User logged in with password:", password);
  return token;
}
