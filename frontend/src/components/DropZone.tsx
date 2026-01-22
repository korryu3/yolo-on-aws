import { useState, useRef } from 'react';

interface DropZoneProps {
  onFileSelect: (file: File) => void;
  previewUrl: string | null;
  disabled?: boolean;
}

export function DropZone({ onFileSelect, previewUrl, disabled = false }: DropZoneProps) {
  const [isDragOver, setIsDragOver] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (!disabled) {
      setIsDragOver(true);
    }
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(false);

    if (disabled) return;

    const files = e.dataTransfer.files;
    if (files.length > 0) {
      const file = files[0];
      if (file.type.startsWith('image/')) {
        onFileSelect(file);
      }
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file && file.type.startsWith('image/')) {
      onFileSelect(file);
    }
  };

  const handleClick = () => {
    if (!disabled) {
      fileInputRef.current?.click();
    }
  };

  return (
    <div
      onClick={handleClick}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      className={`
        relative flex flex-col items-center justify-center
        w-full h-72 border-2 border-dashed rounded-2xl
        transition-all duration-200 ease-in-out
        ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
        ${isDragOver
          ? 'border-indigo-500 bg-indigo-50 dark:bg-indigo-900/30'
          : 'border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-800/50 hover:border-indigo-400 hover:bg-indigo-50/50 dark:hover:border-indigo-500 dark:hover:bg-indigo-900/20'
        }
      `}
    >
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        onChange={handleFileChange}
        className="hidden"
        disabled={disabled}
      />

      {previewUrl ? (
        <div className="relative w-full h-full p-4">
          <img
            src={previewUrl}
            alt="Preview"
            className="w-full h-full object-contain rounded-xl"
          />
          <div className="absolute inset-0 flex items-center justify-center bg-black/40 opacity-0 hover:opacity-100 transition-opacity duration-200 rounded-xl m-4">
            <span className="text-white font-medium">クリックで変更</span>
          </div>
        </div>
      ) : (
        <>
          <svg
            className={`w-12 h-12 mb-4 ${isDragOver ? 'text-indigo-500' : 'text-gray-400'}`}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={1.5}
              d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
            />
          </svg>
          <p className="text-lg font-medium text-gray-700 dark:text-gray-300 mb-2">
            画像をドラッグ&ドロップ
          </p>
          <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">または</p>
          <span className="px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-lg hover:bg-indigo-700 transition-colors">
            ファイルを選択
          </span>
        </>
      )}
    </div>
  );
}
