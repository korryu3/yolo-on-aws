import { useEffect, useRef } from 'react';
import type { Detection, ImageSize } from '../types/detection';

interface DetectionCanvasProps {
  imageUrl: string;
  detections: Detection[];
  imageSize: ImageSize;
  maxHeight?: number;
}

function generateColor(className: string): string {
  let hash = 0;
  for (let i = 0; i < className.length; i++) {
    hash = className.charCodeAt(i) + ((hash << 5) - hash);
  }

  const hue = Math.abs(hash % 360);
  const saturation = 70 + (Math.abs(hash) % 20);
  const lightness = 45 + (Math.abs(hash >> 8) % 20);

  return `hsl(${hue}, ${saturation}%, ${lightness}%)`;
}

export function DetectionCanvas({
  imageUrl,
  detections,
  imageSize,
  maxHeight = 600
}: DetectionCanvasProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const img = new Image();
    img.src = imageUrl;

    img.onload = () => {
      const originalWidth = imageSize.width;
      const originalHeight = imageSize.height;

      let displayWidth = originalWidth;
      let displayHeight = originalHeight;

      if (displayHeight > maxHeight) {
        const ratio = maxHeight / displayHeight;
        displayHeight = maxHeight;
        displayWidth = originalWidth * ratio;
      }

      canvas.width = displayWidth;
      canvas.height = displayHeight;

      ctx.drawImage(img, 0, 0, displayWidth, displayHeight);

      detections.forEach((detection) => {
        const { bbox, confidence, class_name } = detection;

        const x1 = bbox.x1 * displayWidth;
        const y1 = bbox.y1 * displayHeight;
        const x2 = bbox.x2 * displayWidth;
        const y2 = bbox.y2 * displayHeight;
        const width = x2 - x1;
        const height = y2 - y1;

        const color = generateColor(class_name);

        ctx.strokeStyle = color;
        ctx.lineWidth = 3;
        ctx.strokeRect(x1, y1, width, height);

        const label = `${class_name} ${(confidence * 100).toFixed(0)}%`;
        ctx.font = 'bold 16px system-ui, sans-serif';
        const textMetrics = ctx.measureText(label);
        const textHeight = 18;
        const padding = 6;

        ctx.fillStyle = color;
        ctx.fillRect(
          x1,
          y1 - textHeight - padding * 2,
          textMetrics.width + padding * 2,
          textHeight + padding * 2
        );

        ctx.fillStyle = 'white';
        ctx.shadowColor = 'rgba(0, 0, 0, 0.3)';
        ctx.shadowBlur = 2;
        ctx.fillText(label, x1 + padding, y1 - padding - 2);
        ctx.shadowBlur = 0;
      });
    };
  }, [imageUrl, detections, imageSize, maxHeight]);

  return (
    <canvas
      ref={canvasRef}
      className="max-w-full rounded-2xl shadow-lg mx-auto"
    />
  );
}

export { generateColor };
