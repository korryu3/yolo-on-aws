import { useDetection } from '../hooks/useDetection';
import { DropZone } from './DropZone';
import { DetectionCanvas } from './DetectionCanvas';
import { DetectionSummary } from './DetectionSummary';
import { LoadingSpinner } from './LoadingSpinner';

export function ImageUpload() {
  const {
    previewUrl,
    result,
    error,
    isLoading,
    confThreshold,
    setConfThreshold,
    selectFile,
    detect,
    reset,
  } = useDetection();

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <header className="text-center mb-12">
        <h1 className="text-3xl font-light tracking-tight text-gray-900 dark:text-white">
          YOLO 物体検出
        </h1>
      </header>

      {!result && (
        <section className="space-y-8">
          <DropZone
            onFileSelect={selectFile}
            previewUrl={previewUrl}
            disabled={isLoading}
          />

          <div className="max-w-md mx-auto">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              信頼度閾値: {confThreshold.toFixed(2)}
            </label>
            <input
              type="range"
              min="0.1"
              max="1.0"
              step="0.05"
              value={confThreshold}
              onChange={(e) => setConfThreshold(parseFloat(e.target.value))}
              className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700 accent-indigo-600"
            />
            <div className="flex justify-between text-xs text-gray-500 dark:text-gray-400 mt-1">
              <span>0.1</span>
              <span>1.0</span>
            </div>
          </div>

          <div className="flex gap-4 justify-center">
            <button
              onClick={detect}
              disabled={!previewUrl || isLoading}
              className="px-6 py-3 bg-indigo-600 text-white font-medium rounded-xl disabled:opacity-50 disabled:cursor-not-allowed hover:bg-indigo-700 transition-colors duration-200"
            >
              {isLoading ? (
                <span className="flex items-center gap-2">
                  <LoadingSpinner size="sm" />
                  検出中...
                </span>
              ) : (
                '検出実行'
              )}
            </button>

            <button
              onClick={reset}
              disabled={isLoading}
              className="px-6 py-3 bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 font-medium rounded-xl disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors duration-200"
            >
              リセット
            </button>
          </div>
        </section>
      )}

      {error && (
        <div className="mt-8 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl text-red-700 dark:text-red-400">
          <strong>エラー:</strong> {error}
        </div>
      )}

      {result && result.image_size && (
        <section className="space-y-8">
          <div className="text-center">
            <h2 className="text-xl font-medium text-gray-900 dark:text-white mb-6">
              検出結果
              <span className="ml-2 text-gray-500 dark:text-gray-400 font-normal">
                ({result.detections.length}件)
              </span>
            </h2>

            <DetectionCanvas
              imageUrl={previewUrl!}
              detections={result.detections}
              imageSize={result.image_size}
            />
          </div>

          <DetectionSummary detections={result.detections} />

          <div className="text-center pt-4">
            <button
              onClick={reset}
              className="px-6 py-3 bg-indigo-600 text-white font-medium rounded-xl hover:bg-indigo-700 transition-colors duration-200"
            >
              新しい画像を検出
            </button>
          </div>
        </section>
      )}
    </div>
  );
}
