import { useEffect, useRef } from 'react';

interface Detection {
  class_id: number;
  class_name: string;
  confidence: number;
  bbox: {
    x1: number;
    y1: number;
    x2: number;
    y2: number;
  };
}

interface DetectionCanvasProps {
  imageUrl: string;
  detections: Detection[];
  imageSize: {
    width: number;
    height: number;
  };
}

// クラス名から一貫性のある色を生成（HSL色空間で視認性確保）
function generateColor(className: string): string {
  // 文字列からハッシュ値を生成
  let hash = 0;
  for (let i = 0; i < className.length; i++) {
    hash = className.charCodeAt(i) + ((hash << 5) - hash);
  }
  
  // 色相（Hue）: 0-360度
  const hue = Math.abs(hash % 360);
  
  // 彩度（Saturation）: 70-90% で鮮やかに
  const saturation = 70 + (Math.abs(hash) % 20);
  
  // 明度（Lightness）: 45-65% で視認性確保
  const lightness = 45 + (Math.abs(hash >> 8) % 20);
  
  return `hsl(${hue}, ${saturation}%, ${lightness}%)`;
}

export function DetectionCanvas({ imageUrl, detections, imageSize }: DetectionCanvasProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const img = new Image();
    img.src = imageUrl;

    img.onload = () => {
      // バックエンドから返された元画像サイズを使用
      const originalWidth = imageSize.width;
      const originalHeight = imageSize.height;

      // 表示サイズを計算（max-h-96 = 384px、アスペクト比維持）
      const maxHeight = 384;
      let displayWidth = originalWidth;
      let displayHeight = originalHeight;

      if (displayHeight > maxHeight) {
        const ratio = maxHeight / displayHeight;
        displayHeight = maxHeight;
        displayWidth = originalWidth * ratio;
      }

      // Canvasサイズを表示サイズに設定
      canvas.width = displayWidth;
      canvas.height = displayHeight;

      // 画像を描画
      ctx.drawImage(img, 0, 0, displayWidth, displayHeight);

      // バウンディングボックス描画（正規化座標 → 表示座標）
      detections.forEach((detection) => {
        const { bbox, confidence, class_name } = detection;
        
        // 正規化座標を元画像サイズに戻してから表示サイズに変換
        const x1 = bbox.x1 * displayWidth;
        const y1 = bbox.y1 * displayHeight;
        const x2 = bbox.x2 * displayWidth;
        const y2 = bbox.y2 * displayHeight;
        const width = x2 - x1;
        const height = y2 - y1;

        // 色生成
        const color = generateColor(class_name);

        // ボックス描画
        ctx.strokeStyle = color;
        ctx.lineWidth = 3;
        ctx.strokeRect(x1, y1, width, height);

        // 背景付きラベル（信頼度のみ）
        const label = `${(confidence * 100).toFixed(1)}%`;
        ctx.font = 'bold 14px sans-serif';
        const textMetrics = ctx.measureText(label);
        const textHeight = 14;
        const padding = 4;

        // ラベル背景
        ctx.fillStyle = color;
        ctx.fillRect(
          x1,
          y1 - textHeight - padding * 2,
          textMetrics.width + padding * 2,
          textHeight + padding * 2
        );

        // ラベルテキスト
        ctx.fillStyle = 'white';
        ctx.fillText(label, x1 + padding, y1 - padding - 2);
      });
    };
  }, [imageUrl, detections, imageSize]);

  return (
    <canvas
      ref={canvasRef}
      className="max-w-full rounded-lg shadow-lg mx-auto"
    />
  );
}
