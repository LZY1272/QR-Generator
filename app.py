from fastapi import FastAPI, Request
from PIL import Image, ImageDraw, ImageFont
import qrcode
import io
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.post("/generate_ticket")
async def generate_ticket(req: Request):
    data = await req.json()

    first_name = data.get("first_name", "")
    last_name = data.get("last_name", "")
    phone = data.get("phone", "")
    email = data.get("email", "")
    date = data.get("pls_choose_a_date", "")

    # Generate the form URL
    url = (
        "https://api.leadconnectorhq.com/widget/form/ZEWXWd1OK2WIC0l9PK3f"
        f"?will_attending_|_上课日期={date}&first_name={first_name}"
        f"&last_name={last_name}&phone={phone}&email={email}"
    )

    # Generate QR code
    qr_img = qrcode.make(url).resize((200, 200))
    bg = Image.new("RGB", (600, 400), color="white")
    bg.paste(qr_img, (50, 100))

    draw = ImageDraw.Draw(bg)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()

    draw.text((270, 100), f"Name: {first_name} {last_name}", fill="black", font=font)
    draw.text((270, 140), f"Phone: {phone}", fill="black", font=font)
    draw.text((270, 180), f"Email: {email}", fill="black", font=font)
    draw.text((270, 220), f"Date: {date}", fill="black", font=font)
    draw.text((50, 320), "Scan the QR to confirm registration", fill="black", font=font)

    img_byte_arr = io.BytesIO()
    bg.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)

    return StreamingResponse(img_byte_arr, media_type="image/png")
