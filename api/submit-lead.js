import { Resend } from "resend";

export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  try {
    const { name, phone, city, propertyType, message } = req.body;

    if (!name || !phone || !city || !propertyType) {
      return res.status(400).json({ error: "Missing required fields" });
    }

    const resend = new Resend(process.env.RESEND_API_KEY);

    await resend.emails.send({
      from: "Orbital Vastu <onboarding@resend.dev>",
      to: ["iam.bharat.71@gmail.com"], // change later to client
      subject: "New Vastu Enquiry",
      html: `
        <h2>New Enquiry</h2>
        <p><b>Name:</b> ${name}</p>
        <p><b>Phone:</b> ${phone}</p>
        <p><b>City:</b> ${city}</p>
        <p><b>Property Type:</b> ${propertyType}</p>
        <p><b>Message:</b> ${message || "N/A"}</p>
      `,
    });

    return res.status(200).json({ success: true });
  } catch (error) {
    console.error("Submit lead error:", error);
    return res.status(500).json({
      error: "Failed to send email",
      details: error.message,
    });
  }
}
