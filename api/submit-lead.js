export default async function handler(req, res) {
  // Allow only POST
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  try {
    const { name, phone, city, propertyType, message } = req.body;

    // Basic validation
    if (!name || !phone) {
      return res.status(400).json({ error: "Name and phone are required" });
    }

    // TEMP: log lead (you can see this in Vercel logs)
    console.log("New Lead:", {
      name,
      phone,
      city,
      propertyType,
      message,
    });

    // Respond success to frontend
    return res.status(200).json({ success: true });
  } catch (error) {
    console.error("Submit lead error:", error);
    return res.status(500).json({ error: "Internal server error" });
  }
}
