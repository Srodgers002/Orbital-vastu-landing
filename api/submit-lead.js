export default async function handler(req, res) {
  try {
    if (req.method !== "POST") {
      return res.status(405).json({ message: "Method not allowed" });
    }

    const { name, phone, city, propertyType, message } = req.body;

    if (!name || !phone || !city || !propertyType) {
      return res.status(400).json({ message: "Missing required fields" });
    }

    console.log("Lead received:", {
      name,
      phone,
      city,
      propertyType,
      message,
    });

    return res.status(200).json({ success: true });
  } catch (err) {
    console.error("Submit lead error:", err);
    return res.status(500).json({ message: "Server error" });
  }
}
