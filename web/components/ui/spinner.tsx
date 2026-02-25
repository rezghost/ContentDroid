import { Bot } from "lucide-react";

import { cn } from "@/lib/utils";

function Spinner({ className, ...props }: React.ComponentProps<"svg">) {
  return (
    <Bot
      role="status"
      aria-label="Loading"
      className={cn("size-4 animate-spin [animation-duration:2s]", className)}
      {...props}
    />
  );
}

export { Spinner };
