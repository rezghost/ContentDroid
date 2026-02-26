import { NextResponse } from "next/server";

export async function POST(request: Request) {
  const baseUrl = process.env.GENERATION_SERVICE_URL;
  if (!baseUrl) {
    return NextResponse.json(
      { error: "GENERATION_SERVICE_URL is not configured" },
      { status: 500 }
    );
  }

  const response = await fetch(`${baseUrl}/generate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: await request.text(),
    cache: "no-store",
  });

  return new NextResponse(await response.text(), {
    status: response.status,
    headers: {
      "Content-Type": response.headers.get("Content-Type") ?? "text/plain",
    },
  });
}
