import { useState, useCallback } from 'react';
import type { DetectionResponse } from '../types/detection';

interface UseDetectionReturn {
  selectedFile: File | null;
  previewUrl: string | null;
  result: DetectionResponse | null;
  error: string | null;
  isLoading: boolean;
  confThreshold: number;
  setConfThreshold: (value: number) => void;
  selectFile: (file: File) => void;
  detect: () => Promise<void>;
  reset: () => void;
}

export function useDetection(): UseDetectionReturn {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [result, setResult] = useState<DetectionResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [confThreshold, setConfThreshold] = useState(0.25);

  const selectFile = useCallback((file: File) => {
    if (!file.type.startsWith('image/')) {
      setError('画像ファイルを選択してください');
      return;
    }

    setSelectedFile(file);
    setError(null);
    setResult(null);

    const reader = new FileReader();
    reader.onloadend = () => {
      setPreviewUrl(reader.result as string);
    };
    reader.readAsDataURL(file);
  }, []);

  const detect = useCallback(async () => {
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

      const apiUrl = import.meta.env.VITE_API_URL ?? '';
      const endpoint = apiUrl ? `${apiUrl}/api/detect` : '/api/detect';

      const response = await fetch(endpoint, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`APIエラー: ${response.status}`);
      }

      const data: DetectionResponse = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : '不明なエラーが発生しました');
    } finally {
      setIsLoading(false);
    }
  }, [selectedFile, confThreshold]);

  const reset = useCallback(() => {
    setSelectedFile(null);
    setPreviewUrl(null);
    setResult(null);
    setError(null);
  }, []);

  return {
    selectedFile,
    previewUrl,
    result,
    error,
    isLoading,
    confThreshold,
    setConfThreshold,
    selectFile,
    detect,
    reset,
  };
}
