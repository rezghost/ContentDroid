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
    <div>
      <DownloadContainer videoId={slug} />
    </div>
  );
}
