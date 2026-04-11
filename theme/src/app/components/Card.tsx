import { ReactNode } from "react";

interface CardProps {
  children: ReactNode;
  className?: string;
  variant?: "default" | "gradient-border";
  gradientColor?: "blue" | "purple" | "green" | "yellow" | "sky";
}

export function Card({ children, className = "", variant = "default", gradientColor = "blue" }: CardProps) {
  const gradientColors = {
    blue: "before:bg-gradient-to-r before:from-[#6366f1] before:to-[#8b5cf6]",
    purple: "before:bg-gradient-to-r before:from-[#8b5cf6] before:to-[#a855f7]",
    green: "before:bg-gradient-to-r before:from-[#10b981] before:to-[#14b8a6]",
    yellow: "before:bg-gradient-to-r before:from-[#f59e0b] before:to-[#f97316]",
    sky: "before:bg-gradient-to-r before:from-[#0ea5e9] before:to-[#06b6d4]",
  };

  if (variant === "gradient-border") {
    return (
      <div className={`relative ${className}`}>
        <div
          className={`absolute inset-0 rounded-xl ${gradientColors[gradientColor]} before:absolute before:inset-0 before:rounded-xl p-[2px]`}
        >
          <div className="w-full h-full bg-white rounded-xl" />
        </div>
        <div className="relative bg-white rounded-xl p-6">{children}</div>
      </div>
    );
  }

  return (
    <div
      className={`bg-white rounded-xl p-6 border border-[#e2e8f0] hover:shadow-lg transition-shadow ${className}`}
    >
      {children}
    </div>
  );
}
