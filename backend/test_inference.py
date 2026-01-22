"""
YOLOモデルの推論をテストするスクリプト
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import io
from main import (
    load_yolo_model,
    preprocess_image,
    run_inference,
    postprocess_detections
)

def draw_detections(image_bytes: bytes, detections: list[dict], output_path: str):
    """検出結果を画像に描画して保存"""
    # 画像を開く
    image = Image.open(io.BytesIO(image_bytes))
    draw = ImageDraw.Draw(image)
    width, height = image.size
    
    # フォント（デフォルトフォント使用）
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
    except:
        font = ImageFont.load_default()
    
    # 各検出結果を描画
    for det in detections:
        bbox = det['bbox']
        confidence = det['confidence']
        
        # 正規化座標を実座標に変換
        x1 = int(bbox['x1'] * width)
        y1 = int(bbox['y1'] * height)
        x2 = int(bbox['x2'] * width)
        y2 = int(bbox['y2'] * height)
        
        # バウンディングボックスを描画（黄色）
        draw.rectangle([x1, y1, x2, y2], outline="yellow", width=3)
        
        # ラベル描画
        label = f"{confidence:.1%}"
        
        # テキスト背景
        bbox_text = draw.textbbox((x1, y1 - 25), label, font=font)
        draw.rectangle(bbox_text, fill="yellow")
        draw.text((x1, y1 - 25), label, fill="black", font=font)
    
    # 保存
    image.save(output_path)
    print(f"✓ Saved result to: {output_path}")

def main():
    # モデルとテスト画像のパス
    model_path = Path(__file__).parent / "YOLOv10n.onnx"
    test_image_path = Path(__file__).parent / "test-image.jpg"
    
    print(f"Model path: {model_path}")
    print(f"Test image path: {test_image_path}")
    print(f"Model exists: {model_path.exists()}")
    print(f"Image exists: {test_image_path.exists()}")
    print()
    
    if not model_path.exists():
        print(f"❌ Model not found: {model_path}")
        return
    
    if not test_image_path.exists():
        print(f"❌ Test image not found: {test_image_path}")
        return
    
    # モデルロード
    print("Loading model...")
    session = load_yolo_model(str(model_path))
    print("✓ Model loaded")
    
    # 入力情報を確認
    print("\nModel input info:")
    for inp in session.get_inputs():
        print(f"  Name: {inp.name}")
        print(f"  Shape: {inp.shape}")
        print(f"  Type: {inp.type}")
    
    print("\nModel output info:")
    for out in session.get_outputs():
        print(f"  Name: {out.name}")
        print(f"  Shape: {out.shape}")
        print(f"  Type: {out.type}")
    
    # 画像読み込み
    print("\nReading test image...")
    with open(test_image_path, "rb") as f:
        image_bytes = f.read()
    
    # 前処理
    print("Preprocessing...")
    input_tensor, original_size = preprocess_image(image_bytes)
    print(f"  Input tensor shape: {input_tensor.shape}")
    print(f"  Original size: {original_size}")
    
    # 推論
    print("\nRunning inference...")
    outputs = run_inference(session, input_tensor)
    print(f"  Output shape: {outputs.shape}")
    print(f"  Output dtype: {outputs.dtype}")
    print(f"  Output range: [{outputs.min():.4f}, {outputs.max():.4f}]")
    
    # 後処理（複数の閾値でテスト）
    for conf_threshold in [0.1, 0.25, 0.5]:
        print(f"\nPostprocessing with conf_threshold={conf_threshold}...")
        detections = postprocess_detections(outputs, original_size, conf_threshold)
        print(f"  Detected: {len(detections)} objects")
        
        for i, det in enumerate(detections[:5], 1):  # 最初の5件のみ表示
            print(f"  [{i}] {det['class_name']} - {det['confidence']:.1%}")
            print(f"      bbox: ({det['bbox']['x1']:.4f}, {det['bbox']['y1']:.4f}, "
                  f"{det['bbox']['x2']:.4f}, {det['bbox']['y2']:.4f})")
        
        # 画像に描画して保存
        output_path = Path(__file__).parent / f"result_conf{conf_threshold}.jpg"
        draw_detections(image_bytes, detections, str(output_path))

if __name__ == "__main__":
    main()
