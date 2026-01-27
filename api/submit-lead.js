import { Resend } from "resend";

export default async function handler(req, res) {
  try {
    return res.status(200).json({
      method: req.method,
      body: req.body,
      envKeyExists: !!process.env.RESEND_API_KEY,
    });
  } catch (err) {
    return res.status(500).json({
      error: err.message,
      stack: err.stack,
    });
  }
}
