"use client";

import { usePathname } from "next/navigation";
import { SidebarMenuItem, SidebarMenuButton } from "./sidebar";

interface NavItemProps {
  label: string;
  href: string;
  icon: React.ReactNode;
}

export default function SidebarNavItem({ label, href, icon }: NavItemProps) {
  const pathname = usePathname();
  const isActive = pathname === href;

  return (
    <SidebarMenuItem>
      <SidebarMenuButton
        className={`text-primary hover:bg-primary hover:text-primary-foreground active:bg-primary active:text-primary-foreground min-w-8 duration-200 ease-linear ${isActive ? "bg-primary text-primary-foreground" : ""}`}
        asChild
      >
        <a href={href}>
          {icon}
          <span>{label}</span>
        </a>
      </SidebarMenuButton>
    </SidebarMenuItem>
  );
}
