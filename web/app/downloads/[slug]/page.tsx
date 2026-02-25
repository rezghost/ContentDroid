"use client";
import { use } from "react";
import DownloadContainer from "@/components/containers/download-container";

export default function Page({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = use(params);

  return (
    <div className="flex h-full flex-col items-center justify-center rounded-md">
      <DownloadContainer videoId={slug} />
    </div>
  );
}
