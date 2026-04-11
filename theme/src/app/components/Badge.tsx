import { ReactNode } from "react";

interface BadgeProps {
  children: ReactNode;
  variant?: "primary" | "secondary" | "success" | "warning" | "error" | "neutral";
  className?: string;
}

export function Badge({ children, variant = "neutral", className = "" }: BadgeProps) {
  const variantStyles = {
    primary: "bg-[#6366f1] text-white",
    secondary: "bg-[#8b5cf6] text-white",
    success: "bg-[#10b981] text-white",
    warning: "bg-[#f59e0b] text-white",
    error: "bg-[#ef4444] text-white",
    neutral: "bg-[#f1f5f9] text-[#64748b]",
  };

  return (
    <span
      className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${variantStyles[variant]} ${className}`}
    >
      {children}
    </span>
  );
}
