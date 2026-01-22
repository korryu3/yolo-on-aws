export interface BoundingBox {
  x1: number;
  y1: number;
  x2: number;
  y2: number;
}

export interface Detection {
  class_id: number;
  class_name: string;
  confidence: number;
  bbox: BoundingBox;
}

export interface ImageSize {
  width: number;
  height: number;
}

export interface DetectionResponse {
  status: string;
  detections: Detection[];
  image_size?: ImageSize;
  conf_threshold?: number;
}
