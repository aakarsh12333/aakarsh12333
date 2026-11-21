import os
import requests
from PIL import Image

def get_github_stats():
    username = os.environ.get("GITHUB_USERNAME", "aakarsh12333")
    # You can later replace this with actual GitHub API calls.
    # Right now, it returns mock data to trigger the building logic.
    return {"commits": 15, "prs": 2}

def build_city():
    stats = get_github_stats()
    
    # 1. Create the background canvas (1200x800 gives us more vertical breathing room)
    canvas_w, canvas_h = 1200, 800
    city_canvas = Image.new('RGB', (canvas_w, canvas_h), color=(15, 15, 25))
    
    # 2. Map your exact filenames from the assets folder
    asset_dir = "assets"
    base_path = os.path.join(asset_dir, "Gemini_Generated_Image_2sptt32sptt32spt-removebg-preview.png")
    bldg1_path = os.path.join(asset_dir, "Gemini_Generated_Image_2sptt32sptt32spt_1_-removebg-preview.png")
    bldg2_path = os.path.join(asset_dir, "Gemini_Generated_Image_2sptt32sptt32spt_2_-removebg-preview.png")

    try:
        # .convert("RGBA") is strictly required to handle transparency
        base_img = Image.open(base_path).convert("RGBA")
        bldg1_img = Image.open(bldg1_path).convert("RGBA")
        bldg2_img = Image.open(bldg2_path).convert("RGBA")
    except FileNotFoundError as e:
        print(f"Error: Missing asset file. {e}")
        return

    # 3. Resize assets down so they fit on the screen together
    target_size = (400, 400)
    base_img = base_img.resize(target_size, Image.Resampling.LANCZOS)
    bldg1_img = bldg1_img.resize(target_size, Image.Resampling.LANCZOS)
    bldg2_img = bldg2_img.resize(target_size, Image.Resampling.LANCZOS)

    # 4. Helper function to paste assets using an Alpha Mask
    def paste_asset(asset, x, y):
        # mask=asset prevents the transparent background from rendering black
        city_canvas.paste(asset, (x, y), mask=asset)

    # 5. Build the isometric grid layout
    # Center Base Tile
    cx, cy = 400, 400
    paste_asset(base_img, cx, cy)
    
    # Left Base Tile
    left_x, left_y = cx - 200, cy - 100
    paste_asset(base_img, left_x, left_y)
    
    # Right Base Tile
    right_x, right_y = cx + 200, cy - 100
    paste_asset(base_img, right_x, right_y)

    # 6. Place the buildings ON TOP of the left and right tiles based on stats
    if stats["commits"] > 10:
        # Subtracting an extra 150 from Y so it sits perfectly on the tile
        paste_asset(bldg1_img, left_x, left_y - 150)
        
    if stats["prs"] > 0:
        paste_asset(bldg2_img, right_x, right_y - 150)

    # 7. Save the final image
    os.makedirs('dist', exist_ok=True)
    save_path = 'dist/city_render.png'
    city_canvas.save(save_path)
    print(f"City successfully rendered to {save_path}!")

if __name__ == "__main__":
    build_city()