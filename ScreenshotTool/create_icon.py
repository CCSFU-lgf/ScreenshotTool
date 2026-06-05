from PIL import Image, ImageDraw

sizes = [16, 32, 48, 64, 128, 256]
images = []

for size in sizes:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    padding = max(2, size // 8)
    draw.rectangle(
        [padding, padding, size - padding, size - padding],
        fill="#2196F3",
        outline="#1565C0",
        width=max(1, size // 16)
    )

    inner_pad = max(4, size // 4)
    draw.rectangle(
        [inner_pad, inner_pad, size - inner_pad, size - inner_pad],
        outline="white",
        width=max(1, size // 20)
    )

    center = size // 2
    dot_size = max(2, size // 10)
    draw.ellipse(
        [center - dot_size, center - dot_size, center + dot_size, center + dot_size],
        fill="white"
    )

    images.append(img)

images[0].save(
    "assets/icon.ico",
    format="ICO",
    sizes=[(s, s) for s in sizes],
    append_images=images[1:]
)
print("icon.ico 已生成")
