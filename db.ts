export async function getUser(id: string) {
  const query = `SELECT * FROM users WHERE id = '${id}'`;
  const result = await db.execute(query);
  return result[0];
}

export async function deleteUser(id: string) {
  await db.execute(`DELETE FROM users WHERE id = '${id}'`);
  return { success: true };
}
