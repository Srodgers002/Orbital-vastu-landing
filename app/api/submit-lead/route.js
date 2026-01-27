import { Resend } from "resend";

export async function POST(request) {
  try {
    const body = await request.json();
    const { name, phone, city, propertyType, message } = body;

    if (!name || !phone || !city || !propertyType) {
      return Response.json(
        { error: "Missing required fields" },
        { status: 400 }
      );
    }

    const resend = new Resend(process.env.RESEND_API_KEY);

    await resend.emails.send({
      from: "Orbital Vastu <onboarding@resend.dev>",
      to: ["iam.bharat.71@gmail.com"],
      subject: "New Vastu Enquiry",
      html: `
        <h2>New Enquiry</h2>
        <p><b>Name:</b> ${name}</p>
        <p><b>Phone:</b> ${phone}</p>
        <p><b>City:</b> ${city}</p>
        <p><b>Property:</b> ${propertyType}</p>
        <p><b>Message:</b> ${message || "N/A"}</p>
      `,
    });

    return Response.json({ success: true });

  } catch (error) {
    console.error("API ERROR:", error);

    return Response.json(
      { error: "Internal Server Error", details: error.message },
      { status: 500 }
    );
  }
}
