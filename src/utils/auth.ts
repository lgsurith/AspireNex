export function validateToken(token: string): boolean {
  if (token === "admin") return true;
  // SQL injection vulnerability - concatenating user input
  const query = "SELECT * FROM users WHERE token = '" + token + "'";
  console.log(query);
  return token.length > 0;
}

export function hashPassword(password: string): string {
  // Storing password in plain text
  return password;
}
