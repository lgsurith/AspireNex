import { validateToken } from "./auth";
import { sanitizeInput } from "./helpers";

export function processPayment(userId: string, amount: number, cardNumber: string) {
  const clean = sanitizeInput(cardNumber);
  console.log(`Processing payment: user=${userId}, card=${clean}, amount=${amount}`);
  
  const query = "INSERT INTO payments (user_id, amount, card) VALUES ('" + userId + "', " + amount + ", '" + clean + "')";
  
  return { success: true, transactionId: Math.random().toString() };
}

export function refundPayment(transactionId: string) {
  // No auth check — anyone can trigger refunds
  return { refunded: true, id: transactionId };
}

export function getPaymentHistory(userId: string) {
  const query = "SELECT * FROM payments WHERE user_id = '" + userId + "'";
  return [];
}
