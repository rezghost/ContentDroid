import { NextResponse } from "next/server";

type RouteContext = {
  params: Promise<{ id: string }>;
};

export async function GET(_: Request, context: RouteContext) {
  const baseUrl = process.env.GENERATION_SERVICE_URL;
  if (!baseUrl) {
    return NextResponse.json(
      { error: "GENERATION_SERVICE_URL is not configured" },
      { status: 500 }
    );
  }

  const { id } = await context.params;
  const response = await fetch(`${baseUrl}/video/${encodeURIComponent(id)}`, {
    cache: "no-store",
  });

  return new NextResponse(await response.text(), {
    status: response.status,
    headers: {
      "Content-Type": response.headers.get("Content-Type") ?? "text/plain",
    },
  });
}
