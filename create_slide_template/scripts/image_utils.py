import os
import sys
from pathlib import Path
import google.generativeai as genai
from PIL import Image
import io

def generate_image_from_prompt(prompt: str, output_path: str, api_key: str = None):
    """
    Gemini (NanoBanaNana) を使用して画像を生成し、保存する
    """
    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        print("エラー: GEMINI_API_KEY が設定されていません。画像生成をスキップします。")
        return False
        
    try:
        genai.configure(api_key=api_key)
        
        # モデル名は利用可能な最新の画像生成モデルを指定
        # 注意: 2024年現在、一般公開されているAPIでのモデル名は変動しやすいため
        # 実際には 'gemini-pro' 等のテキストモデルではなく画像生成専用モデルが必要
        # ここでは 'gemini-1.5-pro-latest' 等、マルチモーダル対応モデルでの生成を試みるか
        # もしくは Imagen on Vertex AI の使用が一般的だが、
        # 簡易的に google-generativeai SDK の画像生成メソッド(もしあれば)を使用する想定
        
        # ※実際のGemini Image Generation APIのリファレンスに基づくコード
        # 現時点ではSDKの仕様が流動的なため、例外処理で囲みつつ実装
        
        # 仮の実装: 多くの場合はimagenモデルを指定する
        model = genai.GenerativeModel('gemini-1.5-pro') 
        
        # 注: google-generativeai ライブラリでの画像生成はまだBeta等の可能性があるため
        # エラー時はダミー画像を生成する等のフォールバック推奨
        
        print(f"画像生成中... プロンプト: {prompt[:30]}...")
        
        # TODO: 正式な画像生成APIコールに変更が必要な可能性あり
        # response = model.generate_content(prompt) # これはテキスト/マルチモーダル用
        
        # ダミー実装（APIキーがない場合やモデル未対応時のためのプレースホルダー）
        # 実際にはここで img = response.images[0] のように取得したい
        
        # テスト用に単色画像を作成
        img = Image.new('RGB', (800, 600), color = (73, 109, 137))
        img.save(output_path)
        print(f"画像保存完了（ダミー）: {output_path}")
        return True

    except Exception as e:
        print(f"画像生成エラー: {e}")
        return False

def add_image_to_slide(slide, image_info, output_dir="output/images"):
    """
    スライドに画像を追加する
    image_info format:
    {
        "generated": true,
        "prompt": "Description...",
        "path": "path/to/existing/image.png", # 既存画像の場合
        "position": {"left": 1.0, "top": 2.0, "width": 6.0, "height": 4.0}
    }
    """
    # 保存先ディレクトリ
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    image_path = image_info.get("path")
    
    # 画像生成が必要な場合
    if image_info.get("generated") and image_info.get("prompt"):
        prompt = image_info["prompt"]
        filename = f"gen_{hash(prompt)}.png"
        generated_path = str(Path(output_dir) / filename)
        
        if generate_image_from_prompt(prompt, generated_path):
            image_path = generated_path
    
    if not image_path or not os.path.exists(image_path):
        print(f"警告: 画像ファイルが見つからないため追加できません: {image_path}")
        return

    # 位置情報
    from pptx.util import Inches
    pos = image_info.get("position", {})
    left = Inches(pos.get("left", 1.0))
    top = Inches(pos.get("top", 2.0))
    width = Inches(pos.get("width", 6.0))
    height = Inches(pos.get("height", 4.0))
    
    # 画像を追加
    slide.shapes.add_picture(image_path, left, top, width, height)
