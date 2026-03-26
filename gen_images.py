import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import requests
import base64
import os
import json

API_KEY = "AIzaSyBe4ATw6sh__AVpXUmTvudknYLV3ejGC0Y"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

IMAGES = [
    {
        "file": "img-hero.png",
        "prompt": (
            "Real editorial photograph of a modern empty city street at night, shot from ground level "
            "looking up at tall glass office buildings. Long exposure, light trails, very dark moody atmosphere. "
            "Shot on Sony A7R IV, 16mm wide angle, f/8, ISO 800. No people, no text. "
            "Color graded dark charcoal with slight warm glow from windows. Grain texture visible. "
            "Feels like a real photograph taken by a professional photographer, not AI generated."
        ),
        "aspect": "16:9",
    },
    {
        "file": "img-freedom.png",
        "prompt": (
            "Real candid photograph: a man in his 30s, back to camera, standing on a rooftop "
            "looking over a city skyline at golden hour. Arms slightly spread, relaxed posture. "
            "Shot on Canon 5D Mark IV, 50mm, f/2.0, natural backlight. "
            "Feels like genuine editorial lifestyle photography, film-like grain, warm tones. "
            "Not staged, natural moment captured. No text."
        ),
        "aspect": "4:3",
    },
    {
        "file": "img-lawyer.png",
        "prompt": (
            "Real professional headshot photograph of a serious confident man in his 40s, "
            "dark navy suit, white shirt, no tie. Sitting slightly turned, looking directly at camera. "
            "Shot on Hasselblad medium format, 80mm, f/2.8, studio soft-box lighting from left side. "
            "Dark grey seamless backdrop. Shallow depth of field. Sharp eyes. "
            "Looks like a real law firm partner photo, not AI. No text."
        ),
        "aspect": "1:1",
    },
    {
        "file": "img-team.png",
        "prompt": (
            "Real candid workplace photo: 3 professionals around a dark wooden table in a modern office, "
            "looking at documents, one person pointing at paper. "
            "Shot on Fujifilm X-T4, 23mm, f/2.8, available light from large window. "
            "Slightly moody office environment, dark interior design, plants in background. "
            "Journalistic documentary style, natural expressions, real people. No text."
        ),
        "aspect": "16:9",
    },
    {
        "file": "img-court.png",
        "prompt": (
            "Real architectural photograph of a grand courthouse entrance, stone columns, "
            "heavy wooden doors, low dramatic angle shot at dusk. "
            "Shot on Canon EOS R5, 24mm tilt-shift, f/11, blue hour lighting. "
            "Moody dramatic sky, stone texture clearly visible, slight vignette. "
            "Feels like real architectural photography. No people, no text."
        ),
        "aspect": "4:3",
    },
]

URL = (
    f"https://generativelanguage.googleapis.com/v1beta/models/"
    f"imagen-4.0-generate-001:predict?key={API_KEY}"
)

def generate(item):
    payload = {
        "instances": [{"prompt": item["prompt"]}],
        "parameters": {
            "sampleCount": 1,
            "aspectRatio": item["aspect"],
        },
    }
    print(f"  Generating {item['file']} ...", end=" ", flush=True)
    resp = requests.post(URL, json=payload, timeout=60)
    if resp.status_code != 200:
        print(f"FAIL ({resp.status_code}): {resp.text[:200]}")
        return False
    data = resp.json()
    try:
        b64 = data["predictions"][0]["bytesBase64Encoded"]
        path = os.path.join(OUT_DIR, item["file"])
        with open(path, "wb") as f:
            f.write(base64.b64decode(b64))
        print(f"OK - saved {item['file']}")
        return True
    except (KeyError, IndexError) as e:
        print(f"PARSE ERROR: {e}\nResponse: {json.dumps(data)[:300]}")
        return False

if __name__ == "__main__":
    print("=== Image Generation ===\n")
    ok = 0
    for img in IMAGES:
        if generate(img):
            ok += 1
    print(f"\nDone: {ok}/{len(IMAGES)} images generated in:\n  {OUT_DIR}")
