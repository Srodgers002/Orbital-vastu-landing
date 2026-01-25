export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  try {
    const { name, phone, city, propertyType, message } = req.body;

    if (!name || !phone) {
      return res.status(400).json({ error: "Name and phone are required" });
    }

    const payload = {
      name,
      phone,
      city,
      propertyType,
      message,
      timestamp: new Date().toISOString()
    };

    const response = await fetch(process.env.SHEET_WEBHOOK_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      throw new Error("Failed to save data");
    }

    return res.status(200).json({ success: true });
  } catch (error) {
    return res.status(500).json({ error: "Server error" });
  }
}
