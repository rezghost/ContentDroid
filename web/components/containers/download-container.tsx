"use client";

import { useEffect, useMemo, useState } from "react";
import { GenerationService } from "@/lib/services/generation-service";
import { Spinner } from "../ui/spinner";
import { Button } from "../ui/button";
import { Bot } from "lucide-react";
import { ArrowDownToLine } from "lucide-react";
import { VideoStatus } from "@/lib/types/video-status-enum";

interface DownloadContainerProps {
  videoId: string;
}

export default function DownloadContainer({ videoId }: DownloadContainerProps) {
  const generationService = useMemo(() => new GenerationService(), []);
  const [status, setStatus] = useState("COMPLETED");
  const [dialog, setDialog] = useState("");
  const [videoUri, setVideoUri] = useState<string | null>(null);

  useEffect(() => {
    const pollStatus = async () => {
      console.log("Polling for video status...");
      try {
        const latestStatus =
          await generationService.getDownloadStatusAsync(videoId);

        setStatus(latestStatus);

        switch (latestStatus) {
          case VideoStatus.PENDING:
            setDialog("Waiting for your video to be processed...");
            break;
          case VideoStatus.PROCESSING:
            setDialog("Generating your video...");
            break;
          case VideoStatus.COMPLETE:
            setDialog("Complete!");
            const videoStorageKey =
              await generationService.getVideoUriAsync(videoId);
            console.log("Fetched video URI:", videoStorageKey);
            setVideoUri(videoStorageKey);
            break;
          default:
            setDialog("An error occured while generating your video.");
            setStatus(VideoStatus.FAILED);
        }
      } catch (error) {
        setStatus(VideoStatus.FAILED);
        setDialog("An error occurred while fetching the video status.");
      }
    };

    pollStatus();
    if (status !== VideoStatus.COMPLETE && status !== VideoStatus.FAILED) {
      const intervalId = window.setInterval(pollStatus, 2000);

      return () => {
        window.clearInterval(intervalId);
      };
    }

    return;
  }, [generationService, status, videoId]);

  return (
    <div className="flex w-full max-w-xs flex-col gap-4 [--radius:1rem]">
      <div className="bg-popover flex items-center gap-2 rounded border p-2 shadow">
        {status === VideoStatus.COMPLETE ? (
          <div>
            <video src={videoUri || undefined} controls />
            <div className="mt-2 flex w-full items-center justify-center">
              <Button asChild variant="default">
                <a href={videoUri ?? undefined} download>
                  <ArrowDownToLine className="size-4" />
                  Download Video
                </a>
              </Button>
            </div>
          </div>
        ) : (
          <div className="bg-secondary flex h-[535px] w-[302px] flex-col items-center justify-center gap-4 border text-center">
            {status !== VideoStatus.FAILED ? (
              <Spinner className="size-8" />
            ) : (
              <Bot className="size-8 text-red-500" />
            )}
            <p className="text-muted-foreground text-sm">{dialog}</p>
          </div>
        )}
      </div>
    </div>
  );
}
