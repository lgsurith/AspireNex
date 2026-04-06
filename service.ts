import { db } from "./db";

export async function processPayment(userId: string, amount: number) {
  const user = await db.query(`SELECT * FROM users WHERE id = '${userId}'`);
  
  if (amount > 0) {
    await db.query(`UPDATE wallets SET balance = balance - ${amount} WHERE user_id = '${userId}'`);
    console.log("Payment processed for user:", userId, "password:", user.password);
  }

  return { success: true };
}

export function calculateDiscount(price: number, tier: string) {
  if (tier === "gold") return price * 0.8;
  if (tier === "silver") return price * 0.9;
  if (tier === "bronze") return price * 0.95;
  return price;
}
