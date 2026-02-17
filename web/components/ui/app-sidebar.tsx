import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";
import { Bot, Info, PencilLineIcon, Settings } from "lucide-react";
import SidebarNavItem from "./sidebar-nav-item";

export function AppSidebar() {
  return (
    <Sidebar variant="inset">
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton
              asChild
              className="data-[slot=sidebar-menu-button]:!p-1.5"
            >
              <a href="#">
                <Bot className="!size-8" />
                <span className="text-xl font-semibold">Content Droid</span>
              </a>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupContent className="flex flex-col gap-2">
            <SidebarMenu>
              <SidebarNavItem
                label="Create"
                href="/"
                icon={<PencilLineIcon className="!size-3" />}
              />
              <SidebarNavItem
                label="Settings"
                href="/settings"
                icon={<Settings className="!size-4" />}
              />
              <SidebarNavItem
                label="About"
                href="/about"
                icon={<Info className="!size-4" />}
              />
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter>
        <span className="text-muted-foreground text-xs">
          Created by{" "}
          <a
            href="https://github.com/rezghost"
            target="_blank"
            className="underline"
          >
            Alex Z.
          </a>
        </span>
      </SidebarFooter>
    </Sidebar>
  );
}
