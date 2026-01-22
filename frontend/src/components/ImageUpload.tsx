import { useState } from 'react';

interface Detection {
  // 将来的にYOLOの検出結果を格納
}

interface ApiResponse {
  status: string;
  detections: Detection[];
  message?: string;
}

export function ImageUpload() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<ApiResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

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

      {previewUrl && (
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

      {result && (
        <div className="p-6 bg-gray-50 dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
          <h3 className="text-xl font-semibold mb-4 text-gray-800 dark:text-white">結果</h3>
          <pre className="bg-white dark:bg-gray-900 p-4 rounded overflow-x-auto text-sm text-gray-800 dark:text-gray-200">
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
