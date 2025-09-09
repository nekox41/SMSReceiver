from win10toast import ToastNotifier
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import threading
import pystray
from PIL import Image, ImageDraw

class NotificationHandler(BaseHTTPRequestHandler):

    toaster = ToastNotifier()
    
    def do_POST(self):
        content_length= int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        try:
            data = json.loads(post_data.decode("utf-8"))
            self.toaster.show_toast("来自手机的通知", data["text"])
            self.send_response_only(200)
            self.end_headers()
            self.wfile.write(b"OK")
        except Exception as e:
            print(f"error: {e}")
            self.send_response_only(400)
            self.end_headers()


def create_image(width, height, color1, color2):
    # Generate an image and draw a pattern
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill=color2)
    dc.rectangle(
        (0, height // 2, width // 2, height),
        fill=color2)

    return image

def on_exit(icon, server):
    icon.stop()
    server.shutdown()
    server.server_close()

if __name__ == "__main__":
    server = HTTPServer(('0.0.0.0', 8080), NotificationHandler)
    threading.Thread(target=server.serve_forever).start()
    print("✅启动成功，正在监听 http://0.0.0.0:8080")
    menu = pystray.Menu(
        pystray.MenuItem("退出", lambda icon: on_exit(icon, server)),
    )
    icon = pystray.Icon("test", create_image(64, 64, "black", "white"), "SMSReceiver", menu)
    icon.run()