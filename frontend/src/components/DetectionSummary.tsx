import type { Detection } from '../types/detection';
import { generateColor } from './DetectionCanvas';

interface DetectionSummaryProps {
  detections: Detection[];
}

interface GroupedDetection {
  class_name: string;
  count: number;
  maxConfidence: number;
  color: string;
}

function groupDetections(detections: Detection[]): GroupedDetection[] {
  const groups = new Map<string, { count: number; maxConfidence: number }>();

  detections.forEach((d) => {
    const existing = groups.get(d.class_name);
    if (existing) {
      existing.count++;
      existing.maxConfidence = Math.max(existing.maxConfidence, d.confidence);
    } else {
      groups.set(d.class_name, {
        count: 1,
        maxConfidence: d.confidence,
      });
    }
  });

  return Array.from(groups.entries())
    .map(([class_name, data]) => ({
      class_name,
      count: data.count,
      maxConfidence: data.maxConfidence,
      color: generateColor(class_name),
    }))
    .sort((a, b) => b.maxConfidence - a.maxConfidence);
}

export function DetectionSummary({ detections }: DetectionSummaryProps) {
  if (detections.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500 dark:text-gray-400">
        検出されたオブジェクトはありません
      </div>
    );
  }

  const grouped = groupDetections(detections);

  return (
    <div className="space-y-3">
      {grouped.map(({ class_name, count, maxConfidence, color }) => (
        <div
          key={class_name}
          className="flex items-center gap-4 p-4 bg-white dark:bg-gray-800 rounded-xl shadow-sm"
        >
          <div
            className="w-3 h-3 rounded-full flex-shrink-0"
            style={{ backgroundColor: color }}
          />

          <div className="flex-1 min-w-0">
            <span className="font-medium text-gray-900 dark:text-white">
              {class_name}
            </span>
            <span className="ml-2 text-sm text-gray-500 dark:text-gray-400">
              ({count})
            </span>
          </div>

          <div className="w-24 h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
            <div
              className="h-full rounded-full transition-all duration-300"
              style={{
                width: `${maxConfidence * 100}%`,
                backgroundColor: color,
              }}
            />
          </div>

          <span className="text-sm font-mono text-gray-600 dark:text-gray-400 w-12 text-right">
            {(maxConfidence * 100).toFixed(0)}%
          </span>
        </div>
      ))}
    </div>
  );
}
