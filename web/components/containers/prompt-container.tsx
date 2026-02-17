"use client";

import { Trash } from "lucide-react";
import { Button } from "../ui/button";
import { Textarea } from "../ui/textarea";
import { useState } from "react";

export default function PromptContainer() {
  const MAX_CHARACTERS = 250;
  const [textAreaContent, setTextAreaContent] = useState("");
  const [characterCount, setCharacterCount] = useState(0);

  const handleInputChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setTextAreaContent(event.target.value);
    setCharacterCount(event.target.value.length);
  };

  const handleCancel = () => {
    setTextAreaContent("");
    setCharacterCount(0);
  };

  const reachedCharacterLimit = characterCount >= MAX_CHARACTERS;

  return (
    <div className="flex h-full w-3/4 flex-col items-center justify-center rounded-md bg-zinc-100 p-4 shadow-md">
      <Textarea
        placeholder="Enter your prompt here..."
        onChange={handleInputChange}
        className="bg-background"
        value={textAreaContent}
        rows={10}
        aria-invalid={reachedCharacterLimit}
      />
      <div className="mt-0.5 flex w-full flex-row items-end justify-end">
        <p
          className={`text-muted-foreground px-1 text-xs ${reachedCharacterLimit ? "text-red-400" : ""}`}
        >
          {characterCount} / {MAX_CHARACTERS} characters
        </p>
      </div>
      <div className="mt-2 flex w-full flex-row items-end justify-between">
        <Button
          className="ml-2 cursor-pointer"
          variant="outline"
          onClick={handleCancel}
        >
          <Trash /> Cancel
        </Button>
        <Button
          disabled={reachedCharacterLimit}
          className="ml-2 cursor-pointer"
        >
          Submit
        </Button>
      </div>
    </div>
  );
}
