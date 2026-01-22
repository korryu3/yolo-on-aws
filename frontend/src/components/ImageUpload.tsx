import { useState } from 'react';
import { DetectionCanvas } from './DetectionCanvas';

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

interface ApiResponse {
  status: string;
  detections: Detection[];
  image_size?: {
    width: number;
    height: number;
  };
  conf_threshold?: number;
}

export function ImageUpload() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<ApiResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [confThreshold, setConfThreshold] = useState<number>(0.25);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    // 画像ファイルのみ許可
    if (!file.type.startsWith('image/')) {
      setError('画像ファイルを選択してください');
      return;
    }

    setSelectedFile(file);
    setError(null);
    setResult(null);

    // プレビュー画像を生成
    const reader = new FileReader();
    reader.onloadend = () => {
      setPreviewUrl(reader.result as string);
    };
    reader.readAsDataURL(file);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('画像を選択してください');
      return;
    }

    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('conf_threshold', confThreshold.toString());

      const apiUrl = import.meta.env.VITE_API_URL;
      if (!apiUrl) {
        throw new Error('API URLが設定されていません');
      }

      const response = await fetch(`${apiUrl}/api/detect`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`APIエラー: ${response.status}`);
      }

      const data: ApiResponse = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : '不明なエラーが発生しました');
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setPreviewUrl(null);
    setResult(null);
    setError(null);
  };

  return (
    <div className="max-w-4xl mx-auto p-8">
      <h1 className="text-4xl font-bold text-center text-gray-800 dark:text-white mb-8">
        YOLO 物体検出
      </h1>
      
      <div className="mb-8 text-center">
        <input
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          id="file-input"
          className="hidden"
        />
        <label 
          htmlFor="file-input" 
          className="inline-block px-6 py-3 bg-indigo-600 text-white rounded-lg cursor-pointer hover:bg-indigo-700 transition-colors duration-200"
        >
          画像を選択
        </label>
        
        {selectedFile && (
          <p className="mt-4 text-sm text-gray-600 dark:text-gray-400">{selectedFile.name}</p>
        )}
      </div>

      {/* 信頼度閾値スライダー */}
      <div className="mb-8 max-w-md mx-auto">
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
          className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700"
        />
        <div className="flex justify-between text-xs text-gray-500 dark:text-gray-400 mt-1">
          <span>0.1</span>
          <span>1.0</span>
        </div>
      </div>

      {previewUrl && !result && (
        <div className="mb-8 text-center">
          <h3 className="text-xl font-semibold mb-4 text-gray-800 dark:text-white">プレビュー</h3>
          <img 
            src={previewUrl} 
            alt="Preview" 
            className="max-w-full max-h-96 mx-auto rounded-lg shadow-lg"
          />
        </div>
      )}

      <div className="flex gap-4 justify-center mb-8">
        <button
          onClick={handleUpload}
          disabled={!selectedFile || isLoading}
          className="px-6 py-3 bg-indigo-600 text-white rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-indigo-700 transition-colors duration-200"
        >
          {isLoading ? '処理中...' : '検出実行'}
        </button>
        
        <button
          onClick={handleReset}
          disabled={isLoading}
          className="px-6 py-3 bg-gray-200 text-gray-800 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-300 transition-colors duration-200"
        >
          リセット
        </button>
      </div>

      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 mb-8">
          <strong>エラー:</strong> {error}
        </div>
      )}

      {result && result.image_size && (
        <div className="mb-8">
          <h3 className="text-xl font-semibold mb-4 text-center text-gray-800 dark:text-white">
            検出結果 ({result.detections.length}件)
          </h3>
          
          {/* Canvas + 画像表示 */}
          <div className="text-center mb-6">
            <DetectionCanvas
              imageUrl={previewUrl!}
              detections={result.detections}
              imageSize={result.image_size}
            />
          </div>

          {/* 検出結果テーブル */}
          {result.detections.length > 0 && (
            <div className="overflow-x-auto">
              <table className="min-w-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg">
                <thead className="bg-gray-100 dark:bg-gray-700">
                  <tr>
                    <th className="px-4 py-2 text-left text-sm font-semibold text-gray-700 dark:text-gray-300">信頼度</th>
                    <th className="px-4 py-2 text-left text-sm font-semibold text-gray-700 dark:text-gray-300">座標 (x1, y1, x2, y2)</th>
                  </tr>
                </thead>
                <tbody>
                  {result.detections.map((detection, index) => (
                    <tr key={index} className="border-t border-gray-200 dark:border-gray-700">
                      <td className="px-4 py-2 text-sm text-gray-800 dark:text-gray-200">
                        {(detection.confidence * 100).toFixed(1)}%
                      </td>
                      <td className="px-4 py-2 text-sm text-gray-800 dark:text-gray-200 font-mono">
                        ({detection.bbox.x1}, {detection.bbox.y1}, {detection.bbox.x2}, {detection.bbox.y2})
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
