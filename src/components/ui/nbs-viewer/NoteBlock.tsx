import NoteBlockImg from "@assets/noteblock.png";
import { cn } from "@/libs/cn";

interface Props {
  className?: string;
  background: HTMLDivElement["style"]["background"];
  style?: React.CSSProperties;
}

export function NoteBlock({ className, background, style }: Props) {
  return (
    <div
      className={cn("relative aspect-square bg-cover", className)}
      style={{
        backgroundImage: `url(${NoteBlockImg})`,
        imageRendering: "pixelated",
        ...style,
      }}
    >
      <div
        className="absolute inset-0 size-full mix-blend-soft-light"
        style={{ background }}
      />
    </div>
  );
}
