"use client";

import { useEffect, useMemo, useState } from "react";
import { GenerationService } from "@/lib/services/generation-service";

interface DownloadContainerProps {
  videoId: string;
}

export default function DownloadContainer({ videoId }: DownloadContainerProps) {
  const generationService = useMemo(() => new GenerationService(), []);
  console.log("DownloadContainer initialized with videoId:", videoId);
  const [status, setStatus] = useState("PENDING");

  useEffect(() => {
    const pollStatus = async () => {
      try {
        const latestStatus =
          await generationService.getDownloadStatusAsync(videoId);
        setStatus(latestStatus);
      } catch (error) {
        setStatus("Error: cannot find video");
      }
    };

    pollStatus();
    const intervalId = window.setInterval(pollStatus, 2000);

    return () => {
      window.clearInterval(intervalId);
    };
  }, [generationService, videoId]);

  return <p>{status}</p>;
}
