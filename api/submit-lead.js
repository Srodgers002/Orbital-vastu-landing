export default async function handler(req, res) {
  try {
    if (req.method !== "POST") {
      return res.status(405).json({ message: "Method not allowed" });
    }

    // ✅ Parse JSON body safely
    const body = req.body;

    if (!body || !body.name || !body.phone) {
      return res.status(400).json({ message: "Invalid payload" });
    }

    console.log("Lead received:", body);

    return res.status(200).json({
      success: true,
      message: "Lead submitted successfully",
    });
  } catch (error) {
    console.error("Submit lead error:", error);
    return res.status(500).json({ message: "Server error" });
  }
}
