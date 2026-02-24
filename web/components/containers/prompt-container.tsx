"use client";

import { Trash } from "lucide-react";
import { Button } from "../ui/button";
import { Textarea } from "../ui/textarea";
import { useState } from "react";
import { GenerationService } from "@/lib/services/generation-service";
import { redirect } from "next/dist/client/components/navigation";

export default function PromptContainer() {
  const MAX_CHARACTERS = 250;
  const [textAreaContent, setTextAreaContent] = useState("");
  const [characterCount, setCharacterCount] = useState(0);
  const generationService = new GenerationService();

  const handleInputChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setTextAreaContent(event.target.value);
    setCharacterCount(event.target.value.length);
  };

  const handleCancel = () => {
    setTextAreaContent("");
    setCharacterCount(0);
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    const formData = new FormData(event.target as HTMLFormElement);

    const formValues = {
      prompt: formData.get("prompt") as string,
    };

    const data = await generationService.generateVideoAsync(formValues.prompt);
    redirect(`/downloads/${data}`);
  };

  const reachedCharacterLimit = characterCount >= MAX_CHARACTERS;

  return (
    <form onSubmit={handleSubmit} className="mt-0.5 flex h-full w-1/2 flex-col">
      <Textarea
        name="prompt"
        value={textAreaContent}
        onChange={handleInputChange}
        maxLength={MAX_CHARACTERS}
        placeholder="Enter your prompt..."
      />
      <div className="flex flex-row items-end justify-end">
        <p
          className={`text-muted-foreground mt-0.5 px-1 text-xs ${
            reachedCharacterLimit ? "text-red-400" : ""
          }`}
        >
          {characterCount} / {MAX_CHARACTERS} characters
        </p>
      </div>
      <div className="mt-2 flex w-full flex-row items-end justify-between">
        <Button
          type="button"
          className="ml-2 cursor-pointer"
          variant="outline"
          onClick={handleCancel}
        >
          <Trash />
          Cancel
        </Button>
        <Button
          type="submit"
          disabled={reachedCharacterLimit}
          className="ml-2 cursor-pointer"
        >
          Submit
        </Button>
      </div>
    </form>
  );
}
