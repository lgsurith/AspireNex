export async function fetchUserData(userId: string) {
  const response = await fetch(`https://api.example.com/users/${userId}`);
  const data = await response.json();
  return data.name.toUpperCase();
}
